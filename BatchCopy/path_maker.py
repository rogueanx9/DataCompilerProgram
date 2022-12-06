import os
from glob import glob
from typing import List

from utils import *
from exclude_folder import ExcludeLoop

class PathMaker():
    RELEASE = True

    def __init__(self, message: str, default_path: str) -> None:
        self.base_path = Abspath(message) if self.RELEASE else default_path
        self.folders_in_base_path = [folder for folder in glob(os.path.join(self.base_path, "*")) if os.path.isdir(folder)]

    def ExcludeLoop(self, to_compare: List[str], message: str):
        self.folders_in_base_path = ExcludeLoop(self.folders_in_base_path, to_compare, message)

    def TargetRelPath(self, message: str, default_path: str):
        self.target_rel_path = Relpath(message) if self.RELEASE else default_path