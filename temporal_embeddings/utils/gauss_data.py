from pathlib import Path
import pandas as pd
import torch
from torch.utils.data import DataLoader
from transformers.tokenization_utils import BatchEncoding, PreTrainedTokenizer

from temporal_embeddings.parameters.parameters import INPUT_FILE_PATH, SHUFFLE, BATCH_SIZE, NUM_WORKERS, DROP_lAST, MAX_SEQ_LEN, SPECIAL_TOKENS

class GaussData:
    def __init__(self, file_path: Path, tokenizer: PreTrainedTokenizer):
        self.tokenizer: PreTrainedTokenizer = tokenizer

        # self.dataset is of the form : [{"sent0": "...", "sent1": "...", "score": ...}]
        self.dataset = pd.read_csv(str(file_path)).to_dict("records")[:1000000]
        self.dataset_length = len(self.dataset)

        self.train_dataset = self.dataset[:int(0.9 * self.dataset_length)]
        self.val_dataset = self.dataset[int(0.9 * self.dataset_length):int(0.95 * self.dataset_length)]
        self.test_dataset = self.dataset[int(0.95 * self.dataset_length):]

        self.train_dataloader = DataLoader(self.train_dataset, collate_fn=self.collate_fn, batch_size=BATCH_SIZE, shuffle=SHUFFLE, num_workers=NUM_WORKERS, pin_memory=True, drop_last=DROP_lAST)
        self.val_dataloader = DataLoader(self.val_dataset, collate_fn=self.collate_fn, batch_size=BATCH_SIZE, shuffle=SHUFFLE, num_workers=NUM_WORKERS, pin_memory=True, drop_last=DROP_lAST)
        self.test_dataloader = DataLoader(self.test_dataset, collate_fn=self.collate_fn, batch_size=BATCH_SIZE, shuffle=SHUFFLE, num_workers=NUM_WORKERS, pin_memory=True, drop_last=DROP_lAST)
    
    def tokenize(self, batch: list[str]) -> BatchEncoding:
        return self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=MAX_SEQ_LEN, add_special_tokens=SPECIAL_TOKENS)
    
    def collate_fn(self, data_list: list[dict]) -> BatchEncoding:
        """
        Merges a list of samples to form a mini-batch of Tensor(s). Used when using batched loading from a map-style dataset.
        """

        return BatchEncoding(
            {
                "sent0": self.tokenize([d["sent0"] for d in data_list]),
                "sent1": self.tokenize([d["sent1"] for d in data_list]),
                "score": torch.FloatTensor([float(d["score"]) for d in data_list]),
            }
        )
    
    def get_train_dataloader(self) -> DataLoader:
        return self.train_dataloader
    
    def get_val_dataloader(self) -> DataLoader:
        return self.val_dataloader
    
    def get_test_dataloader(self) -> DataLoader:
        return self.test_dataloader