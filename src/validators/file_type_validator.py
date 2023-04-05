import os
from typing import List
from enumerations.file_type import FileType

from .path_validator import PathValidation


class FileTypeValidator:
    def __init__(self, file_path: str, valid_extensions: List[str]):
        self._validate(file_path, valid_extensions)
        self.file_path = file_path

    def __get__(self, instance, owner):
        return self.file_path

    def __set__(self, instance, file_path, valid_extensions: List[str]):
        self._validate(file_path, valid_extensions)
        self.file_path = file_path

    def _validate(self, value: str, valid_extensions: List[str]):
        PathValidation(value)  # check file path is OK or not

        _, ext = os.path.splitext(value)
        if ext not in valid_extensions:
            raise ValueError("unsupported file")
