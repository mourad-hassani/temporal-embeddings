import json
from tqdm import tqdm
from typing import List

from temporal_embeddings.evaluation.utils.data.shared import TIME_SENSITIVE_QA_PATH

def process_time_sensitive_qa():
    data_list: list[dict] = []

    with open(TIME_SENSITIVE_QA_PATH / "human_annotated_test.json", "r") as f:
        data: List[dict] = json.load(f)

        for d in tqdm(data):
            for q in d["questions"]:
                data_list.append({"question": q[0], "paragraphs": d["paras"], "answer": q[1][0]["para"]})

    with open(TIME_SENSITIVE_QA_PATH / "processed_human_annotated_test.json", "w") as g:
        json.dump(data_list, g, indent=4, ensure_ascii=False)