import multiprocessing

from src.utilities.pandas_helper import PandasHelper
import pandas as pd
from datetime import datetime
import pycountry_convert as pc


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
def get_continental_from_country(row):
    # do some computation on the row
    try:
        country = row["Country"]

        country_alpha2 = pc.country_name_to_country_alpha2(country)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)

        row["continental"] = country_continent_name

        return row
    except Exception as e:
        return None


def convert_date_time(row):
    # do some computation on the row
    try:
        timestamp = row["InvoiceDate"]
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        week_day = timestamp.strftime("%A")
        am_or_pm = timestamp.strftime("%p")
        week_number = timestamp.strftime("%V")
        year = timestamp.strftime("%Y")
        year_month = timestamp.strftime("%Y/%m")
        year_month_day = timestamp.strftime("%Y/%m/%d")
        year_month_day_hour = timestamp.strftime("%Y/%m/%d %H")
        year_month_day_hour_min = timestamp.strftime("%Y/%m/%d %H:%M")
        time_str = timestamp.strftime("%H:%M")

        row["year"] = year
        row["year_month"] = year_month
        row["year_month_day"] = year_month_day
        row["year_month_day_hour"] = year_month_day_hour
        row["year_month_day_hour_min"] = year_month_day_hour_min
        row["time_str"] = time_str
        row["year_month_day_hour_min"] = year_month_day_hour_min
        row["am_or_pm"] = am_or_pm
        row["week_day"] = week_day
        row["week_number"] = week_number

        return row
    except Exception as e:
        print(e)
        raise e


def add_dim_date_to_df(df: pd.DataFrame) -> pd.DataFrame:
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
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:

        df = pd.DataFrame(
            pool.map(
                convert_date_time,
                [row for index, row in df.iterrows()],
            )
        )

        print("timestamp column process completed ...")
        return df

def add_continent_to_df(df: pd.DataFrame) -> pd.DataFrame:
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
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:

        df = pd.DataFrame(
            pool.map(
                get_continental_from_country,
                [row for index, row in df.iterrows()],
            )
        )

        print("timestamp column process completed ...")
        return df


if __name__ == "__main__":

    base_data_sources_folder: str = "../dataset"
    main_data_source = "merged_data.csv"

    # 1-merge all different data together
    merged_df = merge_data_frames(file_path=f"{base_data_sources_folder}/dataset.xlsx")

    # 2-export data to CSV file
    write_data_frame_to_csv(merged_df, f"{base_data_sources_folder}/{main_data_source}")

    # 3- load the merged data to memory
    data_source: pd.DataFrame = pd.read_csv(
        f"{base_data_sources_folder}/{main_data_source}"
    )
    new_dataframe = add_dim_date_to_df(data_source)

    # 4- save the new dataframe to csv file
    write_data_frame_to_csv(
        new_dataframe, f"{base_data_sources_folder}/{main_data_source}"
    )

   # 5- load the merged data to memory
    data_source: pd.DataFrame = pd.read_csv(
        f"{base_data_sources_folder}/{main_data_source}"
    )
    new_dataframe = add_continent_to_df(data_source)

    # 6- save the new dataframe to csv file
    write_data_frame_to_csv(
        new_dataframe, f"{base_data_sources_folder}/{main_data_source}"
    )
