# Preprocess Era5 atmospheric forcing fields for Nemo runs

1. Download data

download_monthly.py

Downloads a subset of global fields to monthly files.

Produces files:
reanalysis-era5_2016-06.nc
...

2. Extract individual fields

./extract_fields.sh

Extract individual fields from source files

Produces files:
era5_D2M_y2016m06.nc
...

These files can be used as forcing in Nemo 3.6 and 4.0.

3. Compute specific humidity

./compute_spec_hum.sh

Produces files:
era5_Q2_y2016m06.nc
...

Uses:
compute_spec_hum.py

Dependency: python, iris
