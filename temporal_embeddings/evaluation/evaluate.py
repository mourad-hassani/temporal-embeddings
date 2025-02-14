import json
from pathlib import Path
from typing import List, Dict

from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import numpy as np

from temporal_embeddings.utils.os.folder_management import create_folders
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.parameters import MAX_SEQ_LEN
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.temporal_bert_evaluation import evaluate_temporal_bert
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert_full.temporal_bert_full import evaluate_temporal_bert_full
from temporal_embeddings.evaluation.utils.evaluation.mistral.mistral_evaluation import evaluate_mistral
from temporal_embeddings.evaluation.utils.evaluation.alibaba.alibaba_evaluation import evaluate_alibaba

DATA_FILE_PATH: Path = Path("data/evaluation/time_sensitive_qa/processed_human_annotated_test.json")

def evaluate_model(model_name: str) -> None:
    if model_name == "temporal_bert":
        evaluate_temporal_bert()
        return
    
    if model_name == "temporal_bert_full":
        evaluate_temporal_bert_full()
        return
    
    if model_name == "mistral":
        evaluate_mistral()
        return
    
    if model_name == "alibaba":
        evaluate_alibaba()
        return

    model: SentenceTransformer = SentenceTransformer(model_name)
    model.max_seq_length = MAX_SEQ_LEN

    output_similarities: List[int] = []

    data: List[Dict] = []
    ground_truth: List[int] = []

    with DATA_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        for element in tqdm(data):
            ground_truth.append(element["answer"])

            question: str = element["question"]
            question_emb = model.encode(question, convert_to_tensor=True) if model_name != "BAAI/bge-large-en" else model.encode(question, convert_to_tensor=True, normalize_embeddings=True)

            paragraphs: List[str] = element["paragraphs"]

            similarities: List[float] = []
            
            for paragraph in paragraphs:
                paragraph_emb = model.encode(paragraph, convert_to_tensor=True) if model_name != "BAAI/bge-large-en" else model.encode(paragraph, convert_to_tensor=True, normalize_embeddings=True)

                similarities.append(util.cos_sim(question_emb, paragraph_emb)[0])

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