import argparse
from pathlib import Path

from temporal_embeddings.synthetic_data.create_synthetic_dataset import create_synthetic_dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a synthetic dataset.")
    parser.add_argument(
        "--output_file_path",
        type=str,
        default="data/synthetic_data/synthetic_dataset.json",
        help="Path to the output synthetic dataset file.",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=400000,
        help="Number of synthetic data samples to generate.",
    )
    args = parser.parse_args()

    create_synthetic_dataset(output_file_path=Path(args.output_file_path), size=args.size)