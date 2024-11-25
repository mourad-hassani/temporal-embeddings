import torch
from torch.utils.data import DataLoader
from transformers.tokenization_utils import BatchEncoding, PreTrainedTokenizer
from transformers import AutoTokenizer

from temporal_embeddings.model.gauss_model import GaussModel, GaussOutput
from parameters import MODEL_NAME, INFERENCE_DEVICE, BATCH_SIZE, NUM_WORKERS, MAX_SEQ_LEN, INPUT_FILE_PATH, SPECIAL_TOKENS
from temporal_embeddings.data_utils.utils.similarity import asymmetrical_kl_sim

class Inference:
    def __init__(self, sentences1: list[str], sentences2: list[str], scores: list[float]):
        self.model = GaussModel(MODEL_NAME, True).eval().to(INFERENCE_DEVICE)
        self.model.load_state_dict(torch.load('temporal_bert.pth', map_location=torch.device(INFERENCE_DEVICE)))

        self.tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, model_max_length = MAX_SEQ_LEN, use_fast = False)

        self.sentences1, self.sentences2, self.scores = sentences1, sentences2, scores

    def tokenize(self, batch: list[str]) -> BatchEncoding:
        return self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=MAX_SEQ_LEN, add_special_tokens=SPECIAL_TOKENS)
    
    def data_loader(self, sentences: list[str]):
        return DataLoader(sentences, collate_fn=self.tokenize, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True, drop_last=False)

    def sim_fn(self, sent1: str, sent2: str) -> float:
            sent1: GaussOutput = self.encode_fn(sent1)
            sent2: GaussOutput = self.encode_fn(sent2)
            return asymmetrical_kl_sim(sent1.mu, sent1.std, sent2.mu, sent2.std).item()

    @torch.inference_mode()
    def encode_fn(self, sentence: str, **_) -> GaussOutput:
        self.model.eval()

        output: GaussOutput = None

        for batch in self.data_loader([sentence]):
            output = self.model.forward(**batch.to(INFERENCE_DEVICE))
            break

        return output
    
    def evaluate(self) -> dict:
        similarities: list[float] = []
        
        for sent1, sent2 in zip(self.sentences1, self.sentences2):
            similarities.append(self.sim_fn(sent1, sent2))
        
        return {"sent1": self.sentences1, "sent2": self.sentences2, "similarity": similarities, "ground_truth": self.scores}