from pathlib import Path
import pandas as pd

def log_info(data: dict, path: Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        df: pd.DataFrame = pd.read_csv(path)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(path, index=False)
    else:
        pd.DataFrame([data]).to_csv(path, index=False)