from logger import LOGGER
from image_taker import ImageTaker
from tomopy.prep.normalize import normalize
from processing.recontructor import reconstruct
import numpy as np

'''
if problems try lower resolution
'''



def main():

    n_tomos = 4
    n_flats = 2
    n_darks = 2
    url = "http://192.168.0.107:8080/video"

    sample_name = "spata"

    image_taker = ImageTaker(n_tomos, n_flats, n_darks, url)
    image_taker.get_tomos()
    image_taker.get_flats()
    image_taker.get_darks()
    image_taker.save_images(sample_name)

    tomos_3d, flats_3d, darks_3d = image_taker.get_3d_arrays()
    reconstruct(tomos_3d, flats_3d, darks_3d, sample_name)









if __name__ == '__main__':
    main()
