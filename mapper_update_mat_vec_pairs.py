#!/opt/conda/default/bin/python

import sys
import random
import numpy as np
import os

num_vec_pr = os.environ.get('NUM_VEC_PR')
name_file_vector_pr = "./vector_page_rank" + num_vec_pr + ".txt"

file1 = open(name_file_vector_pr, "r")
vec_page_rank = file1.readlines()
file1.close()
vec_page_rank = [x.strip() for x in vec_page_rank]
dict_vec_pr = {}
for line in vec_page_rank:
    numbers = line.split()
    idx = int(numbers[0])
    value = float(numbers[1])
    dict_vec_pr[idx] = value

for line in sys.stdin:
    line = line.strip()
    numbers = line.split(maxsplit=2)
    idx_vec = int(numbers[0])
    new_vec_value = dict_vec_pr[idx_vec]
    print("%d %f\t%s" % (idx_vec, new_vec_value, numbers[2]))
