import pandas as pd
from datetime import date, timedelta

from astral import LocationInfo
from astral.sun import sun
from multiprocessing import Pool
from countryinfo import CountryInfo
import itertools
def get_capital_by_country_name(country_name):
    try:
        # Search for the country using its name
        return CountryInfo(country_name).capital()
    except Exception:
        # Handle case where the country does not exist in the library
        return None

def convert_date_time(row):
    # do some computation on the row
    timestamp = row["InvoiceDate"]
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

if __name__ == '__main__':
    sdate = date(2009,1,1)   # start date
    edate = date(2011,12,31)   # end date

    dates=pd.date_range(sdate,edate-timedelta(days=1),freq='d').to_list()

    df: pd.DataFrame = pd.read_csv("../dataset/merged_data.csv")
    countries=df['Country'].unique().tolist()
    capitals=[get_capital_by_country_name(country) for country in countries]

    dim_date=pd.DataFrame(itertools.product(dates,countries))
    print(*zip(countries,capitals), sep='\n')
    # print(*df,sep='\n')