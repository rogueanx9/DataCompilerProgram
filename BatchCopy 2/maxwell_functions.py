import os
import shutil
from utils import Folders, Files, Subpath, MEDIA_FILES, ExcludeLoop, FileFiltered
from file_handle import KeyInFile, WriteToTempFile, IsTempFile, TempFile, CacheTempFile
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

        dst_target = os.path.join(dst_history, os.path.basename(job), "GEOLOG")
        CopyFilesInJobFolder("05geolog", job, dst_target)

        dst_target = os.path.join(dst_history, os.path.basename(job), "DAILY GEOLOG")
        CopyFilesInJobFolder("14dlygeo", job, dst_target)

        dst_target = os.path.join(dst_history, os.path.basename(job), "MISC")
        CopyFilesInJobFolder("21temp", job, dst_target, 3)

        dst_target = os.path.join(dst_history, os.path.basename(job), "MISC")
        CopyFilesInJobFolder("20other", job, dst_target, 3)

def CopyFilesInJobFolder(folder_name: str, job: str, dst_target: str, depth_target: int = 99) -> None:
    job_target = os.path.join(job, folder_name)
    if not os.path.exists(job_target):
        print(f"{os.path.basename(job)} doesn't have {folder_name} folder")
    else:
        CopyFiles(job_target, dst_target, depth_target)

def CopyFiles(job_target: str, dst_target: str, depth_target: int = 99) -> None:
    subpath_prev, subpath_count = "", 0
    for file in Files(job_target, recursive=True):
        subpath = Subpath(job_target, os.path.split(file)[0])
        report_target = os.path.join(dst_target, subpath)
        file_not_copied = os.path.join(report_target, "FILE NOT COPIED.txt")

        # Check if there is a temp file not copied
        if subpath != subpath_prev and IsTempFile(os.path.basename(file_not_copied)):
            prev_target = os.path.join(dst_target, subpath_prev)
            if not os.path.isdir(prev_target):
                os.makedirs(prev_target)

            shutil.copy2(TempFile(os.path.basename(file_not_copied)), prev_target)
            os.remove(TempFile(os.path.basename(file_not_copied)))

        # Check if file is in FILE NOT COPIED.txt. TODO: Cache in Memory. It is so slow now.
        # if os.path.isfile(file_not_copied) and KeyInFile(file, file_not_copied, True):
        #     print(f"{file} already noted in {file_not_copied}. Skipping...")
        #     continue

        # Filter file with more than depth_target subfolder
        if subpath.count(os.sep) > depth_target:
            print(f"{file} located in more than {depth_target} subfolder. Skipping...")
            continue

        # Filter file if parent directory has over max_files files copied
        subpath_count = subpath_count + 1 if subpath == subpath_prev else 0
        subpath_prev = subpath
        if subpath_count > 500:
            print(f"{os.path.split(file)[0]} has over 500 files copied. Cannot copy {os.path.basename(file)}!")
            WriteToTempFile(os.path.basename(file_not_copied), file)
            continue

        # Filter file according to extension and file size
        if FileFiltered(file, MEDIA_FILES, 200): 
            WriteToTempFile(os.path.basename(file_not_copied), file)
            continue

        # Create folder if doesn't exist
        if not os.path.exists(report_target):
            os.makedirs(report_target)

        # Copy file to folder target
        if not os.path.exists(os.path.join(report_target, os.path.basename(file))):
            try:
                shutil.copy2(file, report_target)
                print(f"Copied {os.path.basename(file)} to {report_target}")
                Extractor(os.path.join(report_target, os.path.basename(file)))
            except Exception as e:
                print(f"Cannot copy {file} as {e}. Skipping...")

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

def CopyWellHistTemplate():
    file_to_copy = "\\\\Tenfps1vfs\\ptdm\\05-DATA\\DATA COMPILING\\USER GUIDE\\Data Compiling - Rogan Steeven Saulus\\Template\\Well History - Compile - Template2.xlsx"
    wells = ExcludeLoop(Folders(input("WELLS: ")), name_shorter=os.path.basename)
    for well in wells:
        TARGET = os.path.join(well, "WELL_HISTORY")
        if not os.path.exists(TARGET):
            print(f"{os.path.basename(well)} has no WELL_HISTORY folder. Skipping...")
            continue
        if not os.path.exists(os.path.join(TARGET, os.path.basename(file_to_copy))):
            shutil.copy2(file_to_copy, TARGET)
            print(f"Copied well history template to {os.path.basename(well)}")