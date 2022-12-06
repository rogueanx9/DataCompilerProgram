import os
from dataclasses import dataclass, field
from typing import List, Any, Callable, Union
from glob import iglob

@dataclass
class Walks:
    root: str = ""
    dirs: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)

def Abspath(msg: str) -> str:
    path = ""
    while not path:
        path = input(msg)
    return os.path.abspath(path)

def Files(path: str, recursive: bool = False) -> List[str]:
    if not path: 
        print("[W] Path is Empty. Returning empty list")
        return []
    ast = "**" if recursive else "*"
    return [file for file in iglob(os.path.join(path, ast), recursive=recursive) if os.path.isfile(file)]

def Folders(path: str, recursive: bool = False) -> List[str]:
    if not path: 
        print("[W] Path is Empty. Returning empty list")
        return []
    ast = "**" if recursive else "*"
    return [folder for folder in iglob(os.path.join(path, ast), recursive=recursive) if os.path.isdir(folder)]

def Indent(level: int) -> str:
    return ' ' * 4 * level

def KeysIn(keys, text: str) -> bool:
    for key in keys:
        if key in text.lower():
            return True
    return False

def KeyInList(v_list, keys, ext_only = False):
    for item in v_list:
        item = item if not ext_only else item.split(".")[-1]
        if KeysIn(keys, item):
            return True
    return False

def PrepDefault(_: Union[Walks,str]) -> bool:
    return True

def PrintCurrentDir(level: int, walks: Walks, rootPrep: Callable[[Walks], bool], filePrep: Callable[[str], bool]):
    show = rootPrep(walks)
    if not show: return
    print(f"{Indent(level)}{os.path.basename(walks.root)}")

    for file in walks.files:
        show = filePrep(file)
        if not show: continue
        print(f"{Indent(level + 1)}{file}")

def PrintDecor(markFunc: Callable[[Walks], bool]):
    def wrapper(msg: str, walks: Walks) -> None:
        show = markFunc(walks)
        if show: print(msg)
    return wrapper

def PrintKey(msg, keys, ext_only = False):
    text = msg if not ext_only else msg.split(".")[-1]
    
    if KeysIn(keys, text):
        print("[f]", end=" ")
        print(msg)

def SepInput(msg: str, sep: str = ","):
    keys = input(msg)
    splitted = keys.split(sep)

    if len(splitted) == 0:
        print("[W] Input cannot be empty.")
        return SepInput(msg, sep)

    return splitted

def WillExit(key: str) -> bool:
    if key == os.path.abspath("q"): return True
    if key == os.path.abspath("exit"): return True

    return False

def list_files_bak(startpath, keys, show_folder = False):
    count = 0
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        if show_folder or KeyInList(files, keys):
            print('{}{}/'.format(indent, os.path.basename(root)))
            if KeyInList(files, keys):
                print(root)
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            PrintKey('{}{}'.format(subindent, f), keys, False)

        count = count + 1
        if not show_folder:
            print(count, end='\r')