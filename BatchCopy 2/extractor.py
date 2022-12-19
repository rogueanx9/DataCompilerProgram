import os, zipfile
import extract_msg
from utils import Files, NewFolderName

def Extractor(path: str) -> None:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".msg": MsgExtractor(path)
    if ext == ".zip": ZipExtractor(path)

def MsgExtractor(path: str) -> None:
    zip_name = os.path.splitext(path)[0] + ".zip"

    # Extract Msg to Zip
    try:
        msg = extract_msg.openMsg(path)
        msg.save(zip=zip_name, skipBodyNotFound=True)
        print(f"Extracted {os.path.basename(path)} to {os.path.split(path)[0]}")
    except Exception as e:
        print(f"Cannot extract {os.path.basename(path)} as {e}. Skipping...")
        return
    
    # Extract Zip to folder
    newFolderName = ZipExtractor(zip_name)

    # If somehow the attachment is extractable, extract
    for file in Files(newFolderName, recursive=True):
        Extractor(file)

    # Delete zip
    if os.path.isfile(zip_name):
        os.remove(zip_name)

@NewFolderName
def ZipExtractor(path: str) -> None:
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            if LeastZipTreeCount(zip_ref) > 1:
                extract_path = os.path.splitext(path)[0]
                if not os.path.exists(extract_path):
                    os.mkdir(extract_path)
                zip_ref.extractall(extract_path)
            else:
                zip_ref.extractall(os.path.split(path)[0])
            print(f"Extracted {os.path.basename(path)} to {os.path.split(path)[0]}")
    except Exception as e:
        print(f"Cannot extract {os.path.basename(path)} as {e}. Skipping...")

def LeastZipTreeCount(zipfile: zipfile.ZipFile) -> int:
    leastTree = 0
    leastTreeCount = 0
    for path in zipfile.namelist():
        counter = path.count("/")
        if counter < leastTree:
            leastTree = counter
            leastTreeCount = 0
        if counter == leastTree:
            leastTreeCount += 1
    return leastTreeCount