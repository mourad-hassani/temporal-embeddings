import os
import json
from pathlib import Path
from typing import List, Dict
import time

from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import numpy as np
from mistralai import Mistral
from torch import Tensor

from temporal_embeddings.utils.os.folder_management import create_folders
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.parameters import MAX_SEQ_LEN
from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.temporal_bert_evaluation import evaluate_temporal_bert

DATA_FILE_PATH: Path = Path("data/evaluation/time_sensitive_qa/processed_human_annotated_test.json")

def evaluate_mistral() -> None:
    # api_key = os.getenv("MISTRAL_API_KEY")
    api_key: str = "OeZfwmPee7UPF0QCeOXd1Q6g1ea78JIz"

    client: Mistral = Mistral(api_key)

    # embeddings_batch_response = client.embeddings.create(
    #     model="mistral-embed",
    #     inputs=["Embed this sentence.", "As well as this one."],
    # )

    # for emb in embeddings_batch_response.data:
    #     print(emb.embedding)

    output_similarities: List[int] = []

    data: List[Dict] = []
    ground_truth: List[int] = []

    questions: List[str] = []
    paragraphs: List[str] = []

    questions_emb = []
    paragraphs_emb = []

    with DATA_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

        for element in tqdm(data):
            ground_truth.append(element["answer"])
            questions.append(element["question"])
            paragraphs.extend(element["paragraphs"])

        # questions_emb = client.embeddings.create(model="mistral-embed", inputs=questions).data
        for i in range(0, len(questions), 100):
            print(i)
            time.sleep(2)
            batch = questions[i:i + 25]
            batch_emb = client.embeddings.create(model="mistral-embed", inputs=batch).data
            questions_emb.extend(batch_emb)
        # half = len(paragraphs) // 2
        # paragraphs_emb = client.embeddings.create(model="mistral-embed", inputs=paragraphs).data
        batch_size = 25
        for i in range(0, len(paragraphs), batch_size):
            print(i)
            time.sleep(2)
            batch = paragraphs[i:i + batch_size]
            batch_emb = client.embeddings.create(model="mistral-embed", inputs=batch).data
            paragraphs_emb.extend(batch_emb)

        for element in tqdm(data):
            similarities: List[float] = []

            question_index = questions.index(element["question"])
            question_emb = Tensor(questions_emb[question_index].embedding)
            
            for paragraph in element["paragraphs"]:
                paragraph_index = paragraphs.index(paragraph)
                paragraph_emb = Tensor(paragraphs_emb[paragraph_index].embedding)

                similarities.append(util.cos_sim(question_emb, paragraph_emb)[0])

            output_similarities.append(similarities.index(max(similarities)))

    similarities_file_path: Path = Path(f"output/similarities/mistral/mistral_similarities.json")
    create_folders(similarities_file_path.parent)
    
    with similarities_file_path.open("w", encoding="utf-8") as g:
        json.dump(output_similarities, g, indent=4, ensure_ascii=False)

    print(compute_accuracy(ground_truth, output_similarities))

def compute_accuracy(first_list: List[int], second_list: List[int]) -> float:
    first_list, second_list = np.array(first_list), np.array(second_list)

    assert first_list.size == second_list.size

    return sum(first_list == second_list) / first_list.size