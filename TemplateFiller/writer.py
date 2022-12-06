### DECORATOR ONLY ###
## Need decorator from reader as the head of decorator
## @SomeReaderFunc
## @SomeWriterFunc
## def ParseFunc()

from typing import Any, Callable, List

def PBU_Pressure_writer(func: Callable[[object, str],List[Any]]):
    def wrapper(self: object, line: str, no_line: int) -> None:
        pressure_sheet = self.workbook["PRESSURE"]
        data = func(self, line)
        for col in range(len(data)):
            cell = pressure_sheet.cell(no_line + 4, col + 1)
            cell.value = data[col]
    return wrapper