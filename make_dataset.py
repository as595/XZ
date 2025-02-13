import pandas as pd

from astroquery.skyview import SkyView
from astropy import coordinates
from astropy import units as u
from astropy.wcs import WCS
from astropy.io import fits

import requests

import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore', category=AstropyWarning)

import os,sys

# ----------------------------------------------------------------------------------------------------

def get_fits(names, coords, surveys=['VLA FIRST (1.4 GHz)'], size=0.0325, dir='z_shaped'):

    for i in range(len(coords)):

        coord = coords[i]
        fitsname = '{}/{}.fits'.format(dir, names[i])

        # get images:
        SkyView.clear_cache()
        try:
            image = SkyView.get_images(position=coord, radius=size*u.deg, survey=surveys, cache=False)
            url = SkyView.get_image_list(position=coord, radius=size*u.deg, survey=surveys, cache=False)
            
            file = requests.get(url[0], allow_redirects=True)
            open(fitsname, 'wb').write(file.content)
        except:
            print("No FITS available:", names[i])

            
    return

# ----------------------------------------------------------------------------------------------------

def get_coords(filename):

    df = pd.read_csv(filename, sep='\t', header=None)
    names = df[1]; ra = df[2]; dec = df[3]
    coords = coordinates.SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame='fk5')

    return names, coords

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    filename = 'x_shaped_list.txt'
    dir = 'x_shaped'

    # extract coordinates:
    names, coords = get_coords(filename)

    # get FITS files:
    get_fits(names, coords, dir=dir)

    # make PNG images:

    

