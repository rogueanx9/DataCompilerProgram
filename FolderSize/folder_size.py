from utils import Abspath, ConvertBytes, MEDIA_FILES
from glob import iglob
import os

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        print(f"Current entry: {entry.name[:15]} ... {entry.name[-15:]}", end='\r')
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            # Ignore Media Files
            if os.path.splitext(entry.path)[1].lower() in MEDIA_FILES:
                continue
            
            total += entry.stat(follow_symlinks=False).st_size
    return total

def main():
    SRC = [
        "\\\\jktbbfs1\\shared\\MAXWELL\\DRL_Wel1_Operated\\Block_B",
        "\\\\jktbbfs1\\shared\\MAXWELL\\DRL_Wel1_Operated\\MADURA",
        "\\\\jktbbfs1\\shared\\MAXWELL\\DRL_Wel1_Operated\\SAMPANG"
        ]
        
    # while input("Add folder? ").lower() in ["y", ""]:
    #    SRC.append(Abspath("Input folder to check size: "))

    total_size = 0
    for folder in SRC:
        print(f"Current folder: {os.path.basename(folder)}")
        total_size += get_tree_size(folder)
    print(f"Total size: {ConvertBytes(total_size)}")

if __name__ == "__main__":
    main()
