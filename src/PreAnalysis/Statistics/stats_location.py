'''Script that produces a file containing the location of each artist. '''

import os
import time

#Rough estimation of wether the location is in the US or Canada.
def is_in_US_Canada(lat_, lon_):
    lat = float(lat_)
    lon = float(lon_)
    if lat > 4.0/14.0*lon and lon > -179 and lon < -50:
        return True
    else:
        return False

start_time = time.time()
count = 0
with open('Output/locations_by_artist.txt','w') as output:
    output.write('artist_id\tartist_name\tis_in_US_Canada\tlocation\n')
    with open('Input/artist_location.txt','r') as file:
        for line in file:
            entries = line.split('<SEP>')
            artist_id = entries[0]
            latitude = entries[1]
            longitude = entries[2]
            artist_name = entries[3]
            location = entries[4]
            US_Canada = is_in_US_Canada(latitude,longitude)
            if US_Canada:
                count += 1
            output.write(artist_id+'\t'+artist_name+'\t'+str(US_Canada)+'\t'+location)

print('elapsed time = '+str(time.time()-start_time))
print('nb artists in US/Canada = '+str(count))