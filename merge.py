from pathlib import Path

from temporal_embeddings.data_utils.temporal_index.merge_dataframes import merge_csv_files

INPUT_FOLDER_PATH : Path = Path("./data/fineweb/test")

merge_csv_files(INPUT_FOLDER_PATH)