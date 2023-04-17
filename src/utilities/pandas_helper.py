from typing import List, Optional

import pandas as pd

from validators.path_validator import PathValidation
from validators.file_type_validator import FileTypeValidator
from enumerations.file_type import FileType


class PandasHelper:
    VALID_EXTENSIONS = [".csv", ".xlsx", ".xls"]
    _file_path: PathValidation
    _file_type:FileType
    _df: pd.DataFrame
    _sheet_name=Optional[str]

    def __init__(self, file_path, sheet_name:Optional[str]=None) -> None:
        # check file path existed
        self._file_path = PathValidation(file_path)

        # check valid file extension
        FileTypeValidator(file_path=self.file_path, valid_extensions=self.VALID_EXTENSIONS)

        # guess file type
        self._file_type:FileType=FileType.initiate(file_path=self.file_path)
        self._sheet_name=sheet_name

        self._load_dataframe_in_memory()

    def _load_dataframe_in_memory(self):

        if self._file_type == FileType.CSV:
            self._df = pd.read_csv(self.file_path)
        elif self._file_type == FileType.EXCEL:
            if self._sheet_name is not None:
                self._df = pd.read_excel(self.file_path,sheet_name=self._sheet_name)
            else:
                self._df = pd.read_excel(self.file_path)

    @property
    def file_path(self) -> str:
        return self._file_path.value

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def columns(self) -> List[str]:
        return list(self.df.columns)

    @property
    def file_type(self) -> FileType:
        return self._file_type

    def get_unique_values(self,column:str)->List:
        if column not in self.columns:
            raise ValueError(f"invalid column! columns must be one of {self.columns}")

        return list(self.df[column].unique())
