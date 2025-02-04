import os
import pandas as pd
import ast
from pathlib import Path

from tqdm import tqdm

def merge_csv_files(folder_path: Path) -> None:
    merged_df = pd.DataFrame()

    for file_name in tqdm(os.listdir(folder_path)):
        if file_name.endswith(".csv"):
            file_path: Path = folder_path / Path(file_name)

            df = pd.read_csv(file_path, index_col=0)

            for col in df.columns:
                df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            
            if merged_df.empty:
                merged_df = df
            
            else:
                for idx in df.index:
                    if idx in merged_df.index:
                        for col in df.columns:
                            merged_df.at[idx, col] = merged_df.at[idx, col] + df.at[idx, col]
                    
                    else:
                        merged_df.loc[idx] = df.loc[idx]

    if not os.path.exists(folder_path / Path("dataset")):
        os.makedirs(folder_path / Path("dataset"))

    merged_df.sort_index()

    merged_df.to_csv(folder_path / Path("dataset/dataset.csv"))
    merged_df.to_json(folder_path / Path("dataset/dataset.json"), orient="index", force_ascii=False, indent=4)