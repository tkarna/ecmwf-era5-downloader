
#!/bin/bash

start_date="2016-06-01"
end_date="2017-03-01"


# map era5 variable names to nemo names
declare -A nemoname
# 10 m wind velocity
nemoname[u10]=U10m
nemoname[v10]=V10m
# short wave radiation
nemoname[ssrd]=radsw
# long wave radiation
nemoname[strdc]=radlw
# 2 m air temperature
nemoname[t2m]=T2m
# total precipitation
nemoname[tp]=precip
# snow fall
nemoname[sf]=snow
# surface pressure
nemoname[sp]=sfcpres
# dew point temperature
nemoname[d2m]=D2M


check_date=`date +"%Y-%m-%d" -d "$end_date + 1 month"`;
current_date=$start_date
while [ "$current_date" != "$check_date" ]; do
    year=`date +"%Y" -d "$current_date"`
    month=`date +"%m" -d "$current_date"`
    day=`date +"%d" -d "$current_date"`
    # ------------------------------------------------------------------
    infile=reanalysis-era5_${year}-${month}.nc
    echo "Processing $infile"
    for var in u10 v10 ssrd strdc t2m d2m tp sf sp; do
        outvar=${nemoname[$var]}
        outfile=era5_${outvar}_y${year}m${month}.nc
        echo $var "->" $outfile

        # extract variable
        ncks -v $var $infile $outfile

        # rename variables
        ncrename -v ${var},${outvar} $outfile

        # make time dimension unlimited (copy file)
        ncks --mk_rec_dmn time $outfile -o tmp.nc
        mv tmp.nc $outfile
    done
    # ------------------------------------------------------------------
    # increment date
    current_date=`date +"%Y-%m-%d" -d "$current_date + 1 month"`;
done

