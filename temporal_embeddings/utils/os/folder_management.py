import os
import glob
from pathlib import Path

def clear_files(folder: Path) -> None:
    """
    Deletes all files within the specified folder.

    Parameters:
        folder (Path): The path to the folder containing the files to be cleared.

    Returns:
        None: This function does not return any value.
    """

    files = glob.glob(str(folder / Path("*.json")))
    
    for f in files:
        os.remove(f)

    files = glob.glob(str(folder / Path("*.csv")))
    
    for f in files:
        os.remove(f)

def create_folders(path: Path) -> None:
    """
    Creates all the needed folders in the path that are not already created.

    Parameters:
        path (Path): The path where folders need to be created.

    Returns:
        None: This function does not return any value.
    """
    path.mkdir(parents=True, exist_ok=True)