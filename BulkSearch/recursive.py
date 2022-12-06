import os
from glob import glob
from typing import List

def Files(files: List[str]) -> List[str]:
    return [file for file in files if os.path.isfile(file)]

def IsIn(text: str, keywords: List[str]) -> bool:
    for word in keywords:
        if word.lower() in text.lower():
            return True
    return False

def Stripped(text: str) -> str:
    return text.lstrip().rstrip()

def SeparatorInput(msg: str, sep: str = ",") -> List[str]:
    text = input(msg)
    if not text:
        print("Cannot input empty string.")
        return SeparatorInput(msg, sep)

    if not sep in text:
        return [text]

    return [Stripped(x) for x in text.split(sep)]

def main():
    BASE_PATH = input("Input directory: ")
    KEYWORDS = SeparatorInput("Input keywords (e.g. mit,pbu): ")

    print("\n--- Searching Files ---")

    FILES_IN_BASE_PATH = Files(glob(os.path.join(BASE_PATH, "**"), recursive=True))
    FILTERED_FILES = [file for file in FILES_IN_BASE_PATH if IsIn(os.path.basename(file), KEYWORDS)]

    print("--- DONE ---")
    for file in FILTERED_FILES:
        print(f"File: {os.path.basename(file)}")
        print(f"Path: {file}")
        print()

if __name__ == "__main__":
    main()
