import os
from datetime import datetime
from typing import Any, List
import xlsxwriter
from utils import IsFloat

class ExcelWriter:
    def __init__(self, path: str, name: str) -> None:
        self.path = path
        self.name = name
        self.workbook = xlsxwriter.Workbook(os.path.join(path, name + ".xlsx"))
        self.worksheet = self.workbook.add_worksheet()
        self.row = 1
        self.col = 1

    def CreateHeaderColumn(self, col_names: List[str]) -> None:
        for i in range(len(col_names)):
            self.worksheet.write(0, i, col_names[i])
        self.NextRow()

    def Write(self, row: int = 0, col: int = 0, value: str = "") -> None:
        row = row if row > 0 else self.row
        col = col if col > 0 else self.col

        self.worksheet.write(row - 1, col - 1, value)

    def WriteDate(self, row: int = 0, col: int = 0, value: str = "") -> None:
        if IsFloat(value): self._WriteDateLegacy(row, col, value)
        else:              self._WriteDate(row, col, value)

    def WriteNumber(self, row: int = 0, col: int = 0, value: str = "") -> None:
        row = row if row > 0 else self.row
        col = col if col > 0 else self.col

        self.worksheet.write_number(row - 1, col - 1, float(value))

    def Save(self) -> None:
        print(f"Saved {self.name}.xlsx in {self.path}")
        self.workbook.close()

    def NextRow(self):
        self.row = self.row + 1

    def NextCol(self):
        self.col = self.col + 1

    def _WriteDate(self, row: int = 0, col: int = 0, value: str = "") -> None:
        row = row if row > 0 else self.row
        col = col if col > 0 else self.col

        # Assume it is a correct format from Excel
        try:
            date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            date = datetime.strptime("2040-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')

        format = self.workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
        self.worksheet.write_datetime(row - 1, col - 1, date, format)

    def _WriteDateLegacy(self, row: int = 0, col: int = 0, value: str = "") -> None:
        row = row if row > 0 else self.row
        col = col if col > 0 else self.col

        format = self.workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
        self.worksheet.write(row - 1, col - 1, float(value), format)