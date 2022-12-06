import os

def Abspath(msg: str) -> str:
    path = input(msg)
    while not path:
        print("[W] You cannot input empty string.")
        path = input(msg)
    return os.path.abspath(path)