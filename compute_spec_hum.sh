for f in $(ls era5_D2M_*.nc); do
    dewt=$f
    spres="${f/D2M/sfcpres}"
    q2="${f/D2M/Q2}"
    cmd="python compute_spec_hum.py $dewt $spres $q2"
    echo $cmd
    $cmd
done
