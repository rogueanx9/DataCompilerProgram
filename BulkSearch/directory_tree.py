import os
from glob import glob
from utils import Abspath, Indent, Folders, Files

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if files: print("[F]", end=" ")
        level -= 1 if files else 0
        print(f"{Indent(level)}\\{os.path.basename(root)}")
        level += 1 if files else 0
        for file in files:
            print(f"{Indent(level + 1)}{os.path.basename(file)}")

def list_files2(startpath: str, level: int = 0) -> None:
    # Gather files and folders
    files = Files(startpath)
    folders = Folders(startpath)

    # Preprocess
    if not files and not folders:
        return
    
    # Print Current Directory
    print(f"{Indent(level)}\\{os.path.basename(startpath)}")
    
    # Print files in current directory
    for file in files:
        print(f"{Indent(level + 1)}{os.path.basename(file)}")

    # Recursively list files in subfolder
    level += 1
    for folder in folders:
        list_files2(folder, level)


def main():
    PATH_TO_SEARCH = Abspath("Input path to search: ")
    for job in glob(os.path.join(PATH_TO_SEARCH, "*")):
        list_files2(job)
        input("Press ENTER to continue...")
        print()

def main2():
    list_files2(Abspath("Input path to list: "))

if __name__ == "__main__":
    main()
