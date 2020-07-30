import json
from pathlib import Path
import zipfile
import tarfile

def load_wordlist(file_path: str) -> list:
    """Loads words list from a text file
    
    Args:
        file_path: path to wordslist file
    
    Returns:
        list: list of loaded words
    """
    wordslist = []
    with open(file_path, "r", errors="ignore") as file:
        for line in file:
            for word in line.split():
                wordslist.append(word)
    return wordslist