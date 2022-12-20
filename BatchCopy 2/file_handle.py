import os, tempfile, shutil, time
from typing import List

def WriteToFile(path: str, content: str) -> None:
    target_ext = [".txt", ".csv"]
    if os.path.splitext(path)[1].lower() not in target_ext:
        raise Exception(f"Path should be a file with an extension of {','.join(target_ext)}")

    with open(path, 'a') as f:
        f.write(f"{content}\n")

def WriteToTempFile(filename: str, content: str) -> None:
    file_path = os.path.join(tempfile.gettempdir(), filename)
    WriteToFile(file_path, content)

def CacheTempFile(file: str, delete: bool) -> str:
    if not os.path.isfile(file):
        return file
        
    target = os.path.join(tempfile.gettempdir(), os.path.basename(file))
    if not delete:
        if os.path.isfile(target): 
            shutil.copyfile(file, target)
        return target
    else:
        if os.path.isfile(target): 
            os.remove(target)
        return file

def DeleteTempFile(filename: str) -> None:
    file_path = os.path.join(tempfile.gettempdir(), filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

def IsTempFile(filename: str) -> bool:
    return os.path.isfile(TempFile(filename))

def KeyInFile(key: str, file: str, case_sen = False) -> bool:
    key = key if case_sen else key.lower()
    with open(file, 'r') as f:
        for line in f:
            line = line if case_sen else line.lower()
            if key in line:
                return True
    return False

def KeysInFile(keys: List[str], file: str, case_sen = False) -> bool:
    for key in keys:
        if KeyInFile(key, file, case_sen):
            return True
    return False

def TempFile(filename: str) -> str:
    return os.path.join(tempfile.gettempdir(), filename)

def Test():
    key = "\\\\jktbbfs1\\shared\\maxwell\\drl_wel1_operated\\block_b\\belida_field\\ba-23\\job09@2009\\10report\\dhv10101\\8136.jpg"
    file = "\\\\Tenfps1vfs\\ptdm\\00-E-FILE\\BLOCK B\\FIELD\\BELIDA\\WELL\\BLDA_WELL_BA_0023ST2\\WELL_HISTORY\\JOB09@2009\\REPORT\\dhv10101\\FILE NOT COPIED.txt"
    print(KeyInFile(key, file, False))

if __name__ == "__main__":
    Test()