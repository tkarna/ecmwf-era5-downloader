# Preprocess Era5 atmospheric forcing fields for Nemo runs

## Download data for a month

`python download_ecmwf_era5.py 2014-10`

Downloads a subset of global fields to monthly files.

Produces file:
`era5_y2014m10.nc`

Dependency: python, cdsapi, python-netCDF4

## Download multiple months

`python download_ecmwf_era5.py 2014-12 -e 2015-02`

Produces files:
`era5_y2014m12.nc`
`era5_y2015m01.nc`
`era5_y2015m02.nc`

