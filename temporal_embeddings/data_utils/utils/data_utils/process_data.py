from pathlib import Path
from typing import Dict, List
import json
import math

from tqdm import tqdm
from datatrove.pipeline.readers import ParquetReader
from stanza.server import CoreNLPClient

from temporal_embeddings.data_utils.utils.stanza.temporal_expressions import contains_temporal_expression
from temporal_embeddings.data_utils.utils.text.get_sentences import split_into_sentences

OUTPUT_PATH: Path = Path("data/fineweb")

BATCH_SIZE: int = 10

def process_data(num_rows: int = 100) -> None:
  client = CoreNLPClient(annotators=['tokenize', 'ner'], be_quiet=True)

  ceil: int = math.ceil(num_rows / BATCH_SIZE)

  for i in range(ceil):
    limit: int = BATCH_SIZE if i < (ceil - 1) else (num_rows - (BATCH_SIZE * i))
  
    temporal_sentences: List[Dict] = []

    data_reader = ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data", skip=(BATCH_SIZE * i), limit=limit, doc_progress=True, file_progress=True)

    for document in tqdm(data_reader()):
      for sent in split_into_sentences(document.text):
        contains_temporal_expression_bool, extracted_temporal_expressions = contains_temporal_expression(sent, client)
        if contains_temporal_expression_bool:
          temporal_sentences.append({"sent": sent, "expressions": [{"text": e.text, "value": e.value if e.value else e.altValue, "type": e.type} for e in extracted_temporal_expressions if str(e).strip() != ""]})

    OUTPUT_FILE_PATH: Path = OUTPUT_PATH / Path(f"{BATCH_SIZE * i}-{(BATCH_SIZE * i) + limit}.json")
    with OUTPUT_FILE_PATH.open("w") as f:
      json.dump(temporal_sentences, f, ensure_ascii=False, indent=4)