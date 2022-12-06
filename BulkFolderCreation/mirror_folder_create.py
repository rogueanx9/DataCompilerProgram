from typing import List

import os
from glob import glob

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[Warning] You cannot input empty string as an absolute path!")
        path = input(msg)
    return os.path.abspath(path)

def Folders(path: str) -> List[str]:
    return [_ for _ in glob(os.path.join(path, "*")) if os.path.isdir(_)]

def main():
    SRC_PATH = Abspath("Input source folder to mirror: ")
    DST_PATH = Abspath("Input target folder: ")
    DST_BASENAME = os.path.basename(DST_PATH)
    SRC_FOLDERS = Folders(SRC_PATH)

    print("Start mirroring folder...")
    for folder in SRC_FOLDERS:
        folder_name = os.path.basename(folder)
        DST_FOLDER_PATH = os.path.join(DST_PATH, folder_name)

        if not os.path.exists(DST_FOLDER_PATH):
            os.mkdir(DST_FOLDER_PATH)
            print(f"Created {folder_name} in {DST_BASENAME}")

if __name__ == "__main__":
    main()