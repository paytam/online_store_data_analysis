import multiprocessing
from typing import List

from src.utilities.pandas_helper import PandasHelper
import pandas as pd
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
from multiprocessing import Pool
from countryinfo import CountryInfo


def merge_data_frames(file_path: str) -> pd.DataFrame:
    """
    In order to read all data in the source excel file and the merge all together and save it
    as a output file

    Args:
        file_path: the file path of data source
    :return:
    :rtype:
    """
    df_2009: pd.DataFrame = PandasHelper(file_path, sheet_name="Year 2009-2010").df
    print("2009 data loaded")
    df_2010: pd.DataFrame = PandasHelper(file_path, sheet_name="Year 2010-2011").df
    print("2010 data loaded")
    result = pd.concat([df_2009, df_2010])
    print("data merged completed!!!!")
    return result


def write_data_frame_to_csv(df: pd.DataFrame, file_path: str):
    """
    export data set to csv file, in the given file path
    :param df:
    :type df:
    :param file_path:
    :type file_path:
    :return:
    :rtype:
    """
    df.to_csv(file_path)

    print("exporting file to csv completed...")


# define a function to apply to each row
def convert_date_time(time_stamp_column_name, index, row):
    # do some computation on the row
    timestamp = row[time_stamp_column_name]
    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    week_day = timestamp.strftime("%A")
    am_or_pm = timestamp.strftime("%p")
    year = timestamp.strftime("%Y")
    year_month = timestamp.strftime("%Y/%m")
    year_month_day = timestamp.strftime("%Y/%m/%d")
    year_month_day_hour = timestamp.strftime("%Y/%m/%d %H")
    year_month_day_hour_min = timestamp.strftime("%Y/%m/%d %H:%M")
    time = timestamp.strftime("%H:%M")
    print(f"row index {index} processed!!")

    return pd.Series(
        [
            year,
            year_month,
            year_month_day,
            year_month_day_hour,
            year_month_day_hour_min,
            time,
            week_day,
            am_or_pm,
        ]
    )


def add_dim_date_to_df(df: pd.DataFrame, time_stamp_column_name: str) -> pd.DataFrame:
    """
    split the timestamp column and then add new columns to dataframe.

    :param df:
    :type df:
    :param time_stamp_column_name: the timestamp column name
    :type time_stamp_column_name:
    :return:
    :rtype:
    """
    # create a pool of processes
    pool = Pool(multiprocessing.cpu_count())

    df[
        [
            "year",
            "year_month",
            "year_month_day",
            "year_month_day_hour",
            "year_month_day_hour_min",
            "time",
            "week_day",
            "am_or_pm",
        ]
    ] = pool.map(
        convert_date_time,
        [(time_stamp_column_name, index, row) for index, row in df.iterrows()],
    )

    print("timestamp column process completed ...")
    return df


if __name__ == "__main__":

    base_data_sources_folder: str = "../dataset"
    main_data_source = "merged_data.csv"

    # 1-merge all different data together
    # merged_df = merge_data_frames(file_path=f"{base_data_sources_folder}/dataset.xlsx")

    # 2-export data to CSV file
    # write_data_frame_to_csv(merged_df, f"{base_data_sources_folder}/{main_data_source}")

    # 3- load the merged data to memory
    data_source: pd.DataFrame = pd.read_csv(
        f"{base_data_sources_folder}/{main_data_source}"
    )
    new_dataframe = add_dim_date_to_df(data_source, "InvoiceDate")

    # 4- save the new dataframe to csv file
    write_data_frame_to_csv(
        new_dataframe, f"{base_data_sources_folder}/{main_data_source}"
    )
