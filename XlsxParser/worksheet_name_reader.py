from typing import Any, List
from pandas import ExcelFile
import os
from glob import iglob

from zipfile import ZipFile
from bs4 import BeautifulSoup
import xlrd

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[Warning] Absolute path cannot be empty!")
        path = input(msg)
    return os.path.abspath(path)

def ChainRelPath(*paths: str) -> str:
    relPath = ""
    for path in paths:
        relPath = os.path.join(relPath, path)
    return relPath

def Folders(path: str, keywords: List[str] = [""]) -> List[str]:
    return [_ for _ in iglob(os.path.join(path, "*")) if os.path.isdir(_) and KeywordsIn(os.path.basename(_), keywords)]

def Files(path: str, keywords: List[str] = [""]) -> List[str]:
    return [_ for _ in iglob(os.path.join(path, "*")) if os.path.isfile(_) and KeywordsIn(os.path.basename(_), keywords)]

def KeywordsIn(text: str, keywords: List[str]) -> bool:
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

def PrintList(items: List[Any], sep: str = '  ', col: int = 2):
    end = ''
    max_len_col = []

    for i in range(len(items)):
        if i < col:
            max_len_col.append(len(items[i]))
        elif len(items[i]) > max_len_col[i % col]:
            max_len_col[i % col] = len(items[i])

    for i in range(len(items)):
        spaces = max_len_col[i % col] - len(items[i])
        end = spaces * ' ' + ('\n' if (i+1) % col == 0 else sep)
        print(items[i], end=end)

    if '\n' not in end: print()

def PathSplitTail(path: str, count: int = 1):
    for i in range(count):
        path = os.path.split(path)[0]
    return path

def WorksheetNames(file: str) -> List[Any]:
    ext = os.path.splitext(file)[1]
    try:
        # --- PANDAS ---
        # return ExcelFile(file).sheet_names

        # --- ZipFile (.xlsx only)
        if ext.lower() in [".xlsx", ".xlsm"]:
            zipped_file = ZipFile(file)
            byte = zipped_file.open(r'xl/workbook.xml').read()
            soup = BeautifulSoup(byte, "xml")
            return [sheet.get("name") for sheet in soup.find_all("sheet")]

        # --- xlrd ---
        elif ext.lower() == ".xls": 
            return xlrd.open_workbook(file, on_demand=True).sheet_names()

        else: raise Exception("Wrong extension!")
    except Exception as e:
        print(f"Cannot load workbook! {e}")
        print("Returning empty list...")
        return [""]

def main():
    SRC_PATH = Abspath("Input your well directory: ")
    SRC_FOLDERS = Folders(SRC_PATH)
    INTERMEDIATE_FOLDER = ChainRelPath("PRESSURE_SURVEY")

    print(f"!! {os.path.basename(PathSplitTail(SRC_PATH))}'s wells worksheet names !!")
    for folder in SRC_FOLDERS:
        print(f"\n{os.path.basename(folder)}")

        folder_append = os.path.join(folder, INTERMEDIATE_FOLDER)
        xls_files = Files(folder_append, ["xls"])
        
        for xls_file in xls_files:
            print(f"> {os.path.basename(xls_file)}")
            PrintList(WorksheetNames(xls_file))

if __name__ == "__main__":
    while True:
        main()