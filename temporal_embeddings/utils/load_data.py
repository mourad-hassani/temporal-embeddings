import csv
from pathlib import Path
import pandas as pd
from temporal_embeddings.parameters.parameters import INPUT_FILE_PATH

def load_data(file_path: Path = INPUT_FILE_PATH, split: str = "train") -> list[list[str]]:
    first_sentences: list[str] = []
    second_sentences: list[str] = []
    scores: list[float] = []
    
    row_count = 0
    
    with file_path.open("r") as f:
        count_reader = csv.reader(f)
        
        for row in count_reader:
            row_count += 1
    
    with file_path.open("r") as f:
        if split == "train":
            start_index = 0
            end_index = int(row_count * 0.9)
        
        elif split == "dev":
            start_index = int(row_count * 0.9) + 1
            end_index = int(row_count * 0.91)
        
        elif split == "test":
            start_index = int(row_count * 0.91) + 1
            end_index = int(row_count)
        
        idx: int = 0
        reader = csv.reader(f)
        
        for row in reader:
            if start_index <= idx <= end_index:
                first_sentences.append(row[0])
                second_sentences.append(row[1])
                scores.append(row[2])
            
            idx += 1
    
    return [first_sentences, second_sentences, scores]