"""Script that creates, for each feature of type array, a csv file containing the given feature for all songs."""

import os
import hdf5_getters
import numpy as np
import time

def toJson(value):
    json = '['

    if len(value) > 0:
        if value[0].__class__.__name__ == 'ndarray':
            json += toJson(value[0])
            for i in range(1, len(value)):
                json += ',' + toJson(value[i])
        else:
            #array of strings
            if hasattr(value,'dtype') and value.dtype.str.startswith('|S'):
                json += value[0].decode('UTF-8')
                for i in range(1, len(value)):
                    json += ',' + value[i].decode('UTF-8')

            #array of scalars
            else:
                json += str(value[0])
                for i in range(1,len(value)):
                    json += ',' + str(value[i])
    json += ']'
    return json
                

def write_line(output, getter,data,song_nb):
    line = hdf5_getters.get_track_id(data).decode('UTF-8')
    h5getter = getattr(hdf5_getters, getter)
    line += '\t' + toJson(h5getter(data,song_nb))
    line += '\n'
    output.write(line)

start_time=time.time()

#folder
data_folder = '/Volumes/Seagate/Dataset'

list_attr = ('artist_mbtags',
            'artist_mbtags_count',
            'artist_terms',
            'artist_terms_freq',
            'artist_terms_weight',
            'bars_confidence',
            'bars_start',
            'beats_confidence',
            'beats_start',
            'sections_confidence',
            'sections_start',
            'segments_confidence',
            'segments_loudness_max',
            'segments_loudness_max_time',
            'segments_loudness_start',
            'segments_pitches',
            'segments_start',
            'segments_timbre',
            'similar_artists',
            'tatums_confidence',
            'tatums_start')

output_files = {}
for feat in list_attr:
    feat_file = open('/Volumes/Seagate/Arrays/'+feat+'.csv','w')
    feat_file.write('track_id\t'+feat+'\n')
    output_files[feat] = feat_file

#run through each .h5 file contained in the folder
progression = 0
interval = 0
for folder, subfolders, files in os.walk(data_folder):
    for f in files:
        if f.endswith('.h5') and not f.startswith('._'):
            #open the hdf5 file
            h5 = hdf5_getters.open_h5_file_read(folder + '/' + f)

            #add one entry line in the database per row contained in the file
            for song_nb in range(hdf5_getters.get_num_songs(h5)):
                for feat,feat_file in output_files.items():
                    write_line(feat_file,'get_%s' % feat,h5,song_nb)
                progression += 1
                interval += 1
                if interval == 1000:
                    print(progression)
                    interval = 0
                    exit(1)
            h5.close()

for feat in list_attr:
    output_files[feat].close()

print('nb songs = %d' %progression)
elapsed_time=time.time()-start_time
print('elapsed time = ' + str(elapsed_time) + ' sec')
        
        