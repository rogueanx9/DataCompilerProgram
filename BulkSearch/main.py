import os
from glob import glob
from typing import List

def Folders(folders: List[str]) -> List[str]:
    return [folder for folder in folders if os.path.isdir(folder)]

def Files(files: List[str]) -> List[str]:
    return [file for file in files if os.path.isfile(file)]

def GlobJoin(src: str, append: str) -> List[str]:
    return glob(os.path.join(src, append))

def main():
    WELLS_PATH = os.path.abspath(input("Input well directory: "))
    REL_PATH = os.path.relpath(input("Input relative path directory: "))
    WELLS = Folders(GlobJoin(WELLS_PATH, "*"))

    for well in WELLS:
        well_name = os.path.basename(well)
        FOLDERS_IN_REL_PATH = Folders(GlobJoin(well, os.path.join(REL_PATH, "*")))

        print(f"---- {well_name} ----")

        for folder in FOLDERS_IN_REL_PATH:
            folder_name = os.path.basename(folder)
            files = Files(GlobJoin(folder, "*"))

            print(f"{folder_name} [{len(files)}]", end=": ")
            for file in files:
                print(os.path.basename(file), end=", ")
            print()

def main2():
    WELLS_PATH = os.path.abspath(input("Input well directory: "))
    WELLS = Folders(GlobJoin(WELLS_PATH, "*"))

    for well in WELLS:
        well_name = os.path.basename(well)
        print(well_name)

if __name__ == "__main__":
    main2()
