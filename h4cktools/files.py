import json
from pathlib import Path
import zipfile
import tarfile

def load_list(file_path: str) -> list:
    """Loads list from a text file
    
    Args:
        file_path: path to list file
    
    Returns:
        list: list of loaded words
    """
    wordslist = []
    with open(file_path, "r", errors="ignore") as file:
        for line in file:
            for word in line.split():
                if word and not word.startswith("#"):
                    wordslist.append(word)
    return wordslist