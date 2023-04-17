#
# step one: read all the data sources
# step two: try to add new column based on value on each row
# step three: save the result
from typing import List

from src.utilities.pandas_helper import PandasHelper
import pandas as pd
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
from multiprocessing import Pool
from countryinfo import CountryInfo

def merge_data_frames() -> None:
    """
    In order to read all data in the source excel file and the merge all together and save it
    as a output file
    :return:
    :rtype:
    """
    file_path = file_path = "../../dataset/dataset.xlsx"
    df_2009:pd.DataFrame=PandasHelper(file_path, sheet_name='Year 2009-2010').df
    print("2009 data loaded")
    df_2010:pd.DataFrame=PandasHelper(file_path, sheet_name='Year 2010-2011').df
    print("2010 data loaded")
    result = pd.concat([df_2009, df_2010])
    print("data merged")
    result.to_csv('../../dataset/merged_data.csv')



# define a function to apply to each row
def convert_date_time(row):
    # do some computation on the row
    timestamp = row["InvoiceDate"]
    timestamp=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    week_day = timestamp.strftime("%A")
    am_or_pm = timestamp.strftime("%p")
    year = timestamp.strftime("%Y")
    year_month = timestamp.strftime("%Y/%m")
    year_month_day = timestamp.strftime("%Y/%m/%d")
    year_month_day_hour = timestamp.strftime("%Y/%m/%d %H")
    year_month_day_hour_min = timestamp.strftime("%Y/%m/%d %H:%M")
    time = timestamp.strftime("%H:%M")

    capital=get_capital_by_country_name(row['Country'])
    location_info=LocationInfo(capital,row['Country'])
    s=sun(location_info.observer, date=timestamp)

    dawn = s["dawn"].strftime("%H:%M")
    sunrise = s["sunrise"].strftime("%H:%M")
    noon = s["noon"].strftime("%H:%M")
    sunset = s["sunset"].strftime("%H:%M")
    dusk = s["dusk"].strftime("%H:%M")

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
            dawn,
            sunrise,
            noon,
            sunset,
            dusk,
            capital,
        ]
    )


if __name__ == "__main__":
    # create a pool of processes
    pool=Pool()

    # merge_data_frames()

    df:pd.DataFrame=pd.read_csv("../dataset/merged_data.csv")

    print(*df['Country'].unique().tolist(),sep='\n')

    #
    # start=datetime.now()
    # df[
    #     [
    #         "year",
    #         "year_month",
    #         "year_month_day",
    #         "year_month_day_hour",
    #         "year_month_day_hour_min",
    #         "time",
    #         "week_day",
    #         "am_or_pm",
    #         'dawn',
    #         "sunrise",
    #         'noon',
    #         'sunset',
    #         'dusk',
    #         'capital',
    #
    #     ]
    # ] = pool.map(convert_date_time, [row for index, row in df.iterrows()])
    # finish=datetime.now()
    # df.to_csv('../../dataset/added.csv')
    # print(finish-start)
    #
    #
    #
