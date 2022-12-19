import os
from glob import iglob
from typing import List

MEDIA_FILES = [".mp4", ".wmv", ".asf", ".bup", ".ifo", ".vob", ".avi", ".mkv", ".mov", ".wav"]

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[W] You cannot input empty path.")
        path = input(msg)
    return os.path.abspath(path)

def ConvertBytes(bytes: float) -> str:
    BYTE_CONV = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    count = 0
    while bytes > 1024:
        bytes /= 1024
        count += 1
    
    return f"{bytes:.2f}{BYTE_CONV[count]}"

def Files(path: str, recursive: bool = False) -> List[str]:
    if not path: 
        print("[W] Path is Empty. Returning empty list")
        return []
    path = RegexHandler(path)
    ast = "**" if recursive else "*"
    return [file for file in iglob(os.path.join(path, ast), recursive=recursive) if os.path.isfile(file)]

def RegexHandler(path: str) -> str:
    if "[" in path or "]" in path:
        path = SquareBracketHandler(path)
    return path

def SquareBracketHandler(path: str) -> str:
    newPath = ""
    for char in path:
        if char == '[' or char == ']':
            newPath += "[" + char + "]"
        else:
            newPath += char
    return newPath