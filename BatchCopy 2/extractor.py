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

    print(f"Extracted {os.path.basename(path)} to {os.path.split(path)[0]}")

@NewFolderName
def ZipExtractor(path: str) -> None:
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(os.path.split(path)[0])
    print(f"Extracted {os.path.basename(path)} to {os.path.split(path)[0]}")