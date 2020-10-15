#!/opt/conda/default/bin/python

import sys

last_key = None

for input_line in sys.stdin:
    input_line = input_line.strip()
    this_key, value = input_line.split("\t", 1)

    idx_src, idx_tgt = this_key.split()

    if idx_src == idx_tgt or (last_key != None and last_key == this_key):
        continue
    else:
        print("%s\t%d" % (this_key, 1))
        last_key = this_key
