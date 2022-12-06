import os
from glob import iglob
from typing import List

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[W] Absolute path cannot be empty!")
        path = input(msg)
    return os.path.abspath(path)

def Folders(path: str, recursive: bool = False) -> List[str]:
    ast = "**" if recursive else "*"
    return [folder for folder in iglob(os.path.join(path, ast), recursive=recursive)]

def ExpandRelPath(path_dict: dict) -> List[str]:
    rel_paths = []
    for k, v in path_dict.items():
        if isinstance(v, dict):
            rel_paths.extend([os.path.join(k,path) for path in ExpandRelPath(v)])
        else:
            rel_paths.append(os.path.relpath(k))

    return rel_paths