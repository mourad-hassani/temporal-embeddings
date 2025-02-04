from pathlib import Path
import json
from typing import List

import numpy as np
from tqdm import tqdm

from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.inference import Inference

SBERT_SIMILARITIES_FILE_PATH: Path = Path("output/similarities/temporal_bert/temporal_bert_similarities.json")
GROUND_TRUTH_FILE_PATH: Path = Path("data/evaluation/time_sensitive_qa/processed_human_annotated_test.json")

def evaluate_temporal_bert() -> None:
    similarities_list: List[int] = []

    with GROUND_TRUTH_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        inference: Inference = Inference()

        for element in tqdm(data):
            question: str = element["question"]
            question = f"[CLS] {question} [SEP] 09 august 2024 [SEP]"

            second_sentences: List[str] = [f"[CLS] {p} [SEP] 09 august 2024 [SEP]" for p in element["paragraphs"]]
            first_sentences: List[str] = [question] * len(second_sentences)
            ground_truth: List[float] = [0.0] * len(second_sentences)

            inference.set_sentences(first_sentences, second_sentences, ground_truth)

            similarities: List[float] = None

            output = inference.evaluate()

            similarities = output["similarity"]

            similarities_list.append(similarities.index(max(similarities)))

    with SBERT_SIMILARITIES_FILE_PATH.open("w", encoding="utf-8") as g:
        json.dump(similarities_list, g, indent=4, ensure_ascii=False)

    ground_truth: List[int] = []

    with open(GROUND_TRUTH_FILE_PATH, "r") as f:
        data: List[dict] = json.load(f)

        for e in data:
            ground_truth.append(e["answer"])

    print(compute_accuracy(ground_truth, similarities_list))

def compute_accuracy(first_list: List[int], second_list: List[int]) -> float:
    first_list, second_list = np.array(first_list), np.array(second_list)

    assert first_list.size == second_list.size

    return sum(first_list == second_list) / first_list.size