import os

from utils import Abspath, Folders, ExpandRelPath

LOG_CREATE   = {"CASED_HOLE_LOG": "", "COMPLETION_LOG": "", "COMPOSITE_IMAGES": "", "LITHOLOGIC_LOG": "", "OPEN_HOLE_LOG": ""}
PRESS_CREATE = {"FBHP": "", "SBHP": "", "RFT_MDT": "", "PBU": ""}
PVT_CREATE   = {"CRUDE_ASSAY": "", "GAS_COMPOSITION": "", "PVT_REPORT": "", "WATER_ANALYSIS": ""}
WELL_CREATE  = {"CORE": "", "FWR": "", "LOG": LOG_CREATE, "PRESSURE_SURVEY": PRESS_CREATE, "PVT": PVT_CREATE, "TRAJECTORY": "", "WELL_HISTORY": "", "WELL_SKETCH": "", "WRR": ""}

def main():
    WELLS_PATH = Abspath("Wells folder: ")
    WELLS_FOLDERS = Folders(WELLS_PATH)
    WELL_NEW_FOLDERS = ExpandRelPath(WELL_CREATE)

    for well in WELLS_FOLDERS:
        well_folders = [os.path.join(well, folder) for folder in WELL_NEW_FOLDERS]
        for folder in well_folders:
            if not os.path.exists(folder):
                print(f"Created {os.path.basename(folder)} in {os.path.basename(well)}.")
                os.makedirs(folder)

if __name__ == "__main__":
    main()