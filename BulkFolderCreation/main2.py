import os
from glob import glob
from typing import Any, List

def isNumber(any: Any):
    try:
        int(any)
    except:
        return False
    return True

def InputAbspath(msg: str) -> str:
    path = ""
    while not path:
        path = input(msg)
    return os.path.abspath(path)

def MultiFolders(srcs: List[Any], basename_filter = lambda x: bool(x)) -> List[str]:
    folders = []
    for src in srcs:
        if src is List:
            folders += MultiFolders(src, basename_filter)
        else:
            folders += Folders(src, basename_filter)
    return folders

def Folders(src: str, basename_filter = lambda x: bool(x)) -> List[str]:
    return [folder for folder in glob(os.path.join(src, "*")) if os.path.isdir(folder) and basename_filter(os.path.basename(folder))]

def isNumberPredeceasing(text: str) -> bool:
    text_split = text.split()
    if len(text_split) < 2:
        return False
    return isNumber(text_split[0])

def main():
    BLOCK_SRC_PATH = InputAbspath("Input block directory: ")
    FIELD_FOLDERS = Folders(BLOCK_SRC_PATH, lambda x: not isNumberPredeceasing(x))
    WELL_FOLDERS = MultiFolders(FIELD_FOLDERS, lambda x: not isNumberPredeceasing(x))

    NEW_FOLDERS = ["PBU", "MRT", "SBHP_FBHP"]

    for well in WELL_FOLDERS:
        for folder in NEW_FOLDERS:
            folder_path = os.path.join(well, "Pressure Survey", folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created {folder_path}")

def main2():
    WELLS_PATH = InputAbspath("Input wells folder: ")
    DST_PATH = InputAbspath("Input destination: ")
    NEW_FOLDERS = ["PBU", "MRT", "SBHP_FBHP", "RFT"]

    WELL_FOLDERS = Folders(WELLS_PATH)

    for well in WELL_FOLDERS:
        well_basename = os.path.basename(well)
        for folder in NEW_FOLDERS:
            folder_path = os.path.join(DST_PATH, well_basename, "Pressure Survey", folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created {folder_path}")

if __name__ == "__main__":
    main2()