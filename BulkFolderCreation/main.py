import os
from glob import glob

def main():
    SRC_PATH = input("Input source folder: ") if False else "\\\\Tenfps1vfs\\ptdm\\00-E-FILE\\TARAKAN\\FIELD"
    SRC_FOLDERS = glob(os.path.join(SRC_PATH, "*"))

    wells = []
    for folder in SRC_FOLDERS:
        wells += [well for well in glob(os.path.join(folder, "WELL/*"))]

    DST_PATH = input("Input destination folder: ") if False else "\\\\Tenfps1vfs\\ptdm\\05-DATA\\DATA COMPILING\\USER GUIDE\\Data Compiling - Rogan Steeven Saulus\\Block Tarakan"

    for well in wells:
        field = os.path.join(DST_PATH, well.split("\\")[-3])
        if not os.path.exists(field):
            os.mkdir(field)

        well = os.path.join(field, well.split("\\")[-1])
        if not os.path.exists(well):
            os.mkdir(well)

if __name__ == "__main__":
    main()