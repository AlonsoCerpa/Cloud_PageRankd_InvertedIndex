#!/opt/conda/default/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    numbers = line.split()
    vec_value = float(numbers[1])
    num_numbers = len(numbers)
    idx_number = 2
    while idx_number < num_numbers:
        idx_row_in_mat = int(numbers[idx_number])
        idx_number += 1
        mat_value = float(numbers[idx_number])
        print("%d\t%f" % (idx_row_in_mat, vec_value * mat_value))
        idx_number += 1
