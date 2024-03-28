from logger import LOGGER
from components.camera import Camera
from components.microphone import Microphone
from components.image import Image
import cv2 as cv
import os
import time


class ImageTaker:
    def __init__(self, n_tomos, n_flats, n_darks, url):
        # n_tomos sarebbero gli steps
        self.n_tomos, self.tomos = n_tomos, []
        self.n_flats, self.flats = n_flats, []
        self.n_darks, self.darks = n_darks, []

        self.camera = Camera(url)
        self.microphone = Microphone()

    def get_tomos(self):
        try:
            while len(self.tomos) < self.n_tomos:
                ret, frame = self.camera.get_ret_frame()
                if self.microphone.is_vibrating():
                    time.sleep(0.05) # Wait for ending of vibration just to be sure
                    image = Image(frame, 'tomo', '.tiff', color_model="RGB")
                    self.tomos.append(image)
                    LOGGER.info(f"Tomo nr {len(self.tomos)} taken")
        except KeyboardInterrupt:
            LOGGER.info("Keyboard interrupt received. Cleaning...")
            self.microphone.clean()
            LOGGER.info("Exiting...")

    def get_flats(self):
        self._capture("flat", ".tiff", self.flats, self.n_flats)

    def get_darks(self):
        self._capture("dark", ".tiff", self.darks, self.n_darks)


    '''
    def save_images(self, sample_name):
        tomos_path, flats_path, darks_path = self._create_folders(sample_name)
        for i in range(len(self.tomos)):
            tomo_path = os.path.join(tomos_path, f"tomo_{'%04d' % i}")
            cv.imwrite(tomo_path, self.tomos[i])
        LOGGER.info("Tomos saved successfully")

        for i in range(len(self.flats)):
            flat_path = os.path.join(flats_path, f"flat_{'%04d' % i}")
            cv.imwrite(flat_path, self.flats[i])
        LOGGER.info("Flats saved successfully")

        for i in range(len(self.darks)):
            dark_path = os.path.join(darks_path, f"dark_{'%04d' % i}")
            cv.imwrite(dark_path, self.darks[i])
        LOGGER.info("Darks saved successfully")

    '''

    def save_images(self, sample_name):
        tomos_path, flats_path, darks_path = self._create_folders(sample_name)

        save_images_type = [('tomo', self.tomos, tomos_path), ('flat', self.flats, flats_path),
                            ('dark', self.darks, darks_path)]

        for image_type, images, path in save_images_type:
            for i, image in enumerate(images):
                image_path = os.path.join(path, f"{image_type}_{'%04d' % (i+1)}.{image.get_extension()}")
                cv.imwrite(image_path, image.get_array())
            LOGGER.info(f"{image_type.capitalize()}s saved successfully")




    def _capture(self, mode, extension, images_list, n_photos):
        photo_taken = 0
        while len(images_list) < n_photos:
            ret, frame = self.camera.get_ret_frame()
            cv.imshow("Press enter to take photo", frame)
            key = cv.waitKey(1)
            if key == 32:
                image = Image(frame, mode, extension, color_model="RGB")
                images_list.append(image)
                photo_taken += 1
                LOGGER.info(f"{mode} nr {len(images_list)} taken")


    def _create_folders(self, sample_name):
        base_path = "output"
        sample_path = os.path.join(base_path, sample_name)

        # Check if the sample folder already exists
        if os.path.exists(sample_path):
            # If it exists, find an available name
            i = 2
            while True:
                new_sample_name = f"{sample_name}_{i}"
                new_sample_path = os.path.join(base_path, new_sample_name)
                if not os.path.exists(new_sample_path):
                    sample_path = new_sample_path
                    break
                i += 1

        # Create the necessary folders
        projections_path = os.path.join(sample_path, "projections")
        tomos_path = os.path.join(projections_path, "tomos")
        flats_path = os.path.join(projections_path, "flats")
        darks_path = os.path.join(projections_path, "darks")

        os.makedirs(tomos_path, exist_ok=True)
        os.makedirs(flats_path, exist_ok=True)
        os.makedirs(darks_path, exist_ok=True)

        return tomos_path, flats_path, darks_path