import torch
from torch.utils.data import DataLoader
from scipy.stats import spearmanr
from transformers import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer

from temporal_embeddings.model.gauss_model import GaussOutput, GaussModel
from parameters import DTYPE, DEVICE, MODEL_NAME, MAX_SEQ_LEN, INPUT_FILE_PATH, OUTPUT_DIRECTORY_PATH
from temporal_embeddings.data.utils.gauss_data import GaussData
from temporal_embeddings.data.utils.similarity import asymmetrical_kl_sim
from temporal_embeddings.data.utils.save import save_json

class Evaluator():
    def __init__(self):
        self.model: GaussModel = GaussModel(MODEL_NAME, True).eval().to(DEVICE)
        self.model.load_state_dict(torch.load('temporal_bert.pth', map_location=torch.device(DEVICE)))

        self.tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, model_max_length = MAX_SEQ_LEN, use_fast = False)

        self.gauss_data: GaussData = GaussData(INPUT_FILE_PATH, self.tokenizer)

    @torch.inference_mode()
    def evaluate(self) -> float:
        self.model.eval()

        sent0_output: list[GaussOutput] = []
        sent1_output: list[GaussOutput] = []

        scores: torch.FloatTensor = torch.FloatTensor()

        data_loader: DataLoader = self.gauss_data.test_dataloader

        for batch in data_loader:
            with torch.cuda.amp.autocast(dtype=DTYPE):
                sent0_out = self.model.forward(**batch.to(DEVICE).sent0)
                sent1_out = self.model.forward(**batch.to(DEVICE).sent1)
                scores = torch.cat([scores.to(DEVICE), (batch.to(DEVICE).score)], dim=0)

            sent0_output.append(sent0_out)
            sent1_output.append(sent1_out)

        output0: GaussOutput = GaussOutput(mu=torch.cat([out.mu for out in sent0_output], dim=0), std=torch.cat([out.std for out in sent0_output], dim=0))
        output1: GaussOutput = GaussOutput(mu=torch.cat([out.mu for out in sent1_output], dim=0), std=torch.cat([out.std for out in sent1_output], dim=0))

        similarities = asymmetrical_kl_sim(output0.mu, output0.std, output1.mu, output1.std)

        spearman = float(spearmanr(scores.to("cpu").abs(), similarities.to("cpu"))[0]) * 100

        return spearman
    
if __name__ == "__main__":
    evaluator: Evaluator = Evaluator()

    metrics: float = evaluator.evaluate()
    save_json(metrics, OUTPUT_DIRECTORY_PATH / "metrics.json")