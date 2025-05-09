import argparse
import json

import torch
from tqdm import trange, tqdm
from transformers.tokenization_utils import BatchEncoding
from torch.utils.tensorboard import SummaryWriter

from temporal_embeddings.parameters.parameters import (
    EPOCHS, DEVICE, DTYPE, NUM_EVAL_STEPS, OUTPUT_DIRECTORY_PATH, MODEL_NAME, LR,
    WEIGHT_DECAY, NUM_WARMUP_RATIO, TEMPERATURE, INPUT_FILE_PATH, BATCH_SIZE, SEED
)
from temporal_embeddings.model.gauss_model import GaussOutput
from temporal_embeddings.utils.similarity import asymmetrical_kl_sim
from temporal_embeddings.utils.set_seed import set_seed
from temporal_embeddings.execution.execution import Execution
from temporal_embeddings.utils.save import save_json
from temporal_embeddings.utils.loss.cosent_loss import CoSentLoss
from datetime import datetime

def main(data_fraction: float, model_name: str, batch_size: int, lr: float, weight_decay: float, epochs: int, 
         num_warmup_ratio: float, temperature: float, num_eval_steps: int, 
         input_file_path: str, output_directory_path: str) -> None:
    set_seed(seed=SEED)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir_path: str = f"logs/runs/experiment_{current_time}"
    writer = SummaryWriter(log_dir=log_dir_path)
    
    parameters = {
        "model_name": model_name,
        "batch_size": batch_size,
        "learning_rate": lr,
        "weight_decay": weight_decay,
        "epochs": epochs,
        "num_warmup_ratio": num_warmup_ratio,
        "temperature": temperature,
        "num_eval_steps": num_eval_steps,
        "input_file_path": input_file_path,
        "output_directory_path": output_directory_path,
    }
    
    with open(f"{log_dir_path}/parameters.json", "w") as param_file:
        json.dump(parameters, param_file, indent=4)
    
    print("Parameters logged in:", f"{log_dir_path}/parameters.json")
    
    print("Load the execution object")
    execution = Execution(data_fraction=data_fraction, 
                          model_name=model_name, 
                          batch_size=batch_size, 
                          lr=lr, 
                          weight_decay=weight_decay, 
                          epochs=epochs, 
                          num_warmup_ratio=num_warmup_ratio, 
                          temperature=temperature, 
                          num_eval_steps=num_eval_steps, 
                          input_file_path=input_file_path, 
                          output_directory_path=output_directory_path)

    print("Compute the first dev score")
    best_dev_score = execution.evaluator("val")
    best_epoch, best_step = 0, 0
    val_metrics = {
        "epoch": best_epoch,
        "step": best_step,
        "loss": float("inf"),
        "dev_score": best_dev_score,
    }
    execution.log(val_metrics)
    best_state_dict = execution.clone_state_dict()

    scaler = torch.cuda.amp.GradScaler()
    
    current_step = 0

    for epoch in trange(epochs, leave=False, dynamic_ncols=True, desc="Epoch"):
        train_losses = []
        execution.model.train()

        for batch in tqdm(execution.gauss_data.train_dataloader, total=len(execution.gauss_data.train_dataloader), dynamic_ncols=True, leave=False, desc="Step"):
            current_step += 1
            batch: BatchEncoding = batch.to(DEVICE)

            with torch.cuda.amp.autocast(dtype=DTYPE):
                sent0_input_ids = batch.sent0.input_ids.to(DEVICE)
                sent0_attention_mask = batch.sent0.attention_mask.to(DEVICE)
                sent0_out: GaussOutput = execution.model.forward(input_ids=sent0_input_ids, attention_mask=sent0_attention_mask, dates=batch.sent0_date.to(DEVICE))

                sent1_input_ids = batch.sent1.input_ids.to(DEVICE)
                sent1_attention_mask = batch.sent1.attention_mask.to(DEVICE)
                sent1_out: GaussOutput = execution.model.forward(input_ids=sent1_input_ids, attention_mask=sent1_attention_mask, dates=batch.sent1_date.to(DEVICE))

            sim_mat: torch.FloatTensor = asymmetrical_kl_sim(sent0_out.mu, sent0_out.std, sent1_out.mu, sent1_out.std)
            
            criterion = CoSentLoss()
            loss = criterion(sim_mat, batch.score)

            train_losses.append(loss.item())

            execution.optimizer.zero_grad()
            scaler.scale(loss).backward()
            scaler.step(execution.optimizer)

            scale = scaler.get_scale()
            scaler.update()

            if scale <= scaler.get_scale():
                execution.lr_scheduler.step()
            
            if current_step % num_eval_steps == 0:
                execution.model.eval()

                dev_score = execution.evaluator("val")

                if best_dev_score < dev_score:
                    best_dev_score = dev_score
                    best_epoch, best_step = epoch, current_step
                    best_state_dict = execution.clone_state_dict()

                val_metrics = {
                    "epoch": epoch,
                    "step": current_step,
                    "loss": sum(train_losses) / len(train_losses),
                    "dev_score": dev_score,
                }

                print(f"Writing to TensorBoard at step {current_step}:")
                for key, value in val_metrics.items():
                    print(f"  Metrics/{key}: {value}")
                    writer.add_scalar(f"Metrics/{key}", value, current_step)

                print(f"  Loss/train: {sum(train_losses) / len(train_losses)}")
                writer.add_scalar("Loss/train", sum(train_losses) / len(train_losses), current_step)

                print(f"  Score/dev: {dev_score}")
                writer.add_scalar("Score/dev", dev_score, current_step)

                print(f"  Learning_Rate: {execution.optimizer.param_groups[0]['lr']}")
                writer.add_scalar("Learning_Rate", execution.optimizer.param_groups[0]["lr"], current_step)

                execution.log(val_metrics)
                train_losses = []

                execution.model.train()

    dev_metrics = {
        "best-epoch": best_epoch,
        "best-step": best_step,
        "best-dev-auc": best_dev_score,
    }
    save_json(dev_metrics, output_directory_path / "dev-metrics.json")

    execution.model.load_state_dict(best_state_dict)
    torch.save(execution.model.state_dict(), "temporal_bert.pth")
    execution.model.eval().to(DEVICE)

    metrics = execution.evaluator(split="train")
    save_json(metrics, output_directory_path / "metrics.json")

    writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the temporal embeddings model.")
    parser.add_argument("--data_fraction", type=float, default=1.0, help="Fraction of data to use for training.")
    parser.add_argument("--model_name", type=str, default=MODEL_NAME, help="Name of the model.")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Size of the batch.")
    parser.add_argument("--lr", type=float, default=LR, help="Learning rate.")
    parser.add_argument("--weight_decay", type=float, default=WEIGHT_DECAY, help="Weight decay.")
    parser.add_argument("--epochs", type=int, default=EPOCHS, help="Number of epochs.")
    parser.add_argument("--num_warmup_ratio", type=float, default=NUM_WARMUP_RATIO, help="Warmup ratio.")
    parser.add_argument("--temperature", type=float, default=TEMPERATURE, help="Temperature for loss scaling.")
    parser.add_argument("--num_eval_steps", type=int, default=NUM_EVAL_STEPS, help="Number of evaluation steps.")
    parser.add_argument("--input_file_path", type=str, default=INPUT_FILE_PATH, help="Path to the input file.")
    parser.add_argument("--output_directory_path", type=str, default=str(OUTPUT_DIRECTORY_PATH), help="Path to the output directory.")
    args = parser.parse_args()

    main(
        data_fraction=args.data_fraction,
        model_name=args.model_name,
        batch_size=args.batch_size,
        lr=args.lr,
        weight_decay=args.weight_decay,
        epochs=args.epochs,
        num_warmup_ratio=args.num_warmup_ratio,
        temperature=args.temperature,
        num_eval_steps=args.num_eval_steps,
        input_file_path=args.input_file_path,
        output_directory_path=args.output_directory_path,
    )