from tomopy.prep.normalize import normalize
import tomopy
import dxchange
import numpy as np
from logger import LOGGER
import os
import time


def reconstruct(tomos_3d, flats_3d, darks_3d, sample_name):
    tomos = normalize(tomos_3d, flats_3d, darks_3d)
    tomos[np.isnan(tomos)] = 0
    tomos[tomos == -np.inf] = 0
    tomos[tomos == np.inf] = 1
    data = tomopy.minus_log(tomos)
    theta = tomopy.angles(data.shape[0], 0, 360)

    rot_center = (tomos.shape[2]) / 2.0
    LOGGER.info(f"Center of rotation image: {rot_center}")

    auto_rot_center = tomopy.find_center_pc(tomos[0], tomos[-1], tol=0.5, rotc_guess=rot_center)
    LOGGER.info(f"Automatically detected center of rotation: {auto_rot_center}")

    slice_start = 0
    slice_end = len(tomos[0])

    LOGGER.debug("START RECONSTRUCTION")
    rec = tomopy.recon(tomos[:, slice_start:slice_end, :], theta=theta, center=auto_rot_center, algorithm='gridrec')
    LOGGER.debug(f"END RECONSTRUCTION")
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # save slices in tiff format
    fname_out_tiff = get_last_folder(sample_name)
    LOGGER.info(f"Saving slices in '{fname_out_tiff}'")
    dxchange.write_tiff_stack(rec[:, :, :], fname=fname_out_tiff + 'slice')
    LOGGER.info("Slices saved successfully")


def get_last_folder(sample_name):
    directory = 'output/'
    directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    filtered_directories = [d for d in directories if d.startswith(f'{sample_name}')]
    sorted_names = sorted(filtered_directories, key=lambda name: (
        name.startswith(sample_name), -int(name.split('_')[-1]) if '_' in name else 0))
    return f'output/{sorted_names[0]}/recons/'
