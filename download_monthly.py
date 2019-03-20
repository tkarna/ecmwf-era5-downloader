import cdsapi
from dateutil.rrule import rrule, MONTHLY
import datetime
from time import time as timer

"""
Download ERA5 output for NemoNordic reference hindcast runs.

Grid used in Nemo 3.6 forecast:

 lat = 82 ;
 lat = 66.15, 65.925, 65.7, 65.475, 65.25, 65.025, 64.8, 64.575, 64.35,
    64.125, 63.9, 63.675, 63.45, 63.225, 63, 62.775, 62.55, 62.325, 62.1,
    61.875, 61.65, 61.425, 61.2, 60.975, 60.75, 60.525, 60.3, 60.075, 59.85,
    59.625, 59.4, 59.175, 58.95, 58.725, 58.5, 58.275, 58.05, 57.825, 57.6,
    57.375, 57.15, 56.925, 56.7, 56.475, 56.25, 56.025, 55.8, 55.575, 55.35,
    55.125, 54.9, 54.675, 54.45, 54.225, 54, 53.775, 53.55, 53.325, 53.1,
    52.875, 52.65, 52.425, 52.2, 51.975, 51.75, 51.525, 51.3, 51.075, 50.85,
    50.625, 50.4, 50.175, 49.95, 49.725, 49.5, 49.275, 49.05, 48.825, 48.6,
    48.375, 48.15, 47.925 ;
 d_lat = 0.225 ;

 lon = 162 ;
 lon = -5.175, -4.95, -4.725, -4.5, -4.275, -4.05, -3.825, -3.6, -3.375,
    -3.15, -2.925, -2.7, -2.475, -2.25, -2.025, -1.8, -1.575, -1.35, -1.125,
    -0.9, -0.675, -0.45, -0.225, 0, 0.225, 0.45, 0.675, 0.9, 1.125, 1.35,
    1.575, 1.8, 2.025, 2.25, 2.475, 2.7, 2.925, 3.15, 3.375, 3.6, 3.825,
    4.05, 4.275, 4.5, 4.725, 4.95, 5.175, 5.4, 5.625, 5.85, 6.075, 6.3,
    6.525, 6.75, 6.975, 7.2, 7.425, 7.65, 7.875, 8.1, 8.325, 8.55, 8.775, 9,
    9.225, 9.45, 9.675, 9.9, 10.125, 10.35, 10.575, 10.8, 11.025, 11.25,
    11.475, 11.7, 11.925, 12.15, 12.375, 12.6, 12.825, 13.05, 13.275, 13.5,
    13.725, 13.95, 14.175, 14.4, 14.625, 14.85, 15.075, 15.3, 15.525, 15.75,
    15.975, 16.2, 16.425, 16.65, 16.875, 17.1, 17.325, 17.55, 17.775, 18,
    18.225, 18.45, 18.675, 18.9, 19.125, 19.35, 19.575, 19.8, 20.025, 20.25,
    20.475, 20.7, 20.925, 21.15, 21.375, 21.6, 21.825, 22.05, 22.275, 22.5,
    22.725, 22.95, 23.175, 23.4, 23.625, 23.85, 24.075, 24.3, 24.525, 24.75,
    24.975, 25.2, 25.425, 25.65, 25.875, 26.1, 26.325, 26.55, 26.775, 27,
    27.225, 27.45, 27.675, 27.9, 28.125, 28.35, 28.575, 28.8, 29.025, 29.25,
    29.475, 29.7, 29.925, 30.15, 30.375, 30.6, 30.825, 31.05 ;
 d_lon = 0.225 ;
"""


def get_month(year, month, filename=None):
    """
    Download one month of ERA5 single level data.
    """
    year_str = str(int(year))
    month_str = '{:02d}'.format(int(month))
    variables = [
        '10m_u_component_of_wind',
        '10m_v_component_of_wind',
        '2m_dewpoint_temperature',
        '2m_temperature',
        'snowfall',
        'surface_pressure',
        'surface_solar_radiation_downwards',
        'surface_thermal_radiation_downward_clear_sky',
        'total_precipitation',
    ]
    # ['01', '02, ..., '31']
    days = ['{:02d}'.format(day) for day in range(1, 32)]
    # ['00:00', '01:00', ..., '23:00']
    times = ['{:02d}:00'.format(hour) for hour in range(24)]
    # area bounds: North, West, South, East. None => global
    area = [66.15, -5.175, 47.925, 31.05]
    # lat/lon grid resolution; None => Native 0.25 x 0.25 for atm
    grid = [0.225, 0.225]
    if filename is None:
        filename = 'reanalysis-era5_{:}-{:}.nc'.format(year_str, month_str)

    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type':'reanalysis',
            'format':'netcdf',
            'variable':variables,
            'year': year_str,
            'month': month_str,
            'day': days,
            'time': times,
            'area': area,
            'grid': grid,
        },
        filename)


start_month = datetime.datetime(2016, 6, 1)
end_month = datetime.datetime(2017, 6, 1)

for date in rrule(MONTHLY, dtstart=start_month, until=end_month):
    print('\nFetching {:}'.format(date.strftime('%Y-%m')))
    tic = timer()
    toc = timer()
    duration = datetime.timedelta(seconds=toc - tic)
    get_month(date.year, date.month)
    print('Duration: {:}'.format(duration))
