#!/bin/sh

if [ $# -eq 0 ] || [ $1 = "-h" ]
then
    echo "Usage:" $0 "train_set test_set [MIN_K [INCR_K [MAX_K [-w]]]]"
    exit
fi

min=${3:-1}
incr=${4:-1}
max=${5:-200}

weight_var=${6:-empty}

weight_neighbors=""
if [ $weight_var = "-w" ]
then
    weight_neighbors="--weight-neighbors"
fi

for k in $(seq $min $incr $max)
do
    ./classdoc_knn_canevas.py --k $k $1 $2 $weight_neighbors
    if [ $? -ne 0 ]
    then
        exit
    fi
done