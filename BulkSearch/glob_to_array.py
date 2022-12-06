from math import nan
import os
from glob import glob
from typing import Any, List

def isNum(any) -> bool:
    try:
        int(any)
    except:
        return False
    return True

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[Warning] Absolute path can't be empty!")
        path = input(msg)
    return os.path.abspath(path)

def ExtractInt(text: str) -> int:
    num_str = ""
    first_time = True
    for i in range(len(text)):
        if isNum(text[i]):
            first_time = False
            num_str += text[i]
        if not isNum(text[i]) and not first_time:
            break

    if not num_str:
        print("[Warning] There is no number in this text. Returning 0")
        return 0
    else:
        return int(num_str)

def Folders(path: str) -> List[str]:
    return [_ for _ in glob(os.path.join(path, '*')) if os.path.isdir(_)]

def main():
    folders = Folders(Abspath("Input folders absolute path: "))
    for folder in folders:
        print(ExtractInt(os.path.basename(folder)), end=",")

if __name__ == "__main__":
    main()