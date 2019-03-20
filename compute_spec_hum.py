"""
Compute near surface specific humidity from dew point temperature and surface
pressure.
"""
import numpy
import iris


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


def process(dewpointfile, spresfile, outfile):
    """
    Compute specific humidity with iris cube instances
    """
    print('Reading {:}'.format(dewpointfile))
    dewt = iris.load(dewpointfile)[0]
    print('Reading {:}'.format(spresfile))
    spres = iris.load(spresfile)[0]

    humi = dewt.copy()
    humi.data = specific_humidity(dewt.data, spres.data)
    humi.standard_name = 'specific_humidity'
    humi.unit = '1'
    humi.var_name = 'Q2'
    humi.attributes.pop('history', None)

    print('Saving {:}'.format(outfile))
    iris.fileformats.netcdf.save(humi, outfile, unlimited_dimensions=['time'])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            'Compute specific humidity from dew point temperature and'
            'surface pressure'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('dewpointfile',
                        help='NetCDF file containing dew point field')
    parser.add_argument('spresfile',
                        help='NetCDF file containing surface pressure field')
    parser.add_argument('outputfile',
                        help='Output NetCDF file.')
    args = parser.parse_args()

    process(args.dewpointfile, args.spresfile, args.outputfile)
