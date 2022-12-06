from glob import glob
import os, shutil
from typing import List
from multi_process import MultiProcess

def Abspath(message: str) -> str:
    MultiProcess.PrintPool()
    path = ""
    while(not path):
        path = input(message)
        if path:
            break
        print("Absolute path cannot be empty!")
    return os.path.abspath(path)

def Relpath(message: str) -> str:
    MultiProcess.PrintPool()
    path = input(message)
    if path:
        try:
            return os.path.relpath(path)
        except ValueError as e:
            if str(e).startswith("path is on mount"):
                print(f"[ERROR]: You cannot input absolute path. Please retry!")
            else:
                print(f"[ERROR]: {e}. Please retry!")
            return Relpath(message)
    else:
        return ""

def BoolOption(message: str) -> bool:
    MultiProcess.PrintPool()
    Bool = input(f"{message} (Y/N): ")
    if Bool.lower() not in ["y", ""]:
        return False
    return True

def CompareFolder(src: List[str], dst: List[str]):
    src_base_name = [os.path.basename(x) for x in src]
    dst_base_name = [os.path.basename(x) for x in dst]

    src_norm, dst_norm = EqualizeLen(src_base_name, dst_base_name, "-")

    MultiProcess.Print(str(len(src)) + " " + str(len(dst)))
    MultiProcess.Print("-------------------")
    for item_src, item_dst in zip(src_norm, dst_norm):
        print(item_src, end=" | ")
        print(item_dst)
    MultiProcess.Print("-------------------")
    MultiProcess.Print(str(len(src)) + " " + str(len(dst)))

def Copy(src: str, dst: str, copy_folder: bool):
    if copy_folder:
        src_base_name = os.path.basename(src)

        dst_target_folder = os.path.join(dst, src_base_name)
        if not os.path.isdir(dst_target_folder):
            os.mkdir(dst_target_folder)

        shutil.copytree(src, dst_target_folder, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)

def EqualizeLen(list1: List, list2: List, def_val):
    filler = [def_val for _ in range(abs(len(list1) - len(list2)))]
    if len(list1) > len(list2):
        return list1, list2 + filler
    else:
        return list1 + filler, list2

def ExtractInt(text: str) -> int:
    num_str = ""
    first_time = True
    for i in range(len(text)):
        if IsNum(text[i]):
            first_time = False
            num_str += text[i]
        if not IsNum(text[i]) and not first_time:
            break

    if not num_str:
        print("[Warning] There is no number in this text. Returning 0")
        return 0
    else:
        return int(num_str)

def ExtractIntBasename(text: str) -> int:
    return ExtractInt(os.path.basename(text))

def Files(path: str, keywords: List[str], recursive: bool = False) -> List[str]:
    path = os.path.join(path,"**" if recursive else "*")
    return [file for file in glob(path, recursive=recursive) if os.path.isfile(file) and KeywordsIn(os.path.basename(file), keywords)]

def Folders(path: str, keywords: List[str], recursive: bool = False) -> List[str]:
    path = os.path.join(path,"**" if recursive else "*")
    return [folder for folder in glob(path, recursive=recursive) if os.path.isdir(folder) and KeywordsIn(os.path.basename(folder), keywords)]

def IsNum(num: str) -> bool:
    try:
        int(num)
    except ValueError:
        return False
    return True

def KeywordsIn(text: str, keywords: List[str]) -> bool:
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

def Options(options: List) -> dict:
    MultiProcess.PrintPool()
    options_dict = {i+1:options[i] for i in range(len(options))}
    
    for no, folder in options_dict.items():
        end = "\n" if no % 3 == 0 or no == len(options) else "  "
        print(f"{no}. {os.path.basename(folder)}", end=end)

    return options_dict