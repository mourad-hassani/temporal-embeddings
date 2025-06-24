from typing import Dict, List
from pathlib import Path
import json

from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

from temporal_embeddings.utils.os.folder_management import create_folders
from temporal_embeddings.evaluation.utils.evaluation.metrics import compute_accuracy

def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery: {query}'

def evaluate_salesforce(dataset_file_path: Path, eval_id: int, top_k: int) -> None:
    GROUND_TRUTH_FILE_PATH: Path = dataset_file_path
    model_name = "Salesforce/SFR-Embedding-Mistral"
    SIMILARITIES_FILE_PATH: Path = Path(f"output/similarities/salesforce/{model_name}/{eval_id}_similarities.json")
    create_folders(SIMILARITIES_FILE_PATH.parent)

    task = 'Given a question with temporal constraints, retrieve relevant passages that answer the question with the correct temporal information.'

    model = SentenceTransformer(model_name, trust_remote_code=True)

    output_similarities: List[int] = []
    similarities_list: List[List[float]] = []

    data: List[Dict] = []
    ground_truth: List[int] = []

    print(f"Evaluating model: {model_name}")
    print(f"Dataset file path: {GROUND_TRUTH_FILE_PATH}")
    with GROUND_TRUTH_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        for element in tqdm(data):
            ground_truth.append(element["answer"])

            question: str = get_detailed_instruct(task, element["question"])

            paragraphs: List[str] = element["paragraphs"]

            batch_size = 8
            embeddings = []
            for i in range(0, len(paragraphs), batch_size):
                batch = paragraphs[i:i + batch_size]
                if i == 0:
                    batch = [question] + batch
                batch_embeddings = model.encode(batch)
                embeddings.extend(batch_embeddings)

            similarities: List[float] = []
            
            for i, _ in enumerate(paragraphs):
                scores = util.cos_sim(embeddings[0], embeddings[i+1])
                similarities.append(scores.tolist()[0][0])

            similarities_list.append(similarities)
            output_similarities.append(similarities.index(max(similarities)))
    
    with SIMILARITIES_FILE_PATH.open("w", encoding="utf-8") as g:
        json.dump(similarities_list, g, indent=4, ensure_ascii=False)

    print(compute_accuracy(ground_truth, similarities_list, top_k))