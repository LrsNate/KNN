#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from argparse import ArgumentParser
from subprocess import check_output
from time import time

parser = ArgumentParser(description="Find the optimal K hyper-parameter")

parser.add_argument("train_set", help="A file containing the train set")
parser.add_argument("test_set", help="A file containing the test set")
parser.add_argument("--min", dest="min", type=int, help="The minimum K to be tested")
parser.add_argument("--max", dest="max", type=int, help="The maximum K to be tested")
parser.add_argument("--incr", dest="incr", type=int, help="The increment of K when testing")
parser.add_argument("-w", dest="weighted", action="store_true",
                    help="Whether to test the weighted version of the K-NN algorithm")

argv = parser.parse_args()

train_set = argv.train_set
test_set = argv.test_set
weighted = argv.weighted

min_k = 1
max_k = 15
incr_k = 1

if 0 < argv.min < 2000:
    min_k = argv.min

if min_k < argv.max < 2000:
    max_k = argv.max

if 0 < argv.incr < max_k:
    incr_k = argv.incr

base_args = ["./classdoc_knn_canevas.py", train_set, test_set]


def execute(k):
    args = base_args
    args.extend(["--k", str(k)])
    if weighted:
        args.extend("--weight-neighbors")
    return check_output(args)

res_list = []

print "Testing from %d to %d, with an increment of %d. (%s)" % (
    min_k,
    max_k,
    incr_k,
    "weighted" if weighted else "non-weighted"
)

i = min_k
while i <= max_k:
    start_time = int(round(time() * 1000))
    res = execute(i).rstrip('\n').split()
    end_time = int(round(time() * 1000))
    formatted_res = {
        "k": i,
        "score": int(float(res[4])),
        "percent": float(res[2]) * 100
    }
    res_list.append(formatted_res)
    print "k=%d: %d (%.2f%%) [%dms]" % (
        formatted_res["k"],
        formatted_res["score"],
        formatted_res["percent"],
        end_time - start_time
    )
    i += incr_k

max_res = max(res_list, key=lambda x: x["percent"])
print "Maximum result: %d (%.2f%%), with k=%d." % (max_res["score"], max_res["percent"], max_res["k"])