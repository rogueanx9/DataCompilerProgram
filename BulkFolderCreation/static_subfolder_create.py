import os
from glob import glob
from typing import List

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[Warning] You cannot input empty string as an absolute path!")
        path = input(msg)
    return os.path.abspath(path)

def SeparatorInput(msg: str, sep: str = ",") -> List[str]:
    return [_.lstrip().rstrip() for _ in input(f"(use '{sep}' to separate)\n{msg}").split(sep)]

def JoinRelPath(*args: str) -> str:
    relPath = ""
    for arg in args:
        relPath = os.path.join(relPath, arg)
    return relPath

def SubfolderCreation(target_path: str, *args):
    TARGET_BASENAME = os.path.basename(target_path)

    # TODO: Make these 2 variable persist outside scope
    #       without passing arguments
    INTERMEDIATE_FOLDERS = args[0] if args else ["Pressure Survey"]
    NEW_FOLDERS = args[1] if args else SeparatorInput("Input your new folders name: ")

    for folder in NEW_FOLDERS:
        REL_FOLDER_PATH = JoinRelPath(*INTERMEDIATE_FOLDERS, folder)
        NEW_FOLDER_PATH = os.path.join(target_path, REL_FOLDER_PATH)

        if not os.path.exists(NEW_FOLDER_PATH):
            os.makedirs(NEW_FOLDER_PATH)
            print(f"Created {REL_FOLDER_PATH} in {TARGET_BASENAME}")

    return [INTERMEDIATE_FOLDERS, NEW_FOLDERS] # Arguments

if __name__ == "__main__":
    while(True):
        DST_PATH = Abspath("Input your wells folder: ")

        ARGS = []
        for folder in glob(os.path.join(DST_PATH, "*")):
            ARGS = SubfolderCreation(folder, *ARGS)