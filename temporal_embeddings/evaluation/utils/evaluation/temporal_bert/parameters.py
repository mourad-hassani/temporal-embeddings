from pathlib import Path
import torch

MODEL_NAME: str = "distilbert/distilbert-base-uncased"

BATCH_SIZE: int = 64
SHUFFLE: bool = False
NUM_WORKERS: int = 4
DROP_lAST: bool = True
LR: float = 3e-5
WEIGHT_DECAY: float = 2e-4
EPOCHS: int = 1
NUM_WARMUP_RATIO: float = 0.1
MAX_SEQ_LEN: int = 64
DEVICE: str = "cuda:0"
INFERENCE_DEVICE: str = "cpu"
DTYPE: torch.dtype = torch.float16
SEED: int = 0
TEMPERATURE: float = 0.05
NUM_EVAL_STEPS: int = 1000

INPUT_FILE_PATH: str = Path("data/base_dataset/dataset.csv")
OUTPUT_DIRECTORY_PATH: Path = Path("output")

SPECIAL_TOKENS: bool = False