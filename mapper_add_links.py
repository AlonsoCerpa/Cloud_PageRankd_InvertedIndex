#!/opt/conda/default/bin/python

import sys
import random
import numpy as np
from google.cloud import storage

bucket_name = "datos-trabajo-page-rank-inverted-index"
parent_dir_txts_in = "txt"
parent_dir_txts_out = "txt_with_links"
name_file_with_names = "./name_files.txt"
mean_links_out = 30
std_links_oout = 10

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

file1 = open(name_file_with_names, "r")
names_files = file1.readlines()
file1.close()
names_files = [x.strip() for x in names_files] 
length_names_files = len(names_files)

for line in sys.stdin:
    line = line.strip()
    cloud_path_file_in = parent_dir_txts_in + "/" + line
    local_path_file_in = "./" + line
    
    download_blob(bucket_name, cloud_path_file_in, local_path_file_in)
    
    file_read = open(local_path_file_in, 'r')
    data = file_read.read()
    file_read.close()
    length_file = len(data)
    number_links = max(0, int(np.random.normal(mean_links_out, std_links_oout, 1)[0]))
    
    for i in range(number_links):
        pos_in_text = random.randint(0, length_file-1)
        idx_file_linked = random.randint(0, length_names_files-1)
        while data[pos_in_text] != ' ':
            pos_in_text += 1
            if pos_in_text == length_file:
                pos_in_text = 0
        data = data[:pos_in_text] + " LINK_A_OTRO_ARCHIVO=" + names_files[idx_file_linked] + data[pos_in_text:]
    file_write = open(local_path_file_in, 'w')
    file_write.write(data)
    file_write.close()
    cloud_path_file_out = parent_dir_txts_out + "/" + line
    upload_blob(bucket_name, local_path_file_in, cloud_path_file_out)
