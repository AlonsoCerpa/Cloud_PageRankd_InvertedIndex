#!/opt/conda/default/bin/python

import sys
import random
import numpy as np
import string
import re
from google.cloud import storage

bucket_name = "datos-trabajo-page-rank-inverted-index"
parent_dir_txts_in = "txt_with_links"

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

for line in sys.stdin:
    line = line.strip()
    cloud_path_file_in = parent_dir_txts_in + "/" + line
    local_path_file_in = "./" + line

    download_blob(bucket_name, cloud_path_file_in, local_path_file_in)
    
    file_read = open(local_path_file_in, 'r')
    data = file_read.read()
    file_read.close()
    data = data.translate(data.maketrans('', '', string.punctuation))
    data = data.lower()
    words = data.split()
    words = list(set(words))

    for word in words:
        print("%s\t%s" % (word, line))    
