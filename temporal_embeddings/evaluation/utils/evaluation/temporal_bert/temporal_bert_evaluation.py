from pathlib import Path
import json
from typing import List

import numpy as np
from tqdm import tqdm

from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.inference import Inference
from temporal_embeddings.utils.os.folder_management import create_folders

def evaluate_temporal_bert(model_name: str, model_path: str, batch_size: int, max_seq_len: int, dataset_file_path: Path, eval_id: int, top_k: int) -> None:
    GROUND_TRUTH_FILE_PATH: Path = dataset_file_path
    SBERT_SIMILARITIES_FILE_PATH: Path = Path(f"output/similarities/temporal_bert/{model_name}/{eval_id}_temporal_bert_similarities.json")
    create_folders(SBERT_SIMILARITIES_FILE_PATH.parent)

    similarities_list: List[List[int]] = []

    reference_date: str = "09 august 2024"

    with GROUND_TRUTH_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        inference: Inference = Inference(model_name=model_name, model_path=model_path, batch_size=batch_size, max_seq_len=max_seq_len)

        for element in tqdm(data):
            question: str = element["question"]

            second_sentences: List[str] = element["paragraphs"]
            first_sentences: List[str] = [question] * len(second_sentences)
            reference_dates: List[str] = [reference_date] * len(second_sentences)
            ground_truth: List[float] = [0.0] * len(second_sentences)

            inference.set_sentences(first_sentences, reference_dates, second_sentences, reference_dates, ground_truth)

            similarities: List[float] = None

            output = inference.evaluate()

            similarities = output["similarity"]

            similarities_list.append(similarities)

    with SBERT_SIMILARITIES_FILE_PATH.open("w", encoding="utf-8") as g:
        json.dump(similarities_list, g, indent=4, ensure_ascii=False)

    ground_truth: List[int] = []

    with open(GROUND_TRUTH_FILE_PATH, "r") as f:
        data: List[dict] = json.load(f)

        for e in data:
            ground_truth.append(e["answer"])

    print(compute_accuracy(ground_truth, similarities_list, top_k))

def compute_accuracy(first_list: List[int], second_list: List[List[int]], top_k: int) -> float:
    correct = 0
    for gt_idx, sim_scores in zip(first_list, second_list):
        top_k_indices = np.argsort(sim_scores)[-top_k:][::-1]
        if gt_idx in top_k_indices:
            correct += 1
    return correct / len(first_list) if first_list else 0.0