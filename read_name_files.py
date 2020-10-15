import os
import sys

name_dir = "txts_prueba"
name_files = os.listdir(name_dir)
name_created_file = "name_files.txt"
file1 = open(name_created_file, "w")
for name_file in name_files:
    file1.write(name_file + "\n") 
file1.close()