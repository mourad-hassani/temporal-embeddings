import argparse
import concurrent.futures

from temporal_embeddings.data_utils.temporal_index.create_index import create_index, NUM_WORKERS, OUTPUT_FOLDER_PATH
from temporal_embeddings.data_utils.temporal_index.merge_dataframes import merge_csv_files

print(NUM_WORKERS)

parser = argparse.ArgumentParser(description="Commnad line program to create the training dataset")

parser.add_argument("-n", "--num_rows", type=int)
parser.add_argument("-s", "--skip", type=int)

args = parser.parse_args()

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = [executor.submit(create_index, index, args.skip, args.num_rows) for index in range(NUM_WORKERS)]

    for future in concurrent.futures.as_completed(futures):
        print(f"Process {future.result()} completed")

merge_csv_files(OUTPUT_FOLDER_PATH)