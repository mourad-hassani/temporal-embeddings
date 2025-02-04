from pathlib import Path
from typing import Dict
import json
import math
import os
import glob

from tqdm import tqdm
from datatrove.pipeline.readers import ParquetReader
from stanza.server import CoreNLPClient

from temporal_embeddings.data_utils.utils.stanza.temporal_expressions import contains_temporal_expression
from temporal_embeddings.data_utils.utils.text.get_sentences import split_into_sentences
from temporal_embeddings.data_utils.utils.dates.is_date import is_date
from temporal_embeddings.data_utils.utils.intervals.is_interval import is_interval
from temporal_embeddings.data_utils.utils.offsets.is_offset import is_offset
from temporal_embeddings.data_utils.utils.periods.is_period import is_period
from temporal_embeddings.data_utils.utils.refs.is_ref import is_ref

OUTPUT_PATH: Path = Path("data/fineweb")

BATCH_SIZE: int = 10000

def accept_expression(expression: str) -> bool:
    return (is_date(expression) or is_interval(expression) or is_offset(expression) or is_period(expression) or is_ref(expression))

def add_expression(temporal_sentences: Dict, expression: str, sentence: str, text: str, type: str) -> Dict:
    if expression in temporal_sentences:
        temporal_sentences[expression].append({"sent": sentence, "text": text, "type": type})
    
    else:
        temporal_sentences[expression] = [{"sent": sentence, "text": text, "type": type}]
        temporal_sentences = dict(sorted(temporal_sentences.items()))
    
    return temporal_sentences

def process_data_dict(num_rows: int = 20000) -> None:
    files = glob.glob(str(OUTPUT_PATH / Path("*.json")))
    for f in files:
        os.remove(f)

    client = CoreNLPClient(annotators=['tokenize', 'ner'], be_quiet=True)

    ceil: int = math.ceil(num_rows / BATCH_SIZE)

    for i in range(ceil):
        limit: int = BATCH_SIZE if i < (ceil - 1) else (num_rows - (BATCH_SIZE * i))

        temporal_sentences: Dict = {}

        data_reader = ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data", skip=(BATCH_SIZE * i), limit=limit, doc_progress=True, file_progress=True)

        for document in tqdm(data_reader()):
            for sent in split_into_sentences(document.text):
                contains_temporal_expression_bool, extracted_temporal_expressions = contains_temporal_expression(sent, client)
                if contains_temporal_expression_bool:
                    for temporal_expression in [e for e in extracted_temporal_expressions if (str(e.value).strip() != "" and accept_expression(e.value) and e.type != "SET")]:
                        temporal_sentences = add_expression(temporal_sentences=temporal_sentences, expression=temporal_expression.value, sentence=sent, text=temporal_expression.text, type=temporal_expression.type)

        OUTPUT_FILE_PATH: Path = OUTPUT_PATH / Path(f"{BATCH_SIZE * i}-{(BATCH_SIZE * i) + limit}.json")
        with OUTPUT_FILE_PATH.open("w") as f:
            print("Writing to " + str(OUTPUT_FILE_PATH))
            json.dump(temporal_sentences, f, ensure_ascii=False, indent=4)