import os
import shutil
from utils import Folders, Files, Subpath, MEDIA_FILES
from extractor import Extractor

def CopyWellReport(src_well: str, dst_well: str) -> None:
    print(f"\n## Start copy {os.path.basename(src_well)}'s report ##")

    dst_history = os.path.join(dst_well, "WELL_HISTORY")

    JOBS = Folders(src_well)
    for job in JOBS:
        print(f"\n- {os.path.basename(job)}")

        dst_target = os.path.join(dst_history, os.path.basename(job), "REPORT")
        CopyFilesInJobFolder("10report", job, dst_target)

        dst_target = os.path.join(dst_history, os.path.basename(job), "DAILY REPORT")
        CopyFilesInJobFolder("12dlyrpt", job, dst_target)

def CopyFilesInJobFolder(folder_name: str, job: str, dst_target: str) -> None:
    job_target = os.path.join(job, folder_name)
    if not os.path.exists(job_target):
        print(f"{os.path.basename(job)} doesn't have {folder_name} folder")
    else:
        CopyFiles(job_target, dst_target)

def CopyFiles(job_target: str, dst_target: str) -> None:
    for file in Files(job_target, recursive=True):
        #Ignore media file
        if os.path.splitext(file)[1].lower() in MEDIA_FILES:
            print(f"{file} is media file. Skipping...")
            continue

        # Ignore file size over 200 MB
        if os.stat(file).st_size > 200 * 1024 * 1024:
            print(f"{file} size is over 120MB. Skipping...")
            continue

        report_target = os.path.join(dst_target, Subpath(job_target, os.path.split(file)[0]))
        if not os.path.exists(report_target):
            os.makedirs(report_target)
        if not os.path.exists(os.path.join(report_target, os.path.basename(file))):
            shutil.copy2(file, report_target)
            print(f"Copied {os.path.basename(file)} to {report_target}")
            Extractor(os.path.join(report_target, os.path.basename(file)))

def DeleteFiles(dst_target: str) -> None:
    for file in Files(dst_target, recursive=True):
        # Delete Media files
        if os.path.splitext(file)[1].lower() in MEDIA_FILES:
            os.remove(file)
            print(f"Deleted {os.path.basename(file)} in {os.path.split(file)[0]}")

def DeleteFilesHistory(dst_well: str) -> None:
    print(f"\n## Start delete {os.path.basename(dst_well)}'s files ##")

    dst_history = os.path.join(dst_well, "WELL_HISTORY")
    DeleteFiles(dst_history)

def DeleteFolderRecursive(dst_target: str) -> None:
    for folder in Folders(dst_target):
        DeleteFolderRecursive(folder)
    files = Files(dst_target)
    folders = Folders(dst_target)
    if len(files) == 0 and len(folders) == 0:
        os.rmdir(dst_target)
        print(f"Deleted {os.path.basename(dst_target)} in {os.path.split(dst_target)[0]}")

def DeleteFolderRecursiveHistory(dst_well: str) -> None:
    print(f"\n## Start delete {os.path.basename(dst_well)}'s folder ##")

    dst_history = os.path.join(dst_well, "WELL_HISTORY")
    DeleteFolderRecursive(dst_history)