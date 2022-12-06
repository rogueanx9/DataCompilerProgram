from rec_reader import RecReader
from glob import glob
import os
from tqdm import tqdm

def main():
    base_path = os.path.abspath(input("Input your well directory: "))
    wells = [well for well in glob(os.path.join(base_path, "*"))]

    print("Reading files...")
    files = []
    for well in tqdm(wells):
        files += [file for file in glob(os.path.join(well, "**"), recursive=True) if os.path.isfile(file) and ".rec" in file.split("\\")[-1]]

    # print([file.split("\\")[-1] for file in files])
    print("Rewrite .rec files to .xlsx files")
    for file in files:
        print(file)
        reader = RecReader(file)
        reader.Parse()
        break

def main2():
    PATH = os.path.abspath(input("Input your well directory: "))
    files = glob(os.path.join(PATH, "*.txt"))
    
    for file in files:
        reader = RecReader(file)
        reader.Parse()

if __name__ == '__main__':
    main2()

