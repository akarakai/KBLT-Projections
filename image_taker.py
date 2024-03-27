from logger import LOGGER
from components.camera import Camera
from components.microphone import Microphone
from components.image import Image
import cv2 as cv


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
