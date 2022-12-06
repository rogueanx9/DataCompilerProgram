### DECORATOR ONLY ###
from io import TextIOWrapper
from typing import Callable
from utils import StrippedLine

def RecReaderLoop(func: Callable[[object, str, int],None]):
    def wrapper(self: object, f: TextIOWrapper) -> None:
        no_line = 0
        line = StrippedLine(f.readline())
        while(line):
            no_line += 1
            func(self, line, no_line)
            line = StrippedLine(f.readline())
    return wrapper