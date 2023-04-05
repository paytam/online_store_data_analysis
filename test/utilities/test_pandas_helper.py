import pytest
from src.utilities.pandas_helper import PandasHelper
import random

@pytest.fixture()
def pandas_helper():
    return PandasHelper("../dataset/dataset.xlsx")

def test_pandas_helper_invalid_file_path():
    with pytest.raises(ValueError):
        PandasHelper(file_path="x.p")

def test_pandas_helper_invalid_file_type():
    with pytest.raises(ValueError):
        PandasHelper(file_path="./test_pandas_helper.py")


def test_pandas_helper_get_df(pandas_helper):
    assert pandas_helper.df is not None

def test_pandas_helper_get_df_columns(pandas_helper):
    assert len(pandas_helper.columns)>0


def test_pandas_helper_get_df_unique_values(pandas_helper):
    columns=pandas_helper.columns
    uniques=pandas_helper.get_unique_values(random.choice(columns))
    assert len(uniques)>0
