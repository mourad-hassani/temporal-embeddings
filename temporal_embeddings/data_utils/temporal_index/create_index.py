from pathlib import Path
from typing import List

from tqdm import tqdm
from datatrove.pipeline.readers import ParquetReader
from stanza.server import CoreNLPClient
import pandas as pd

from temporal_embeddings.data_utils.utils.stanza.temporal_expressions import contains_temporal_expression
from temporal_embeddings.data_utils.utils.text.get_sentences import split_into_sentences
from temporal_embeddings.data_utils.temporal_index.utils.expressions import accept_expression, add_expression
from temporal_embeddings.utils.os.folder_management import clear_json_files

OUTPUT_PATH : Path = Path("data/fineweb")

NUM_ROWS : int = 1000

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

    output_dataframe : pd.DataFrame = pd.DataFrame(columns=["sentences", "expressions", "values", "current_dates"])

    data_reader = ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data", limit=num_rows, doc_progress=True, file_progress=True)

    for document in tqdm(data_reader()):
        for sent in split_into_sentences(document.text):
            contains_temporal_expression_bool, extracted_temporal_expressions = contains_temporal_expression(sent, client)
            
            if contains_temporal_expression_bool:
                found_expressions : List = [e for e in extracted_temporal_expressions if (str(e.value).strip() != "" and accept_expression(e.value if e.value else e.altValue) and e.type != "SET" and e.type != "TIME")]

                for temporal_expression in found_expressions:
                    expression_value : str = temporal_expression.value if temporal_expression.value else temporal_expression.altValue
                    
                    output_dataframe = add_expression(temporal_sentences=output_dataframe, expression=temporal_expression.text, sentence=sent, value=expression_value)

    output_dataframe = output_dataframe.sort_index()
    
    output_dataframe.to_csv(OUTPUT_PATH / Path("index/index.csv"), index=True)