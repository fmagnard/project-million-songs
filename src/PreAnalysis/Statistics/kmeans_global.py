'''Script that computes k-means clusters of songs with several numerical coordinates.'''

import os
import time
import csv
import numpy as np
from sklearn import cluster as skc

start_time = time.time()

all_data = []

features = {'duration', 'key', 'key_confidence', 'loudness', 'mode', 'mode_confidence', 'tempo','time_signature','time_signature_confidence'}

with open('../GetMissingYears/Output/features.tsv','r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        data = []
        year = row['year'].split('-')[0]
        if int(year) != 0:
            data.append(int(year))

            add = True
            for feature in features:
                if feature in row:
                    value = row[feature]
                    if not(value != 'nan' and value != '' and (value != '0.0' and value != '0' or feature == 'key' or feature == 'mode' or feature.endswith('_confidence'))):
                        add = False
                        break
                    data.append(float(value))
                else:
                    print('======FAIL:'+row)
                    add = False
                    break
            if add:
                all_data.append(data)

all_data = np.array(all_data, dtype=np.float64)
means = np.mean(all_data,axis=0)
stds = np.std(all_data,axis=0)
all_data -= means
all_data /= stds

print("Reading done")

K = 500
with open('Output/scatterplot_features.csv','w') as output:
    output.write('year')
    for f in features:
        output.write('\t'+f)
    
    predictions = skc.KMeans(K, n_jobs=10, tol=0.001, verbose = 1, max_iter = 35).fit_predict(all_data)

    nf = len(features)+1
    centroids = np.zeros((K,nf))
    counts = np.zeros(K)
    for i in range(len(all_data)):
        p = predictions[i]
        centroids[p] += all_data[i]
        counts[p] += 1
    
    for p in range(K):
        centroids[p] /= counts[p]
    
    centroids *= stds
    centroids += means
    
    for c in centroids:
        output.write('\n')
        output.write(str(c[0]))
        for i in range(1,nf):
            output.write('\t'+ str(c[i]))
        
elapsed = time.time()-start_time
print('Elapsed time = '+str(elapsed)+' s')