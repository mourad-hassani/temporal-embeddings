import concurrent.futures
import os

from stanza.server import CoreNLPClient
from datatrove.pipeline.readers import ParquetReader

from temporal_embeddings.data_utils.utils.stanza.temporal_expressions import contains_temporal_expression
from temporal_embeddings.data_utils.utils.text.get_sentences import split_into_sentences
from temporal_embeddings.data_utils.temporal_index.utils.expressions import accept_expression, add_expression

def process_item(item):
    return item

def parallel_for_loop(data):
    max_threads = os.cpu_count()
    print(f"Max threads: {max_threads}")
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        results = list(executor.map(process_item, data))
    return results

def run() -> None:
    data = range(1000000)
    results = parallel_for_loop(data)
    print(results)