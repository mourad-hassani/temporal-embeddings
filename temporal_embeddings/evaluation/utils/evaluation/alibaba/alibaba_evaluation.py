from typing import Dict, List
from pathlib import Path
import json

from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

from temporal_embeddings.utils.os.folder_management import create_folders

DATA_FILE_PATH: Path = Path("data/evaluation/time_sensitive_qa/processed_human_annotated_test.json")

def evaluate_alibaba() -> None:
    model_name = "Alibaba-NLP/gte-Qwen2-7B-instruct"

    model = SentenceTransformer(model_name, trust_remote_code=True)

    model.max_seq_length = 8192

    output_similarities: List[int] = []

    data: List[Dict] = []
    ground_truth: List[int] = []

    with DATA_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        for element in tqdm(data):
            ground_truth.append(element["answer"])

            question: str = element["question"]
            question_emb = model.encode(question, prompt_name="query")

            paragraphs: List[str] = element["paragraphs"]

            similarities: List[float] = []
            
            for paragraph in paragraphs:
                paragraph_emb = model.encode(paragraph)

                scores = (question_emb @ paragraph_emb.T) * 100

                similarities.append(scores.tolist())

            output_similarities.append(similarities.index(max(similarities)))

    similarities_file_path: Path = Path(f"output/similarities/{model_name}/{model_name}_similarities.json")
    create_folders(similarities_file_path.parent)
    
    with similarities_file_path.open("w", encoding="utf-8") as g:
        json.dump(output_similarities, g, indent=4, ensure_ascii=False)

    print(compute_accuracy(ground_truth, output_similarities))

def compute_accuracy(first_list: List[int], second_list: List[int]) -> float:
    first_list, second_list = np.array(first_list), np.array(second_list)

    assert first_list.size == second_list.size

    return sum(first_list == second_list) / first_list.size