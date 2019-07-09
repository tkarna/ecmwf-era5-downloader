"""
Download ERA5 output for NemoNordic reference hindcast runs.

The ERA5 HRES atmospheric data has a resolution of 31km, 0.28125 degrees.
For sub-daily data for the HRES (stream=oper/wave) the analyses (type=an) are
available hourly.

Downloaded ERA 5 parameters are:

10 metre U wind component,            m s**-1,  10u, 165, instantaneous
10 metre V wind component,            m s**-1,  10v, 166, instantaneous
2 metre temperature,                        K,   2t, 167, instantaneous
2 metre dewpoint temperature,               K,   2d, 168, instantaneous
Surface pressure,                          Pa,   sp, 134, instantaneous
Snowfall,               m of water equivalent,   sf, 144, accumulation
Total precipitation,                        m,   tp, 228, accumulation
Surface solar radiation downwards,    J m**-2, ssrd, 169, accumulation
Surface thermal radiation downwards,  J m**-2, strd, 175, accumulation

Accumulation:

HRES: accumulations are over the hour ending at the forecast step

Radiation fields have units J m**-2, i.e. radiation accumulated over 1 h.
To deaccumulate divide by 3600 s.
See:  https://confluence.ecmwf.int/pages/viewpage.action?pageId=104241513

Snowfall and total precipitation have units m/step, step being 1 h.
Nemo needs units kg/m^2/s. To deaccumulate divide by 3.6.

Final variables are:
u10:        10 metre U wind component (m s**-1)
v10:        10 metre V wind component (m s**-1)
d2m:        2 metre dewpoint temperature (K)
t2m:        2 metre temperature (K)
sp:         surface_air_pressure (Pa)
sf:         Snowfall (m of water equivalent)
tp:         Total precipitation (m)
ssrd:       Surface solar radiation downwards (J m**-2)
strd:       Surface thermal radiation downwards (J m**-2)
deacc_ssrd: Surface solar radiation downwards (W m-2)
deacc_strd: Surface thermal radiation downwards (W m-2)
deacc_tp:   Total precipitation (kg m-2 s-1)
deacc_sf:   Snowfall (kg m-2 s-1)
q2:         2 m specific humidity (g/g)

Data will be downloaded on grid:
(same as in FMI EC forecast)

 latitude = 161 ;
 latitude = 66, 65.8875, 65.775, 65.6625, 65.55, 65.4375, 65.325, 65.2125,
    65.1, 64.9875, 64.875, 64.7625, 64.65, 64.5375, 64.425, 64.3125, 64.2,
    64.0875, 63.975, 63.8625, 63.75, 63.6375, 63.525, 63.4125, 63.3, 63.1875,
    63.075, 62.9625, 62.85, 62.7375, 62.625, 62.5125, 62.4, 62.2875, 62.175,
    62.0625, 61.95, 61.8375, 61.725, 61.6125, 61.5, 61.3875, 61.275, 61.1625,
    61.05, 60.9375, 60.825, 60.7125, 60.6, 60.4875, 60.375, 60.2625, 60.15,
    60.0375, 59.925, 59.8125, 59.7, 59.5875, 59.475, 59.3625, 59.25, 59.1375,
    59.025, 58.9125, 58.8, 58.6875, 58.575, 58.4625, 58.35, 58.2375, 58.125,
    58.0125, 57.9, 57.7875, 57.675, 57.5625, 57.45, 57.3375, 57.225, 57.1125,
    57, 56.8875, 56.775, 56.6625, 56.55, 56.4375, 56.325, 56.2125, 56.1,
    55.9875, 55.875, 55.7625, 55.65, 55.5375, 55.425, 55.3125, 55.2, 55.0875,
    54.975, 54.8625, 54.75, 54.6375, 54.525, 54.4125, 54.3, 54.1875, 54.075,
    53.9625, 53.85, 53.7375, 53.625, 53.5125, 53.4, 53.2875, 53.175, 53.0625,
    52.95, 52.8375, 52.725, 52.6125, 52.5, 52.3875, 52.275, 52.1625, 52.05,
    51.9375, 51.825, 51.7125, 51.6, 51.4875, 51.375, 51.2625, 51.15, 51.0375,
    50.925, 50.8125, 50.7, 50.5875, 50.475, 50.3625, 50.25, 50.1375, 50.025,
    49.9125, 49.8, 49.6875, 49.575, 49.4625, 49.35, 49.2375, 49.125, 49.0125,
    48.9, 48.7875, 48.675, 48.5625, 48.45, 48.3375, 48.225, 48.1125, 48 ;
 d_lat = 0.1125 ;

 longitude = 175 ;
 longitude = -5, -4.793103, -4.586207, -4.37931, -4.172414, -3.965517,
    -3.758621, -3.551724, -3.344828, -3.137931, -2.931035, -2.724138,
    -2.517241, -2.310345, -2.103448, -1.896552, -1.689655, -1.482759,
    -1.275862, -1.068966, -0.862069, -0.6551724, -0.4482759, -0.2413793,
    -0.03448276, 0.1724138, 0.3793103, 0.5862069, 0.7931035, 1, 1.206897,
    1.413793, 1.62069, 1.827586, 2.034483, 2.241379, 2.448276, 2.655172,
    2.862069, 3.068965, 3.275862, 3.482759, 3.689655, 3.896552, 4.103448,
    4.310345, 4.517241, 4.724138, 4.931035, 5.137931, 5.344828, 5.551724,
    5.758621, 5.965517, 6.172414, 6.37931, 6.586207, 6.793103, 7, 7.206897,
    7.413793, 7.62069, 7.827586, 8.034483, 8.24138, 8.448276, 8.655172,
    8.862069, 9.068966, 9.275862, 9.482759, 9.689655, 9.896552, 10.10345,
    10.31034, 10.51724, 10.72414, 10.93103, 11.13793, 11.34483, 11.55172,
    11.75862, 11.96552, 12.17241, 12.37931, 12.58621, 12.7931, 13, 13.2069,
    13.41379, 13.62069, 13.82759, 14.03448, 14.24138, 14.44828, 14.65517,
    14.86207, 15.06897, 15.27586, 15.48276, 15.68966, 15.89655, 16.10345,
    16.31034, 16.51724, 16.72414, 16.93103, 17.13793, 17.34483, 17.55172,
    17.75862, 17.96552, 18.17241, 18.37931, 18.58621, 18.7931, 19, 19.2069,
    19.41379, 19.62069, 19.82759, 20.03448, 20.24138, 20.44828, 20.65517,
    20.86207, 21.06897, 21.27586, 21.48276, 21.68966, 21.89655, 22.10345,
    22.31034, 22.51724, 22.72414, 22.93103, 23.13793, 23.34483, 23.55172,
    23.75862, 23.96552, 24.17241, 24.37931, 24.58621, 24.7931, 25, 25.2069,
    25.41379, 25.62069, 25.82759, 26.03448, 26.24138, 26.44828, 26.65517,
    26.86207, 27.06897, 27.27586, 27.48276, 27.68966, 27.89655, 28.10345,
    28.31034, 28.51724, 28.72414, 28.93103, 29.13793, 29.34483, 29.55172,
    29.75862, 29.96552, 30.17241, 30.37931, 30.58621, 30.7931, 31 ;
 d_lon = 0.20689655172413793
"""
import cdsapi
from dateutil.rrule import rrule, MONTHLY
import datetime
from time import time as timer
import numpy
import netCDF4
import os


def download_month(year, month, output_file=None):
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
        'surface_pressure',
        'snowfall',
        'total_precipitation',
        'surface_solar_radiation_downwards',
        'surface_thermal_radiation_downwards',
    ]
    # ['01', '02, ..., '31']
    days = ['{:02d}'.format(day) for day in range(1, 32)]
    # ['00:00', '01:00', ..., '23:00']
    times = ['{:02d}:00'.format(hour) for hour in range(24)]
    # area bounds: North, West, South, East. None => global
    area = [66, -5, 48, 31]
    # lat/lon grid resolution; None => Native 0.25 x 0.25 for atm
    grid = [0.20689655172413793, 0.1125]
    if output_file is None:
        output_file = 'era5_y{:}m{:}.nc'.format(year_str, month_str)

    client = cdsapi.Client()
    product = 'reanalysis-era5-single-levels'
    request = {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': variables,
        'year': year_str,
        'month': month_str,
        'day': days,
        'time': times,
        'area': area,
        'grid': grid,
    }

    # download to tmp file
    tmp_file = 'tmp_' + output_file
    client.retrieve(product, request, tmp_file)
    # copy to convert all variables to float datatype
    convert_to_float(tmp_file, output_file,
                     rm_source_file=True, verbose=False)
    # deaccumulate accumulated fields
    deaccumulate_fields(output_file, ['ssrd', 'strd', 'tp', 'sf'])
    # compute specific humidity
    compute_specific_humidity(output_file)
    return output_file


def convert_to_float(input_file, output_file, rm_source_file=False,
                     verbose=True):
    """
    Copy netCDF file and convert all variables to float data type.

    :arg str input_file: name of the input file
    :arg str output_file: name of the output file
    :kwarg rm_source_file: if True, removes the source file when finished
    """
    if verbose:
        print('Copying to {:}'.format(output_file))

    # open multi-file dataset and copy it to a output dataset
    with netCDF4.Dataset(input_file) as src, netCDF4.Dataset(output_file, 'w') as dst:
        # copy global attributes all at once via dictionary
        for key in src.__dict__:
            if key[0] != '_':
                dst.setncattr(key, src.__dict__[key])
        # copy dimensions
        for name, dimension in src.dimensions.items():
            size = len(dimension) if not dimension.isunlimited() else None
            if name == 'time':
                size = None  # ensure time dim is unlimited
            dst.createDimension(name, (size))
        # copy all variables
        for name, variable in src.variables.items():
            dtype = numpy.float32
            dst.createVariable(name, dtype, variable.dimensions)
            dst[name][:] = variable[:]
            # copy variable attributes
            for key in variable.__dict__:
                if key[0] != '_' and key not in ['scale_factor', 'add_offset', 'missing_value']:
                    try:
                        dst[name].setncattr(key, variable.__dict__[key])
                    except TypeError:
                        # silently omit attributes with unsupported data type
                        pass

    if rm_source_file:
        if os.path.isfile(input_file):
            os.remove(input_file)


def deaccumulate_fields(ncfile, varname_list):
    """
    Deaccumulate fields that have been accumulated over time.

    Creates a new variable "deacc_X" where X is the original variable name.

    Era5 HRES: variables have been accumulated over 1 h.

    See:
    https://confluence.ecmwf.int/pages/viewpage.action?pageId=56658233
    https://apps.ecmwf.int/codes/grib/param-db?id=169
    """
    with netCDF4.Dataset(ncfile, 'r+') as src:
        src.set_auto_scale(False)
        time = src['time'][:]
        assert src['time'].units.split(' ')[0] == 'hours'
        timestep = numpy.diff(time)
        assert numpy.allclose(timestep, timestep[0]*numpy.ones_like(timestep))
        timestep = timestep[0]
        for varname in varname_list:
            scalar_dict = {
                'ssrd': 3600.,
                'strd': 3600.,
                'tp': 3.6,
                'sf': 3.6,
            }
            assert varname in scalar_dict, 'Scalar undefined for {:}'.format(varname)
            scalar = scalar_dict[varname]
            var = src[varname]
            newvarname = 'deacc_' + varname
            if newvarname not in src.variables:
                src.createVariable(newvarname, var.dtype, var.dimensions)
            newvar = src[newvarname]
            vals = var[:].astype(numpy.float32)
            newvar[:] = vals/scalar
            # copy variable attributes
            for key in var.ncattrs():
                if key[0] != '_' and key not in ['scale_factor', 'add_offset', 'missing_value']:
                    newvar.setncattr(key, var.getncattr(key))
            units = {
                'ssrd': 'W m-2',
                'strd': 'W m-2',
                'tp': 'kg m-2 s-1',
                'sf': 'kg m-2 s-1',
            }
            if varname in units:
                newvar.setncattr('units', units[varname])


def specific_humidity(T, p):
    """
    Compute specific humidity from dew point temperature and surface pressure.

    Specific humidity is calculated over water and ice using equations 7.4 and
    7.5 from Part IV, Physical processes section (Chapter 7, section 7.2.1b) in
    the documentation of the IFS for CY41R2. Use the 2m dew point temperature
    and surface pressure (which is approximately equal to the pressure at 2m)
    in these equations. The constants in 7.4 are to be found in Chapter 12
    (of Part IV: Physical processes) and the parameters in 7.5 should be set
    for saturation over water because the dew point temperature is being used.

    See: https://confluence.ecmwf.int/display/CKB/ERA+datasets%3A+near-surface+humidity
    See: https://www.ecmwf.int/en/elibrary/16648-part-iv-physical-processes

    :arg T: dew point temperature in Kelvins (numpy array)
    :arg p: surface pressure in Pascals (numpy array)

    :returns: specific humidity in a numpy array
    """
    R_dry = 287.0597
    R_vap = 461.5250
    T0 = 273.16
    a1 = 611.21
    # a3 and a4 for over water
    a3 = 17.502
    a4 = 32.19
    # eq 7.5
    e_sat = a1 * numpy.exp(a3 * (T - T0)/(T - a4))
    # eq 7.4
    r = R_dry/R_vap
    q_sat = r * e_sat / (p - (1 - r)*e_sat)
    return q_sat


def compute_specific_humidity(ncfile, dewp_varname='d2m', spres_varname='sp',
                              shumi_varname='q2'):
    """
    Compute specific humidity from dewpoint and surface pressure fields.
    """
    with netCDF4.Dataset(ncfile, 'r+') as src:
        q2 = src.createVariable(shumi_varname, numpy.float32,
                                ('time', 'latitude', 'longitude', ))
        q2.units = 'g/g'
        q2.long_name = '2 m specific humidity'

        d2m = src.variables[dewp_varname]
        sp = src.variables[spres_varname]
        for i in range(d2m.shape[0]):
            q2[i] = specific_humidity(d2m[i], sp[i])


if __name__ == '__main__':
    import argparse

    header = "Download ECMWF Era5 HIRES reanalysis data in netCDF format."
    parser = argparse.ArgumentParser(
        description=header,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('month',
                        help='Month to download, expects format "YYYY-MM".')
    parser.add_argument('-end-month', default=None,
                        help='Last month to download, expects format "YYYY-MM".')
    args = parser.parse_args()

    def get_datetime(yyyymm):
        year, month = [int(v) for v in yyyymm.split('-')]
        return datetime.datetime(year, month, 1)

    start_month = get_datetime(args.month)

    if args.end_month is not None:
        end_month = get_datetime(args.end_month)
        print('Downloading range {:%Y-%m} ... {:%Y-%m}'.format(start_month, end_month))
    else:
        end_month = start_month

    for date in rrule(MONTHLY, dtstart=start_month, until=end_month):
        print('\nFetching {:}'.format(date.strftime('%Y-%m')))
        tic = timer()
        download_month(date.year, date.month)
        toc = timer()
        duration = datetime.timedelta(seconds=toc - tic)
        print('Duration: {:}'.format(duration))
