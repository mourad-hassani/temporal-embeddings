from pathlib import Path

from temporal_embeddings.synthetic_data.create_synthetic_dataset import create_synthetic_dataset

create_synthetic_dataset(output_file_path=Path("data/synthetic_data/synthetic_dataset.json"), size=1000)