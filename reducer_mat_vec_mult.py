#!/opt/conda/default/bin/python

import sys

last_key = None
sum_accum = 0.0

for line in sys.stdin:
    line = line.strip()
    this_key, value = line.split("\t")
    this_key = int(this_key)
    value = float(value)
    if last_key == None:
        sum_accum += value
        last_key = this_key
    elif last_key == this_key:
        sum_accum += value
    else:
        print("%d\t%f" % (last_key, sum_accum))
        sum_accum = value
        last_key = this_key

if last_key != None:
    print("%d\t%f" % (last_key, sum_accum))