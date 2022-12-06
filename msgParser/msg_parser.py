import extract_msg

from utils import Abspath

def main():
    msg_path = Abspath("Input msg path: ")
    msg = extract_msg.openMsg(msg_path)
    msg.save(zip="C:\\Users\\Rogan\\Documents\\DataCompilerProgram\\msgParser")

if __name__ == "__main__":
    main()