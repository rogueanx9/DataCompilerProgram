from io import TextIOWrapper
from typing import Any, Callable, List
import xlsxwriter
from tqdm import tqdm
import os

def IsInt(num: str):
    try:
        int(num)
    except:
        return False
    return True

def IsFloat(num: str):
    try:
        float(num)
    except:
        return False
    return True

def PrintDict(dict: dict):
    for k,v in dict.items():
        print(f"{k}: {v}")

def PrintList(list: List, end: str = " "):
    for i in range(len(list)):
        if i < len(list) - 1:
            print(list[i], end=end)
        else:
            print(list[i])

def ReadLoop(func):
    def wrapper(self, f: TextIOWrapper, line: str = "", no: int = 0):
        line = StrippedLine(f.readline())
        while(line):
            no += 1
            func(self, f, line, no)
            line = StrippedLine(f.readline())
        return no
    return wrapper

def ReadLoopData(func):
    def wrapper(self, f: TextIOWrapper, line: str = "", no: int = 0):
        datas = []
        line = StrippedLine(f.readline())
        while(line):
            no += 1
            data = func(self, f, line, no)
            line = StrippedLine(f.readline())
            datas.append(data)
        return no, datas
    return wrapper

def StrippedLine(text: str):
    return text.lstrip().rstrip()

def WriteToXlsxData(func):
    def wrapper(self, f: TextIOWrapper, line: str = "", no: int = 0):
        no, datas = func(self, f, line, no)

        if self.write_to_xlsx:
            print("Writing to xlsx...")
            for i in tqdm(range(len(datas))):
            # for i in range(len(datas)):
                for j in range(len(datas[i])):
                    # print(datas[i][j], end=" ")
                    self.worksheet.write(self.last_row + i, j, datas[i][j])
            self.last_row = no
        else:
            print("Please set write_to_xlsx flag to True.")

        return no
    return wrapper

def WriteToXlsx(func: Callable[[Any], List]):
    def wrapper(self, f: TextIOWrapper, line: str = "", no: int = 0):
        data = func(self, f, line, no)

        if self.write_to_xlsx:
            for i in range(len(data)):
                self.worksheet.write(no, i, data[i])
        else:
            print("Please set write_to_xlsx flag to True.")

    return wrapper