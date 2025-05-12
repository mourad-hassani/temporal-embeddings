import torch
from torch.utils.data import DataLoader
from transformers.tokenization_utils import BatchEncoding, PreTrainedTokenizer
from transformers import AutoTokenizer
from typing import List, Dict

from temporal_embeddings.model.gauss_model import GaussModel, GaussOutput
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.parameters import INFERENCE_DEVICE, NUM_WORKERS, SPECIAL_TOKENS
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.similarity import asymmetrical_kl_sim
from temporal_embeddings.utils.positional_encoding import positional_encoding

class Inference:
    def __init__(self, model_name: str, model_path: str, batch_size: int, max_seq_len: int):
        self.model_name: str = model_name
        self.model_path: str = model_path
        self.batch_size: int = batch_size
        self.max_seq_len: int = max_seq_len

        if model_name == "all-minilm-l6-v2":
            self.model_name = "sentence-transformers/all-MiniLM-L6-v2"

        self.model: GaussModel = GaussModel(self.model_name, False).eval().to(INFERENCE_DEVICE)
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device(INFERENCE_DEVICE)))

        self.tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(self.model_name, model_max_length = self.max_seq_len, use_fast = False)

        self.cached_embeddings: Dict = {}

    def set_sentences(self, sentences1: List[str], sentences1_dates: List[str], sentences2: List[str], sentences2_dates: List[str], scores: list[float]):
        self.sentences1, self.sentences2, self.scores = sentences1, sentences2, scores
        self.sentences1_dates, self.sentences2_dates = sentences1_dates, sentences2_dates

    def tokenize(self, batch: list[str]) -> BatchEncoding:
        return self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=self.max_seq_len, add_special_tokens=SPECIAL_TOKENS)
    
    def data_loader(self, sentences: list[str]):
        return DataLoader(sentences, collate_fn=self.tokenize, batch_size=self.batch_size, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True, drop_last=False)

    def sim_fn(self, sent1: list[str], sent1_dates: list[str], sent2: list[str], sent2_dates: list[str]) -> float:
        sent1: GaussOutput = self.encode_fn(sent1, sent1_dates)
        sent2: GaussOutput = self.encode_fn(sent2, sent2_dates)

        return asymmetrical_kl_sim(sent1.mu, sent1.std, sent2.mu, sent2.std)

    @torch.inference_mode()
    def encode_fn(self, sentences: list[str], dates: list[str], **_) -> GaussOutput:
        self.model.eval()

        output: GaussOutput = None

        for batch in self.data_loader(sentences):
            output = self.model.forward(**batch.to(INFERENCE_DEVICE), dates=positional_encoding(dates[:self.batch_size]).to(INFERENCE_DEVICE))
            break

        return output
    
    def evaluate(self) -> dict:
        similarities: list[float] = []
        
        similarities = [i.item() for i in list(self.sim_fn(self.sentences1, self.sentences1_dates, self.sentences2, self.sentences2_dates))]
        
        return {"sent1": self.sentences1, "sent2": self.sentences2, "similarity": similarities, "ground_truth": self.scores}