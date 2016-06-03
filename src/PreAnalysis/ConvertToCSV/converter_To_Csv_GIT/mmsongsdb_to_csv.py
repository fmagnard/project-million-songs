#!/usr/bin/env python

"""Convert mmsongsdb h5 files into one single csv

Requirements:

- https://github.com/rcrdclub/mm-songs-db-tools
"""

import logging
import os.path
import sys
import time

from mmsongsdbtools.mmsongsdbtocsvconverter import MMSongsDbToCsvConverter


# Logger
logger = logging.getLogger('')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s (%(process)d): %(message)s',
                              '%Y-%m-%d %H:%M:%S')

# Stream handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

# File handler
cwd = os.path.dirname(os.path.realpath(__file__))
log_filename = os.path.join(cwd, 'mmsongsdb.log')
fh = logging.FileHandler(log_filename)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)


def main():
    try:
        csv_filename = sys.argv[1]
        directory = sys.argv[2]
        attrs_to_save = sys.argv[3:]
    except:
        logger.error("Usage: ./mmsongsdb_to_csv.py <csv_filename> <directory> [<attr_to_save> <attr_to_save> ...]")
        sys.exit(1)
        return
    converter = MMSongsDbToCsvConverter(csv_filename, attrs_to_save)
    converter.convert_directory(directory)


if __name__ == '__main__':
    tic = time.clock()
    main()
    toc = time.clock()
    tac = toc-tic
    print "Time spent : %.2f seconds" %tac
