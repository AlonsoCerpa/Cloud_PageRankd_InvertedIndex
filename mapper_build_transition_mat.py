#!/opt/conda/default/bin/python

import sys
import random
import numpy as np
from google.cloud import storage

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

name_file_with_names = "./name_files.txt"
file1 = open(name_file_with_names, "r")
names_files = file1.readlines()
file1.close()
names_files = [x.strip() for x in names_files]
dict_name_files = {}
idx_name_file = 0
for name_file in names_files:
    dict_name_files[name_file] = idx_name_file
    idx_name_file += 1

bucket_name = "datos-trabajo-page-rank-inverted-index"
parent_dir_txts_in = "txts_prueba_links"

for line in sys.stdin:
    line = line.strip()
    cloud_path_file_in = parent_dir_txts_in + "/" + line
    local_path_file_in = "./" + line

    download_blob(bucket_name, cloud_path_file_in, local_path_file_in)
    
    file_read = open(local_path_file_in, 'r')
    data = file_read.read()
    file_read.close()
    
    length_file = len(data)
    start_idx = 0
    idx_found = data.find("LINK_A_OTRO_ARCHIVO=", start_idx)
    idx_source = dict_name_files[line]
    
    end_file = False
    while idx_found != -1 and end_file == False:
        idx_start_name_file = idx_found + 20
        idx_end_name_file = data.find(".txt", idx_start_name_file) + 4
        name_file_found = data[idx_start_name_file:idx_end_name_file]
        idx_target = dict_name_files[name_file_found]
        print("%d %d\t1" % (idx_source, idx_target))
        start_idx = idx_end_name_file
        if start_idx >= length_file:
            end_file = True
        else:
            idx_found = data.find("LINK_A_OTRO_ARCHIVO=", start_idx)
    
