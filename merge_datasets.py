import argparse

from temporal_embeddings.data_utils.temporal_index.merge_dataframes import merge_csv_files

def parse_args():
    parser = argparse.ArgumentParser(description="Merge CSV files in a folder")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing CSV files")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    merge_csv_files(args.folder_path)