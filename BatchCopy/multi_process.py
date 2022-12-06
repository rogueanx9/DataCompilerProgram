import threading

class MultiProcess():
    PROCESSES = 0
    POOL = threading.get_ident()

    def __init__(self) -> None:
        pass

    @classmethod
    def Print(cls, msg: str):
        if cls.PROCESSES:
            print(f"[{cls.POOL}] {msg}")
        else:
            print(msg)

    @classmethod
    def PrintPool(cls):
        if cls.PROCESSES:
            print(f"[{cls.POOL}]", end=" ")