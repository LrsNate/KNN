#!/bin/sh

min=${3:-1}
incr=${4:-1}
max=${5:-200}

shift $((OPTIND-1))

for k in $(seq $min $incr $max)
do
    ./classdoc_knn_canevas.py --k $k $1 $2
done