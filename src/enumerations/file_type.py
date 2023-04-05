import os
from enum import Enum


class FileType(Enum):
    CSV = "csv"
    EXCEL = "excel"

    @staticmethod
    def initiate(file_path: str):
        _, ext = os.path.splitext(file_path)

        if ext == ".csv":
            return FileType.CSV
        elif ext in (".xls", ".xlsx"):
            return FileType.EXCEL
        else:
            raise ValueError("unknown file type")
