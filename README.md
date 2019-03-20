# Preprocess Era5 atmospheric forcing fields for Nemo runs

## 1. Download data

`python download_monthly.py`

Downloads a subset of global fields to monthly files.

Produces files:
`reanalysis-era5_2016-06.nc`
...

Dependency: python, cdsapi

## 2. Extract individual fields

`./extract_fields.sh`

Extract individual fields from source files

Produces files:
`era5_D2M_y2016m06.nc`
...

These files can be used as forcing in Nemo 3.6 and 4.0.

Dependency: nco

## 3. Deaccumulate fields

`./deaccumulate_fields.sh`

Deaccumulates long/shortwave radiation fields by 1/3600.

Produces files:
`era5_radlw_y2016m06.nc`
`era5_radsw_y2016m06.nc`
...

Dependency: nco

## 4. Compute specific humidity

`./compute_spec_hum.sh`

Produces files:
era5_Q2_y2016m06.nc
...

Uses:
`compute_spec_hum.py`

Dependency: python, iris
