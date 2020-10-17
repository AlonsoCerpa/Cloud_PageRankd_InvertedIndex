#!/opt/conda/default/bin/python

from google.cloud import storage
import shutil
import sys

bucket_name = "datos-trabajo-page-rank-inverted-index"
prefix = "output_page_rank" + sys.argv[1]
name_file_write = "vector_page_rank" + sys.argv[1] + ".txt"

def list_blobs(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    list_blobs_names = []
    for blob in blobs:
        list_blobs_names.append(blob.name)
    return list_blobs_names

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

list_blobs_names = list_blobs(bucket_name, prefix)
list_blobs_names.remove(prefix + '/')
list_blobs_names.remove(prefix + '/_SUCCESS')

file_write = open(name_file_write, "wb")
for blob_name in list_blobs_names:
    dir_name, name_file = blob_name.split("/")
    download_blob(bucket_name, blob_name, name_file)
    file_read = open(name_file, 'rb')
    shutil.copyfileobj(file_read, file_write)
    file_read.close()
file_write.close()

upload_blob(bucket_name, name_file_write, name_file_write)