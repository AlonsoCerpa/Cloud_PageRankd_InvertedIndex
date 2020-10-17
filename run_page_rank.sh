#!/bin/bash

for i in {1..7}
do
	# MapRed 3: Calcular el page-rank usando la multiplicación matriz-vector distribuida
   hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -files gs://datos-trabajo-page-rank-inverted-index/mapper_mat_vec_mult.py,gs://datos-trabajo-page-rank-inverted-index/reducer_mat_vec_mult.py -mapper mapper_mat_vec_mult.py -reducer reducer_mat_vec_mult.py -input gs://datos-trabajo-page-rank-inverted-index/output_matrix_vec$i -output gs://datos-trabajo-page-rank-inverted-index/output_page_rank$i
   # Concatenar todos los archivos del vector page-rank en uno solo
   python concat_files_vector_page_rank.py $i
   j=$((i+1))
   # MapRed 4: Generar nuevos pares de la matriz de adyacencia con el nuevo vector page-rank calculado
   hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -D mapred.reduce.tasks=0 -files gs://datos-trabajo-page-rank-inverted-index/mapper_update_mat_vec_pairs.py,gs://datos-trabajo-page-rank-inverted-index/reducer_empty.py,gs://datos-trabajo-page-rank-inverted-index/vector_page_rank$i.txt -mapper mapper_update_mat_vec_pairs.py -reducer reducer_empty.py -input gs://datos-trabajo-page-rank-inverted-index/output_matrix_vec$i -output gs://datos-trabajo-page-rank-inverted-index/output_matrix_vec$j -cmdenv NUM_VEC_PR=$i
done
