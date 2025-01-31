from pathlib import Path
from typing import List
import os

from tqdm import tqdm
from datatrove.pipeline.readers import ParquetReader
from stanza.server import CoreNLPClient
import pandas as pd

from temporal_embeddings.data_utils.utils.stanza.temporal_expressions import contains_temporal_expression
from temporal_embeddings.data_utils.utils.text.get_sentences import split_into_sentences
from temporal_embeddings.data_utils.temporal_index.utils.expressions import add_expression
from temporal_embeddings.utils.os.folder_management import clear_files

OUTPUT_FOLDER_PATH : Path = Path("./data/fineweb/index")

NUM_WORKERS : int = min(10, os.cpu_count())

clients : List[CoreNLPClient] = [CoreNLPClient(endpoint="http://localhost:"+str(60000+i), annotators=['tokenize', 'ner'], be_quiet=True) for i in range(NUM_WORKERS)]

clear_files(OUTPUT_FOLDER_PATH)

def create_index(index : int, skip : int, num_rows : int) -> int:
    """
    Creates the index where we store the temporal expressions and the IDs of sentences.

    Parameters:
        num_rows (int): The number of rows to load from the fineweb database.

    Returns:
        None: This function does not return any value.
    """

    client : CoreNLPClient = clients[index % NUM_WORKERS]

    output_dataframe : pd.DataFrame = pd.DataFrame(columns=["sentences", "expressions", "values", "current_dates"])
    
    avg : int = num_rows // NUM_WORKERS
    remainder : int = num_rows % NUM_WORKERS

    items_to_skip : int = 0
    
    for i in range(index):
        items_to_skip += avg + (1 if i < remainder else 0)
    
    data_reader = ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data", skip=(skip + items_to_skip), limit=(avg + (1 if index < remainder else 0)), doc_progress=True, file_progress=True)

    for document in tqdm(data_reader()):
        for sent in split_into_sentences(document.text):
            contains_temporal_expression_bool, extracted_temporal_expressions = contains_temporal_expression(sent, client)
            
            if contains_temporal_expression_bool:
                found_expressions : List = [e for e in extracted_temporal_expressions]

                for temporal_expression in found_expressions:
                    expression_value : str = temporal_expression.value if temporal_expression.value else temporal_expression.altValue
                    
                    output_dataframe = add_expression(temporal_sentences=output_dataframe, expression=temporal_expression.text, sentence=sent, value=expression_value)

    output_dataframe = output_dataframe.sort_index()
    
    output_dataframe.to_csv(OUTPUT_FOLDER_PATH / Path(f"{index}.csv"), index=True)

    return index