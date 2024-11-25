import os
import glob
from pathlib import Path

def clear_json_files(folder : Path) -> None:
    """
    Deletes all `.json` files within the specified folder.

    Parameters:
        folder (Path): The path to the folder containing the files to be cleared.

    Returns:
        None: This function does not return any value.
    """

    files = glob.glob(str(folder / Path("*.json")))
    
    for f in files:
        os.remove(f)