import os
import sys

name_dir = "txt"
name_files = os.listdir(name_dir)
name_created_file = "name_files.txt"
file1 = open(name_created_file, "w")
num_files_to_read = 1000
for i in range(num_files_to_read):
    file1.write(name_files[i] + "\n")
file1.close()