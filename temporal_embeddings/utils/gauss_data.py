from pathlib import Path
import pandas as pd
import torch
from torch.utils.data import DataLoader
from transformers.tokenization_utils import BatchEncoding, PreTrainedTokenizer

from temporal_embeddings.parameters.parameters import SHUFFLE, BATCH_SIZE, NUM_WORKERS, DROP_lAST, MAX_SEQ_LEN, SPECIAL_TOKENS
from temporal_embeddings.utils.positional_encoding import positional_encoding

class GaussData:
    def __init__(self, file_path: Path, tokenizer: PreTrainedTokenizer, data_fraction: float = 1.0) -> None:
        self.tokenizer: PreTrainedTokenizer = tokenizer

        # self.dataset is of the form : [{"sent0": "...", "sent1": "...", "score": ...}]
        self.dataset = pd.read_csv(str(file_path), verbose=True)
        self.dataset = self.dataset[
            self.dataset["sent0"].str.split().str.len().lt(100) & 
            self.dataset["sent1"].str.split().str.len().lt(100)
        ]
        self.dataset = self.datset.to_dict("records")
        
        self.dataset_length = len(self.dataset)
        print("Original dataset length:", self.dataset_length)

        self.dataset = self.dataset[:int(data_fraction * self.dataset_length)]
        self.dataset_length = len(self.dataset)

        print("Dataset length:", self.dataset_length)

        self.train_dataset = self.dataset[:int(0.9 * self.dataset_length)]
        self.val_dataset = self.dataset[int(0.98 * self.dataset_length):int(0.99 * self.dataset_length)]
        self.test_dataset = self.dataset[int(0.99 * self.dataset_length):]

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
                "sent0_date": positional_encoding([d["sent0_date"] for d in data_list]),
                "sent1": self.tokenize([d["sent1"] for d in data_list]),
                "sent1_date": positional_encoding([d["sent1_date"] for d in data_list]),
                "score": torch.FloatTensor([float(d["score"]) for d in data_list]),
            }
        )
    
    def get_train_dataloader(self) -> DataLoader:
        return self.train_dataloader
    
    def get_val_dataloader(self) -> DataLoader:
        return self.val_dataloader
    
    def get_test_dataloader(self) -> DataLoader:
        return self.test_dataloader