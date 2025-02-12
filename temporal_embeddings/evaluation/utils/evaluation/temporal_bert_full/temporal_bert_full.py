from pathlib import Path
import json
from typing import List, Dict

import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.inference import Inference
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.parameters import MAX_SEQ_LEN
from temporal_embeddings.utils.os.folder_management import create_folders

SBERT_SIMILARITIES_FILE_PATH: Path = Path("output/similarities/temporal_bert_full/temporal_bert_full_similarities.json")
SIMILARITIES_FILE_PATH: Path = Path("output/similarities/temporal_bert_full/similarities.json")
GROUND_TRUTH_FILE_PATH: Path = Path("data/evaluation/time_sensitive_qa/processed_human_annotated_test.json")

def evaluate_temporal_bert_full() -> None:
    evaluate_model("all-mpnet-base-v2")
    evaluate_temporal_bert()

    with SBERT_SIMILARITIES_FILE_PATH.open("r", encoding="utf-8") as f1, SIMILARITIES_FILE_PATH.open("r", encoding="utf-8") as f2:
        list1 = json.load(f1)
        list2 = json.load(f2)

    merged_list = [[(x + y) / 2 for x, y in zip(sublist1, sublist2)] for sublist1, sublist2 in zip(list1, list2)]

    similarities_list: List[int] = [sublist.index(max(sublist)) for sublist in merged_list]

    ground_truth: List[int] = []

    with open(GROUND_TRUTH_FILE_PATH, "r") as f:
        data: List[dict] = json.load(f)

        for e in data:
            ground_truth.append(e["answer"])

    print(compute_accuracy(ground_truth, similarities_list))

def evaluate_temporal_bert() -> None:
    similarities_list: List[List[float]] = []

    reference_date: str = "09 august 2024"

    with GROUND_TRUTH_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        inference: Inference = Inference()

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

    create_folders(SBERT_SIMILARITIES_FILE_PATH.parent)
    with SBERT_SIMILARITIES_FILE_PATH.open("w", encoding="utf-8") as g:
        json.dump(similarities_list, g, indent=4, ensure_ascii=False)

def evaluate_model(model_name: str) -> None:
    model: SentenceTransformer = SentenceTransformer(model_name)
    model.max_seq_length = MAX_SEQ_LEN

    output_similarities: List[List[float]] = []

    data: List[Dict] = []
    ground_truth: List[int] = []

    with GROUND_TRUTH_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        for element in tqdm(data):
            ground_truth.append(element["answer"])

            question: str = element["question"]
            question_emb = model.encode(question, convert_to_tensor=True)

            paragraphs: List[str] = element["paragraphs"]

            similarities: List[float] = []
            
            for paragraph in paragraphs:
                paragraph_emb = model.encode(paragraph, convert_to_tensor=True)

                print(util.cos_sim(question_emb, paragraph_emb)[0])
                similarities.append(util.cos_sim(question_emb, paragraph_emb)[0].tolist())

            output_similarities.append(similarities)

    create_folders(SIMILARITIES_FILE_PATH.parent)
    
    with SIMILARITIES_FILE_PATH.open("w", encoding="utf-8") as g:
        json.dump(output_similarities, g, indent=4, ensure_ascii=False)

def compute_accuracy(first_list: List[int], second_list: List[int]) -> float:
    first_list, second_list = np.array(first_list), np.array(second_list)

    assert first_list.size == second_list.size

    return sum(first_list == second_list) / first_list.size