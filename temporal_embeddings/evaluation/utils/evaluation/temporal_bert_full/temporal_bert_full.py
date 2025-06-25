from pathlib import Path
import json
from typing import List, Dict

from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.inference import Inference
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.parameters import MAX_SEQ_LEN
from temporal_embeddings.utils.os.folder_management import create_folders
from temporal_embeddings.evaluation.utils.evaluation.metrics import compute_accuracy

def evaluate_temporal_bert_full(model_name: str, model_path: str, batch_size: int, max_seq_len: int, dataset_file_path: Path, eval_id: int, top_k: int) -> None:
    SBERT_SIMILARITIES_FILE_PATH: Path = Path(f"output/similarities/temporal_bert_full/{model_name}/{eval_id}_temporal_bert_full_similarities.json")
    create_folders(SBERT_SIMILARITIES_FILE_PATH.parent)
    SIMILARITIES_FILE_PATH: Path = Path(f"output/similarities/temporal_bert_full/{model_name}/{eval_id}_similarities.json")
    create_folders(SIMILARITIES_FILE_PATH.parent)
    GROUND_TRUTH_FILE_PATH: Path = dataset_file_path

    def evaluate_temporal_bert(model_name: str, model_path: str, batch_size: int, max_seq_len: int) -> None:
        similarities_list: List[List[float]] = []

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

                    similarities.append(float(util.cos_sim(question_emb, paragraph_emb)[0].item()))

                output_similarities.append(similarities)

        create_folders(SIMILARITIES_FILE_PATH.parent)
        
        with SIMILARITIES_FILE_PATH.open("w", encoding="utf-8") as g:
            json.dump(output_similarities, g, indent=4, ensure_ascii=False)

    evaluate_model("BAAI/bge-large-en-v1.5")
    evaluate_temporal_bert(model_name, model_path, batch_size, max_seq_len)

    with SBERT_SIMILARITIES_FILE_PATH.open("r", encoding="utf-8") as f1, SIMILARITIES_FILE_PATH.open("r", encoding="utf-8") as f2:
        list1 = json.load(f1)
        list2 = json.load(f2)

    # def rank_list(values: List[float]) -> List[int]:
    #     sorted_indices = sorted(range(len(values)), key=lambda x: values[x], reverse=True)
    #     ranks = [0] * len(values)
    #     for rank, index in enumerate(sorted_indices):
    #         ranks[index] = rank
    #     return ranks

    # list1 = [rank_list(sublist) for sublist in list1]
    # list2 = [rank_list(sublist) for sublist in list2]
    
    merged_list = [[((6*x) + y) for x, y in zip(sublist1, sublist2)] for sublist1, sublist2 in zip(list1, list2)]

    similarities_list: List[List[float]] = merged_list
    ground_truth: List[int] = []

    with open(GROUND_TRUTH_FILE_PATH, "r") as f:
        data: List[dict] = json.load(f)
        for e in data:
            ground_truth.append(e["answer"])

    print(compute_accuracy(ground_truth, similarities_list, top_k))
