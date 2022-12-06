import os
from glob import glob
from multiprocessing.dummy import Pool as ThreadPool
from multi_process import MultiProcess

from utils import *
from exclude_folder import ExcludeLoop, AutoExclude
from dummy_variable import *

MultiProcess.PROCESSES = 0
RELEASE = True
def main(pool: int = 0):
    STOP = False

    SRC_BASE_PATH = Abspath("Input your well source folder: ") if RELEASE else d_SRC_BASE_PATH
    DST_BASE_PATH = Abspath("Input your well destination folder: ") if RELEASE else d_DST_BASE_PATH

    FOLDER_IN_SRC = [well for well in glob(os.path.join(SRC_BASE_PATH, "*")) if os.path.isdir(well)]
    FOLDER_IN_DST = [well for well in glob(os.path.join(DST_BASE_PATH, "*")) if os.path.isdir(well)]

    # If src's and dst's folder is not equal. We need to exclude
    # dst's folder to mimic src's folder
    RUN_EXCLUDE = RELEASE
    if RUN_EXCLUDE:
        FOLDER_IN_SRC, FOLDER_IN_DST, MANUAL_EXCLUDE = AutoExclude(FOLDER_IN_SRC, FOLDER_IN_DST)

        if MANUAL_EXCLUDE:
            FOLDER_IN_SRC = ExcludeLoop(FOLDER_IN_SRC, FOLDER_IN_DST, "Excluding Well Source Folders")
            FOLDER_IN_DST = ExcludeLoop(FOLDER_IN_DST, FOLDER_IN_SRC, "Excluding Well Destination Folders")

    print("##### COPY SECTION #####")
    COPYFOLDER = BoolOption("Do you want to copy folder? if not, mode will be copy files")
    COPYMODE = 'folders' if COPYFOLDER else 'files'
    print(f"Copy Mode: {COPYMODE}")

    SRC_TARGET_REL_PATH = Relpath("Input your relative target source folder: ") if RELEASE else d_SRC_TARGET_REL_PATH
    SRC_RECURSIVE = BoolOption(f"Do you want to search source {COPYMODE} recursively?")

    DST_TARGET_REL_PATH = Relpath("Input your relative target destination folder: ") if RELEASE else d_DST_TARGET_REL_PATH
    KEYWORDS = input("Input keywords in filename (e.g. mit,pbu,capacity): ").split(",")

    print("\n")
    for SRC_WELL, DST_WELL in zip(FOLDER_IN_SRC, FOLDER_IN_DST):
        SRC_WELLNAME = os.path.basename(SRC_WELL)
        DST_WELLNAME = os.path.basename(DST_WELL)

        print(f"----- {SRC_WELLNAME} -----")

        SRC_TARGET_ABS_PATH = os.path.join(SRC_WELL, SRC_TARGET_REL_PATH)
        DST_TARGET_ABS_PATH = os.path.join(DST_WELL, DST_TARGET_REL_PATH)

        if not os.path.isdir(SRC_TARGET_ABS_PATH):
            print(f"{SRC_TARGET_ABS_PATH} doesn't exist. Continue to next well.")
            continue
        if not os.path.isdir(DST_TARGET_ABS_PATH):
            print(f"{DST_TARGET_ABS_PATH} doesn't exist. Continue to next well.")
            continue

        things = Folders(SRC_TARGET_ABS_PATH, KEYWORDS, SRC_RECURSIVE) if COPYFOLDER else Files(SRC_TARGET_ABS_PATH, KEYWORDS, SRC_RECURSIVE)
        
        if not things:
            print(f"There is no {COPYMODE} in {SRC_TARGET_ABS_PATH} that satisfies your keyword.")

        for thing in things:
            if RELEASE:
                Copy(thing, DST_TARGET_ABS_PATH, COPYFOLDER)
                print(f"Copied {os.path.basename(thing)} to {DST_WELLNAME}")

            if not RELEASE:
                STOP = True

        if STOP:
            break

if __name__ == '__main__':
    if MultiProcess.PROCESSES:
        with ThreadPool(2) as p:
            p.map(main, [i+1 for i in range(MultiProcess.PROCESSES)])
    else:
        while(True):
            main()