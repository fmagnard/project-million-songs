'''Script that counts, for each feature, the number of songs for which we know the feature value'''

import os
import time
import csv


start_time = time.time()

nb_features_per_year = {}
features = None

with open('../GetMissingYears/Output/features.tsv','r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        if features is None:
            features = set()
            for f in row:
                features.add(f)
                
        year = row['year'].split('-')[0]
        if not year in nb_features_per_year:
            nb_features_per_year[year] = {}
       
        for feature,value in row.items():
            if feature != 'year':
                #create the feature count if it does not exist
                if not feature in nb_features_per_year[year]:
                    nb_features_per_year[year][feature] = 0
                #update the count if not null value
                if value != 'nan' and (value != '0.0' and value != '0' or feature == 'key' or feature == 'mode') and not ((feature.endswith('_7digitalid') or feature == 'playmeid') and value == '-1'):
                    nb_features_per_year[year][feature] += 1

with open('Output/features_count_per_year.tsv','w') as output:
    all_features = sorted(features)
    output.write('year')
    for f in all_features:
        output.write('\t'+f)
    for year,values in nb_features_per_year.items():
        output.write('\n'+year)
        for f in all_features:
            if f in values:
                output.write('\t'+str(values[f]))
            else:
                output.write('\t0')
        
        
elapsed = time.time()-start_time
print('Elapsed time = '+str(elapsed)+' s')