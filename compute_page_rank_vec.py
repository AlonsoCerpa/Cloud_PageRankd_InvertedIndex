import numpy as np
from google.cloud import storage

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

def pagerank(M, num_iterations = 100, d = 0.85):
    N = M.shape[1]
    v = np.random.rand(N, 1)
    v = v / np.linalg.norm(v, 1)
    M_hat = (d * M + (1 - d) / N)
    for i in range(num_iterations):
        v = M_hat @ v
    return v

bucket_name = "datos-trabajo-page-rank-inverted-index"
prefix = "salida_matrix"
list_blobs_names = list_blobs(bucket_name, prefix)
list_blobs_names.remove('salida_matrix/')
list_blobs_names.remove('salida_matrix/_SUCCESS')

dict_transitions = {}
num_files_to_rank = 4
for i in range(num_files_to_rank):
    dict_transitions[i] = []

for blob_name in list_blobs_names:
    dir_name, name_file = blob_name.split("/")
    download_blob(bucket_name, blob_name, name_file)
    file_read = open(name_file, 'r')
    data = file_read.readlines()
    data = [x.strip() for x in data]
    file_read.close()

    for line in data:
        key, value = line.split("\t")
        idx_src, idx_tgt = key.split()
        idx_src = int(idx_src)
        idx_tgt = int(idx_tgt)
        dict_transitions[idx_src].append(idx_tgt)

M = np.zeros((num_files_to_rank, num_files_to_rank))
for i in range(num_files_to_rank):
    num_links = len(dict_transitions[i])
    percentage = 1.0/num_links
    for idx_tgt_M in dict_transitions[i]:
        M[idx_tgt_M, i] = percentage

"""
M = np.array([[0, 0, 0, 0, 1],
              [0.5, 0, 0, 0, 0],
              [0.5, 0, 0, 0, 0],
              [0, 1, 0.5, 0, 0],
              [0, 0, 0.5, 1, 0]])
"""

v = pagerank(M, 100, 0.85)
print(v)