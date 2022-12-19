import os, platform
from glob import iglob, glob
from typing import List, Any
from regex_handler import RegexHandler
import tempfile
import shutil

MEDIA_FILES = [".mp4", ".wmv", ".asf", ".bup", ".ifo", ".vob", ".avi", ".mkv", ".mov", ".wav"]

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[W] You cannot input empty string.")
        path = input(msg)
    return os.path.abspath(path)

def BoolOptions(msg: str) -> bool:
    Bool = input(f"{msg} (Y/N)? ")
    if Bool.lower() not in ["y", ""]:
        return False
    return True

def ExcludeLoop(first_list: List[Any], second_list = [], name_shorter=lambda x : x) -> List[Any]:
    first_list = ExcludeCLI(first_list, second_list=second_list, name_shorter=name_shorter)
    while BoolOptions("Do you want to exclude again"):
        first_list = ExcludeCLI(first_list, second_list=second_list, name_shorter=name_shorter)
    return first_list

def ExcludeCLI(first_list: List[Any], second_list = [], name_shorter=lambda x : x) -> List[Any]:
    if second_list:
        ListCompare(first_list, second_list, name_shorter=name_shorter)
    return [first_list[i] for i in Options(first_list, name_shorter=name_shorter)]

def Files(path: str, recursive: bool = False) -> List[str]:
    if not path: 
        print("[W] Path is Empty. Returning empty list")
        return []
    path = RegexHandler(path)
    ast = "**" if recursive else "*"
    return [file for file in glob(os.path.join(path, ast), recursive=recursive) if os.path.isfile(file)]

def Folders(path: str, recursive: bool = False) -> List[str]:
    if not path: 
        print("[W] Path is Empty. Returning empty list")
        return []
    path = RegexHandler(path)
    ast = "**" if recursive else "*"
    return [folder for folder in glob(os.path.join(path, ast), recursive=recursive) if os.path.isdir(folder)]

def FileFiltered(file:str, ext_exclude: List[str], max_size: int) -> bool:
    #Ignore file with extension in ext_exclude 
    if os.path.splitext(file)[1].lower() in ext_exclude:
        print(f"{file} extention is in {','.join(ext_exclude)}. Filtered!")
        return True

    # Ignore file size over max_size in MB
    if os.stat(file).st_size > max_size * 1024 * 1024:
        print(f"{file} size is over {max_size}MB. Filtered!")
        return True

    return False

def IsInt(any: Any) -> bool:
    try:
        int(any)
    except ValueError:
        return False
    return True

def ListCompare(first_list: List[Any], second_list: List[Any], name_shorter=lambda x : x) -> None:
    print("\n## COMPARE ##")

    # Run shorting function
    first_list  = [name_shorter(_) for _ in first_list]
    second_list = [name_shorter(_) for _ in second_list]

    # Equalize length of those lists
    diff = len(first_list) - len(second_list)
    if diff < 0:
        first_list = first_list + (abs(diff) * ['-'])
    else:
        second_list = second_list + (abs(diff) * ['-'])

    # Print list side by side
    sep = '|'
    for i, (item_1, item_2) in enumerate(zip(first_list, second_list)):
        print(f"{i+1}. {item_1} {sep} {item_2}")

def NewFolderName(extractor):
    def wrapper(path: str, *args, **kwargs) -> str:
        currDir = os.path.split(path)[0]
        currFolders = Folders(currDir)
        extractor(path, *args, **kwargs)
        new_folders = [_ for _ in Folders(currDir) if _ not in currFolders]
        return new_folders[0] if new_folders else ""
    return wrapper

def NewFileName(extractor):
    def wrapper(path: str, *args, **kwargs) -> str:
        currDir = os.path.split(path)[0]
        currFiles = Files(currDir)
        extractor(path, *args, **kwargs)
        new_files = [_ for _ in Files(currDir) if _ not in currFiles]
        return new_files[0] if new_files else ""
    return wrapper

def Options(options: List[Any], name_shorter=lambda x : x) -> List[int]:
    print("\n## OPTIONS ##")

    # Print Options
    for i, item in enumerate(options):
        end = '\n' if i % 2 != 0 or i == (len(options) - 1) else ' '
        print(f"{i+1}. {name_shorter(item)}", end=end)

    # Get selected options
    exclude_id = [int(id) for id in input("Input to exclude (e.g. 1,3,5 or -1,3,5): ").split(",") if IsInt(id)]

    # Check if there is any negative value
    reverse = True if any([x < 0 for x in exclude_id]) else False

    # Make sure all id is positive
    exclude_id = [abs(id) for id in exclude_id]

    if reverse:
        return [i for i in range(len(options)) if (i+1) in exclude_id]
    else:
        return [i for i in range(len(options)) if (i+1) not in exclude_id]

def Subpath(base_path: str, child_path: str) -> str:
    path = ""
    while os.path.basename(child_path) != os.path.basename(base_path):
        path = os.path.join(os.path.basename(child_path), path)
        child_path = os.path.split(child_path)[0]
    return path

def Symlink(src: str, dst: str) -> None:
    if platform.system() == "Windows":
        def symlink_ms(source, link_name):
            import ctypes
            import ctypes.wintypes as wintypes
            if os.path.exists(link_name):
                df = ctypes.windll.kernel32.DeleteFileW
                if df(link_name) == 0:
                    print("Could not remove existing file:", link_name)
                    print("You should remove the file manually through Explorer or an elevated cmd process. Skipping...")
            csl = ctypes.windll.kernel32.CreateSymbolicLinkW
            csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
            csl.restype = ctypes.c_ubyte
            flags = 1 if os.path.isdir(source) else 0
            flags += 2 # For unprivileged mode. Requires Developer Mode to be activated.
            if csl(link_name, source, flags) == 0:
                raise ctypes.WinError()
        return symlink_ms(src, dst)
    else:
        return os.symlink(src, dst)