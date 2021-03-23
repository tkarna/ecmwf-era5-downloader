# Download and preprocess ERA5 atmospheric forcing fields for NEMO

## Requirements

Python packages:

- netCDF4
- numpy
- cdsapi

These can be installed with `pip`

```bash
pip install -r requirement.txt
```

To use ECMWF `cdsapi`, you'll need to create login credentials and store them
in `$HOME/.cdsapirc ` file.
See the [instructions](https://cds.climate.copernicus.eu/api-how-to).

## Download data for a month

`python download_ecmwf_era5.py 2014-10`

Downloads a subset of global fields to monthly files.

Produces file:
`era5_y2014m10.nc`

## Download multiple months

`python download_ecmwf_era5.py 2014-12 -e 2015-02`

Produces files:
`era5_y2014m12.nc`
`era5_y2015m01.nc`
`era5_y2015m02.nc`

