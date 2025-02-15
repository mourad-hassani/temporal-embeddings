from typing import Dict, List
from pathlib import Path
import json

from sentence_transformers import SentenceTransformer, util
import numpy as np
from tqdm import tqdm

from temporal_embeddings.utils.os.folder_management import create_folders

DATA_FILE_PATH: Path = Path("data/evaluation/time_sensitive_qa/processed_human_annotated_test.json")

def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery: {query}'

def evaluate_salesforce() -> None:
    model_name = "Salesforce/SFR-Embedding-Mistral"

    task = 'Given a question with temporal constraints, retrieve relevant passages that answer the question with the correct temporal information.'

    model = SentenceTransformer(model_name, trust_remote_code=True)

    output_similarities: List[int] = []

    data: List[Dict] = []
    ground_truth: List[int] = []

    with DATA_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        for element in tqdm(data):
            ground_truth.append(element["answer"])

            question: str = get_detailed_instruct(task, element["question"])

            paragraphs: List[str] = element["paragraphs"]

            embeddings = model.encode([question] + paragraphs)

            similarities: List[float] = []
            
            for i, _ in enumerate(paragraphs):
                scores = util.cos_sim(embeddings[0], embeddings[i+1])

                similarities.append(scores.tolist()[0][0])

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