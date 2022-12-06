from typing import List
from utils import Options, CompareFolder, BoolOption, IsNum, ExtractIntBasename
from multi_process import MultiProcess

def IsInclude(item: int, includes: List[int], reverse: bool = False) -> bool:
    if reverse:
        return item not in includes
    else:
        return item in includes

def InputExclude():
    MultiProcess.PrintPool()
    return [int(_) for _ in input("Input your excluded folder (e.g 1,4,5 or -1,-4,-5): ").split(",") if IsNum(_)]

def ExcludeFolder(folders: List[str]):
    MultiProcess.PrintPool()
    folders_dict = Options(folders)
    excluded_folder = InputExclude()
    reverse = any([True for folder in excluded_folder if folder < 0])

    return [v for k,v in folders_dict.items() if not IsInclude(k, [abs(_) for _ in excluded_folder], reverse)]

def ExcludeLoop(to_exclude: List[str], to_compare: List[str], message: str= "Excluding...") -> List[str]:
    MultiProcess.PrintPool()
    print(f"------ {message} ------")
    CompareFolder(to_exclude, to_compare)
    while(True):
        to_exclude = ExcludeFolder(to_exclude)
        CompareFolder(to_exclude, to_compare)

        if not BoolOption("Dou you want to exclude folder again?"):
            break
    return to_exclude

def AutoExclude(target_1: List[str], target_2: List[str]):
    dict_1 = {ExtractIntBasename(folder):folder for folder in target_1}
    dict_2 = {ExtractIntBasename(folder):folder for folder in target_2}

    exclude_1 = []
    exclude_2 = []

    for k,v in dict_1.items():
        if k not in dict_2.keys():
            continue
        exclude_1.append(v)
        exclude_2.append(dict_2[k])

    CompareFolder(exclude_1, exclude_2)
    if BoolOption("Do you want to manually exclude folder?"):
        return target_1, target_2, True

    return exclude_1, exclude_2, False