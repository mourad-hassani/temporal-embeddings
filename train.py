import argparse

import torch
from tqdm import trange, tqdm
from transformers.tokenization_utils import BatchEncoding

from temporal_embeddings.parameters.parameters import EPOCHS, DEVICE, DTYPE, NUM_EVAL_STEPS, OUTPUT_DIRECTORY_PATH
from temporal_embeddings.model.gauss_model import GaussOutput
from temporal_embeddings.utils.similarity import asymmetrical_kl_sim
from temporal_embeddings.utils.set_seed import set_seed
from temporal_embeddings.execution.execution import Execution
from temporal_embeddings.utils.save import save_json
from temporal_embeddings.utils.loss.cosent_loss import CoSentLoss

def main() -> None:
    set_seed()
    
    execution = Execution()

    best_dev_score = execution.evaluator()
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

    for epoch in trange(EPOCHS, leave=False, dynamic_ncols=True, desc="Epoch"):
        train_losses = []
        execution.model.train()

        for batch in tqdm(execution.gauss_data.train_dataloader, total=len(execution.gauss_data.train_dataloader), dynamic_ncols=True, leave=False, desc="Step"):
            current_step += 1
            batch: BatchEncoding = batch.to(DEVICE)

            with torch.cuda.amp.autocast(dtype=DTYPE):
                sent0_input_ids = batch.sent0.input_ids.to(DEVICE)
                sent0_attention_mask = batch.sent0.attention_mask.to(DEVICE)
                sent0_out: GaussOutput = execution.model.forward(input_ids=sent0_input_ids, attention_mask=sent0_attention_mask, date=batch.sent0_date.to(DEVICE))

                sent1_input_ids = batch.sent1.input_ids.to(DEVICE)
                sent1_attention_mask = batch.sent1.attention_mask.to(DEVICE)
                sent1_out: GaussOutput = execution.model.forward(input_ids=sent1_input_ids, attention_mask=sent1_attention_mask, date=batch.sent1_date.to(DEVICE))

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
            
            if current_step % NUM_EVAL_STEPS == 0:
                execution.model.eval()

                dev_score = execution.evaluator()

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
                execution.log(val_metrics)
                train_losses = []

                execution.model.train()

    dev_metrics = {
        "best-epoch": best_epoch,
        "best-step": best_step,
        "best-dev-auc": best_dev_score,
    }
    save_json(dev_metrics, OUTPUT_DIRECTORY_PATH / "dev-metrics.json")

    execution.model.load_state_dict(best_state_dict)
    torch.save(execution.model.state_dict(), "temporal_bert.pth")
    execution.model.eval().to(DEVICE)

    metrics = execution.evaluator(split="train")
    save_json(metrics, OUTPUT_DIRECTORY_PATH / "metrics.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the temporal embeddings model.")
    parser.add_argument("--data_fraction", type=float, default=1.0, help="Fraction of data to use for training.")
    args = parser.parse_args()

    execution = Execution(data_fraction=args.data_fraction)
    main()