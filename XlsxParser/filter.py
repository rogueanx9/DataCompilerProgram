from typing import Any, Callable, List
from utils import IsInt

def FilterCLI(items: List[Any], name_fn: Callable[[Any], Any] = lambda x : x) -> List[Any]:
    filtered_selection = Selector(items, name_fn=name_fn) # Index to filter out, can be negative
    return [items[i] for i in filtered_selection]

def Selector(items: List[Any], name_fn: Callable[[Any], Any] = lambda x : x) -> List[int]:
    PrintItems(items, name_fn=name_fn) # item count start from 1
    selected = [int(_) for _ in input("Select to exclude (e.g. 1,4,6 or -1,4,6 to reverse): ").split(",") if IsInt(_)]

    if any([val < 0 for val in selected]): # Reverse
        filter_fn = lambda id, ids : id in ids
    else:
        filter_fn = lambda id, ids : id not in ids

    return [i for i in range(len(items)) if filter_fn(i + 1, [abs(_) for _ in selected])]

def PrintItems(items: List[Any], col = 2, name_fn: Callable[[Any], Any] = lambda x : x) -> None:
    for i in range(len(items)):
        no = i + 1
        end = "\n" if no % col == 0 or no == len(items) else "  "
        print(f"{no}. {name_fn(items[i])}", end=end)