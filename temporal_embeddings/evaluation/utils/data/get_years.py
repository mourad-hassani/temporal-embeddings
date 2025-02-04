import json
from tqdm import tqdm
import re
from typing import Dict, List

from temporal_embeddings.evaluation.utils.data.shared import TIME_SENSITIVE_QA_PATH


def find_years(text: str) -> list[str]:
    pattern = r' \d{4} '
    
    years = re.findall(pattern, text)
    
    return years

def get_years() -> list[int]:
    years_dict: Dict = {}

    with open(TIME_SENSITIVE_QA_PATH / "human_annotated_test.json", "r") as f:
        data: List[Dict] = json.load(f)

        for d in tqdm(data):
            paras: List[str] = []

            for q in d["questions"]:
                paras.append(q[0])

            for para in paras:
                extracted_years: List[str] = find_years(para)
                for extracted_year in extracted_years:
                    if int(extracted_year) in years_dict:
                        years_dict[int(extracted_year)] += 1
                    else:
                        years_dict[int(extracted_year)] = 1

    return dict(sorted(years_dict.items()))