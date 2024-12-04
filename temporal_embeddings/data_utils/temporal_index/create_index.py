from pathlib import Path
from typing import Dict, List
import json
import math

from tqdm import tqdm
from datatrove.pipeline.readers import ParquetReader
from stanza.server import CoreNLPClient

from temporal_embeddings.data_utils.utils.stanza.temporal_expressions import contains_temporal_expression
from temporal_embeddings.data_utils.utils.text.get_sentences import split_into_sentences
from temporal_embeddings.data_utils.temporal_index.utils.expressions import accept_expression, add_expression
from temporal_embeddings.utils.os.folder_management import clear_json_files

OUTPUT_PATH : Path = Path("data/fineweb")

BATCH_SIZE : int = 5
NUM_ROWS : int = 4

def create_index(num_rows : int = NUM_ROWS) -> None:
    """
    Creates the index where we store the temporal expressions and the IDs of sentences.

    Parameters:
        num_rows (int): The number of rows to load from the fineweb database.

    Returns:
        None: This function does not return any value.
    """

    clear_json_files(OUTPUT_PATH / Path("sentences"))
    clear_json_files(OUTPUT_PATH / Path("index"))

    client = CoreNLPClient(annotators=['tokenize', 'ner'], be_quiet=True)

    ceil : int = math.ceil(num_rows / BATCH_SIZE)

    sentence_counter : int = 0

    sentences : list = []

    for i in range(ceil):
        limit : int = BATCH_SIZE if i < (ceil - 1) else (num_rows - (BATCH_SIZE * i))

        temporal_sentences : Dict = {}

        data_reader = ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data", skip=(BATCH_SIZE * i), limit=limit, doc_progress=True, file_progress=True)

        for document in tqdm(data_reader()):
            for sent in split_into_sentences(document.text):
                contains_temporal_expression_bool, extracted_temporal_expressions = contains_temporal_expression(sent, client)
                
                if contains_temporal_expression_bool:
                    found_expressions : List = [e for e in extracted_temporal_expressions if (str(e.value).strip() != "" and accept_expression(e.value if e.value else e.altValue) and e.type != "SET" and e.type != "TIME")]

                    for temporal_expression in found_expressions:
                        expression_value : str = temporal_expression.value if temporal_expression.value else temporal_expression.altValue
                        
                        temporal_sentences = add_expression(temporal_sentences=temporal_sentences, expression=temporal_expression.text, sentence_id=sentence_counter, value=expression_value)

                    if len(found_expressions) > 0:
                        sentences.append(sent)

                        sentence_counter += 1

        OUTPUT_FILE_PATH : Path = OUTPUT_PATH / Path(f"index/{BATCH_SIZE * i}-{(BATCH_SIZE * i) + limit}.json")
        
        with OUTPUT_FILE_PATH.open("w") as f:
            print("Writing to " + str(OUTPUT_FILE_PATH))
            
            json.dump(temporal_sentences, f, ensure_ascii=False, indent=4)

    OUTPUT_SENTENCES_FILE_PATH : Path = OUTPUT_PATH / Path("sentences/sentences.json")

    with OUTPUT_SENTENCES_FILE_PATH.open("w") as f:
        print("Writing to: " + str(OUTPUT_SENTENCES_FILE_PATH))

        json.dump(sentences, f, ensure_ascii=False, indent=4)