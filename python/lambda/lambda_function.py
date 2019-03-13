import os
import subprocess
import sys
import logging

# set up logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
# commented out to avoid duplicate logs in lambda
# logger.addHandler(logging.StreamHandler())

# imports used for the example code below
from osgeo import gdal


test_filename = 'https://landsat-pds.s3.amazonaws.com/c1/L8/086/240/LC08_L1GT_086240_20180827_20180827_01_RT/LC08_L1GT_086240_20180827_20180827_01_RT_B1.TIF'


def lambda_handler(event, context=None):
    """ Lambda handler """
    logger.debug(event)

    # this try block is for testing and info only, it can be safely removed
    # it prints out info on the linked libraries found in libgdal
    try:
        output = subprocess.check_output('ldd /opt/lib/libgdal.so'.split(' '))
        logger.info(output.decode())
    except Exception as e:
        pass

    # process event payload and do something like this
    fname = event.get('filename', test_filename)
    fname = fname.replace('s3://', '/vsis3/')
    # open and return metadata
    ds = gdal.Open(fname)
    band = ds.GetRasterBand(1)
    stats = band.GetStatistics(0, 1)

    return stats


if __name__ == "__main__":
    """ Test lambda_handler """
    event = {'filename': test_filename}
    stats = lambda_handler(event)
    print(stats)