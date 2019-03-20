#!/bin/bash

# deaccumulate variables
# In Era5 accumulated data has been accumulated over 3600 s

scale_hour () {
    var=$1  # acc_radlw
    unit=$2  # "W m**-2"
    for f in $(ls *_${var}_*.nc); do
        outfile="${f/acc/}"
        outvar="${var/acc/}"
        echo "Rescaling file $f by 1/3600 -> $outfile"
        ncflint -C -O --fix_rec_crd -v $var -w 0.0002777777777777778,0.0 $f $f $outfile
        ncatted -a units,${var},o,c,"$unit" $outfile
        ncrename -v ${var},${outvar} $outfile
        #mv tmp.nc $f
    done
}

# radlw
scale_hour accradlw "W m**-2"

# radsw
scale_hour accradsw "W m**-2"

