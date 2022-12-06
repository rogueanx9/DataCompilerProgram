import os
from glob import iglob
from typing import Any, List

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[Warning] You cannot input empty string!")
        path = input(msg)
    return os.path.abspath(path)

def Relpath(msg: str) -> str:
    path = input(msg)
    return os.path.relpath(path) if path else ""

def IsExt(path: str, ext: str) -> bool:
    # print(os.path.splitext(path)[1].lower())
    return ext.lower() in os.path.splitext(path)[1].lower()

def IsExts(path: str, exts: List[str]) -> bool:
    for ext in exts:
        return IsExt(path, ext)
    return False

def Files(path: str, ext = "", recursive = False) -> List[str]:
    rec = "**" if recursive else "*"
    return [_ for _ in iglob(os.path.join(path, rec), recursive=recursive) if os.path.isfile(_) and IsExt(_, ext)]

def Folders(path: str, recursive = False) -> List[str]:
    rec = "**" if recursive else "*"
    return [_ for _ in iglob(os.path.join(path, rec), recursive=recursive) if os.path.isdir(_)]

def KeysIn(text: str, *keys: str) -> bool:
    for key in keys:
        if key.lower() in text.lower():
            return True
    return False

def IsFloat(num: Any):
    try:
        float(num)
    except:
        return False
    return True

def IsInt(num: Any):
    try:
        int(num)
    except:
        return False
    return True

def SplitPath(path: str, n: int):
    for i in range(n):
        path = os.path.split(path)[0]
    return path