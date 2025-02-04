import torch
from torch.utils.data import DataLoader
from transformers.tokenization_utils import BatchEncoding, PreTrainedTokenizer
from transformers import AutoTokenizer
from typing import List, Dict

from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.gauss_model import GaussModel, GaussOutput
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.parameters import MODEL_NAME, INFERENCE_DEVICE, BATCH_SIZE, NUM_WORKERS, MAX_SEQ_LEN, SPECIAL_TOKENS
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.similarity import asymmetrical_kl_sim

class Inference:
    def __init__(self):
        self.model = GaussModel(MODEL_NAME, True).eval().to(INFERENCE_DEVICE)
        self.model.load_state_dict(torch.load('models/temporal_bert/temporal_bert.pth', map_location=torch.device(INFERENCE_DEVICE)))

        self.tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, model_max_length = MAX_SEQ_LEN, use_fast = False)

        self.cached_embeddings: Dict = {}

    def set_sentences(self, sentences1: List[str], sentences2: List[str], scores: list[float]):
        self.sentences1, self.sentences2, self.scores = sentences1, sentences2, scores

    def tokenize(self, batch: list[str]) -> BatchEncoding:
        return self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=MAX_SEQ_LEN, add_special_tokens=SPECIAL_TOKENS)
    
    def data_loader(self, sentences: list[str]):
        return DataLoader(sentences, collate_fn=self.tokenize, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True, drop_last=False)

    def sim_fn(self, sent1: list[str], sent2: list[str]) -> float:
        sent1: GaussOutput = self.encode_fn(sent1)
        sent2: GaussOutput = self.encode_fn(sent2)

        return asymmetrical_kl_sim(sent1.mu, sent1.std, sent2.mu, sent2.std)

    @torch.inference_mode()
    def encode_fn(self, sentences: list[str], **_) -> GaussOutput:
        self.model.eval()

        output: GaussOutput = None

        for batch in self.data_loader(sentences):
            output = self.model.forward(**batch.to(INFERENCE_DEVICE))
            break

        return output
    
    def evaluate(self) -> dict:
        similarities: list[float] = []
        
        similarities = [i.item() for i in list(self.sim_fn(self.sentences1, self.sentences2))]
        
        return {"sent1": self.sentences1, "sent2": self.sentences2, "similarity": similarities, "ground_truth": self.scores}