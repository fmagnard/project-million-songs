'''Script that computes, for each numerical feature, the mean feature values of all songs'''

import os
import time
import csv


start_time = time.time()

mean_features_per_year = {}
nb_features_per_year = {}
features = {'danceability','duration','energy', 'key', 'key_confidence', 'loudness', 'mode', 'mode_confidence', 'tempo','time_signature','time_signature_confidence'}

with open('../GetMissingYears/Output/features.tsv','r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        year = row['year'].split('-')[0]
        if not year in mean_features_per_year:
            mean_features_per_year[year] = {}
            nb_features_per_year[year] = {}
        for feature in features:
            #create the feature count if it does not exist
            if not feature in mean_features_per_year[year]:
                mean_features_per_year[year][feature] = 0
                nb_features_per_year[year][feature] = 0
            #update the count if not null value
            value = row[feature]
            if value != 'nan' and (value != '0.0' and value != '0' or feature == 'key' or feature == 'mode'):
                try:
                    mean_features_per_year[year][feature] += float(value)
                    nb_features_per_year[year][feature] += 1
                except ValueError:
                    print(value)

with open('Output/features_mean_per_year.tsv','w') as output:
    all_features = sorted(features)
    output.write('year')
    for f in all_features:
        output.write('\t'+f)
    for year in mean_features_per_year:
        output.write('\n'+str(year))
        for f in all_features:
            if nb_features_per_year[year][feature] != 0:
                mean = mean_features_per_year[year][feature]/float(nb_features_per_year[year][feature])
                output.write('\t'+str(mean))
            else:
                output.write('\t0')

        
elapsed = time.time()-start_time
print('Elapsed time = '+str(elapsed)+' s')