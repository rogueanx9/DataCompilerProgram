from typing import List

def Choose(options: dict) -> int:
    keys = list(options.keys())

    valid = False
    while(not valid):
        selected = ConvertInt(input(f"Select one from {keys[0]} to {keys[-1]}: "))
        if selected in keys:
            break
        print(f"You can only input from {keys[0]} to {keys[-1]}. Please retry!")
    return selected

def ConvertInt(text: str):
    try:
        return int(text)
    except:
        return -9999

def Options(options: List) -> dict:
    options_dict = {i+1:options[i] for i in range(len(options))}
    for i, option in options_dict.items():
        end = "\n" if i % 3 == 0 or i == len(options) else "  "
        print(f"{i}. {option}", end=end)
    return options_dict

def StrippedLine(line: str):
    return line.lstrip().rstrip()