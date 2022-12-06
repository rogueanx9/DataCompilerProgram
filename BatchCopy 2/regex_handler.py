
def RegexHandler(path: str) -> str:
    if "[" in path or "]" in path:
        path = SquareBracketHandler(path)
    return path

def SquareBracketHandler(path: str) -> str:
    newPath = ""
    for char in path:
        if char == '[' or char == ']':
            newPath += "[" + char + "]"
        else:
            newPath += char
    return newPath