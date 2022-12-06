from collections import defaultdict
from utils import *
import xlsxwriter
import os

class RecReader():
    def __init__(self, file, write_to_xlsx: bool = True) -> None:
        self.file = file
        self.file_name = file.split("\\")[-1].split(".")[0]
        self.folder = "\\".join(file.split("\\")[:-1])
        self.default_save = os.path.abspath("C:\\Users\\Rogan\\Documents\\RecReader\\Result")
        self.write_to_xlsx = write_to_xlsx

        if write_to_xlsx:
            self.workbook = xlsxwriter.Workbook(os.path.join(self.folder, f"{self.file_name}.xlsx"))
            self.worksheet = self.workbook.add_worksheet()
            self.last_row = 0

    def Parse(self):
        with open(self.file) as f:
            num_line = self.PrintHeader(f)
            num_line = self.WriteDataToXlsx(f, no=num_line)
        self.CloseWorkbook()

    def CloseWorkbook(self):
        self.workbook.close()
        print(f"Saved xlsx file as {self.file_name}.xlsx on {self.folder}")

    # @WriteToXlsxData
    # @ReadLoopData
    @ReadLoop
    @WriteToXlsx
    def PrintHeader(self, f: TextIOWrapper, line: str, no: int):
        line = [StrippedLine(x) for x in line.split(":")]
        PrintList(line, end=": ")
        return line

    # @WriteToXlsxData
    # @ReadLoopData
    @ReadLoop
    @WriteToXlsx
    def WriteDataToXlsx(self, f: TextIOWrapper, line: str, no: int):
        line = [float(x) for x in line.split() if IsFloat(x)]
        return line