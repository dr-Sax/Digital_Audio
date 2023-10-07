import os
from pathlib import Path

_repo_name = "Digital_Audio"

def get_repo_root():
    return _find_repo_root(Path(__file__))

def _find_repo_root(path: Path):
    if os.path.basename(path) == "":
        raise FileNotFoundError(f"Unable to find the root of the repository. Expected to find \"{_repo_name}\"")
    elif os.path.basename(path) == _repo_name:
        return path
    else:
        return _find_repo_root(path.parent)