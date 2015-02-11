#!/bin/sh

min=${3:-1}
incr=${4:-1}
max=${5:-200}

weight_var=${6:-empty}

weight_neighbors=""
if [ $weight_var = "-w" ]
then
    weight_neighbors="--weight-neighbors"
fi

#while getopts ':w' opt ; do
#  case $opt in
#    w) weight_neighbors="--weight-neighbors" ;;
#  esac
#done
## skip over the processed options
#shift $((OPTIND-1))

for k in $(seq $min $incr $max)
do
    ./classdoc_knn_canevas.py --k $k $1 $2 $weight_neighbors
done