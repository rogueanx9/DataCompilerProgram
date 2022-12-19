import os
from utils import Abspath, Folders, ExcludeLoop, Files
from maxwell_functions import CopyWellReport, DeleteFilesHistory, DeleteFolderRecursiveHistory, CopyWellHistTemplate
from extractor import Extractor

def main():
    # Get src and dst wells folder path
    SRC_WELLS = Abspath("Input source wells path: ")
    DST_WELLS = Abspath("Input destination wells path: ")

    # List all well folder path
    SRC_WELL_FOLDERS = Folders(SRC_WELLS)
    DST_WELL_FOLDERS = Folders(DST_WELLS)

    # Compare and Exclude SRC and DST well folders
    SRC_WELL_FOLDERS = ExcludeLoop(SRC_WELL_FOLDERS, DST_WELL_FOLDERS, name_shorter=os.path.basename)
    DST_WELL_FOLDERS = ExcludeLoop(DST_WELL_FOLDERS, SRC_WELL_FOLDERS, name_shorter=os.path.basename)

    for src_well, dst_well in zip(SRC_WELL_FOLDERS, DST_WELL_FOLDERS):
        CopyWellReport(src_well, dst_well)
        # DeleteFilesHistory(dst_well)
        # DeleteFolderRecursiveHistory(dst_well)

def BatchExtractor():
    SRC_PATH = Abspath("Input source folder: ")
    SRC_FILES = Files(SRC_PATH, recursive=True)
    for file in SRC_FILES:
        Extractor(file)


if __name__ == "__main__":
    main()