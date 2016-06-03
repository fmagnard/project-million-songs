"""Script that creates, for each numeric or string feature, a csv file containing the given feature for all songs."""

import os
import hdf5_getters
import numpy as np
import time

def get_getters(list_attr):
    all_getters = sorted(filter(lambda key: key[:4] == 'get_' and key != 'get_num_songs', hdf5_getters.__dict__.keys()))
    
    getters = []
    for attr in list_attr:
        attr_getter = 'get_%s' % attr
        # Sanity
        if attr_getter in all_getters:
            getters.append(attr_getter)
        else:
            print("No such attr! %s", attr_getter)
            exit(0)
    return getters

def write_line(output, getters,data,song_nb):
    line = ''
    for getter in getters:
        h5getter = getattr(hdf5_getters, getter)
        value = h5getter(data,song_nb)
        if line != '':
            line += '\t'
        line += str(value)
    line += '\n'
    output.write(line)

start_time=time.time()

#folder
data_folder = '/Volumes/Seageate/Dataset'

#output 1
metadata = open('Outputs/features.tsv','w')
list_attr1 = ('analysis_sample_rate',
              'artist_7digitalid',
              'artist_familiarity',
              'artist_hotttnesss',
              'artist_id',
              'artist_latitude',
              'artist_location',
              'artist_longitude',
              'artist_mbid',
              'artist_name',
              'artist_playmeid',
              'audio_md5',
              'danceability',
              'duration',
              'end_of_fade_in',
              'energy',
              'key',
              'key_confidence',
              'loudness',
              'mode',
              'mode_confidence',
              'release',
              'release_7digitalid',
              'song_hotttnesss',
              'song_id',
              'start_of_fade_out',
              'tempo',
              'time_signature',
              'time_signature_confidence',
              'title',
              'track_id',
              'track_7digitalid',
              'year')
sep = '\t'
metadata.write(sep.join(list_attr1)+'\n')


getters1 = get_getters(list_attr1)


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
                write_line(metadata,getters1,h5,song_nb)
                progression += 1
                interval += 1
                if interval == 1000:
                    print(progression)
                    interval = 0
            h5.close()

metadata.close()

print('nb songs = %d' %progression)
elapsed_time=time.time()-start_time
print('elapsed time = ' + str(elapsed_time) + ' sec')
        
        