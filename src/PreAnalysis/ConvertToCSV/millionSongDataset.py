'''This class enables the user to request a feature for a song known by its track_id'''

import os
import hdf5_getters

class MillionSongDataset(object):
    #initialize with path to Dataset folder
    def __init__(self, dataset_folder):
        self.dataset_folder = dataset_folder
        self.track_id = ''
        self.h5 = None
    
    #get value of feature for track_id
    def get_feature(self, track_id, feature):
        if self.track_id != track_id:
            if not self.h5 is None:
                self.h5.close()
            file_path = os.path.join(self,track_id[2],track_id[3],track_id[4],track_id+'.h5')
            self.h5 = hdf5_getters.open_h5_file_read(file_path)

        h5getter = getattr(hdf5_getters, 'get_'+feature)
        return h5getter(self.h5,0)
    
    #close last opened .h5 file
    def close_open_file(self):
        if not self.h5 is None:
            self.h5.close()
