from logger import LOGGER
from image_taker import ImageTaker


def main():
    n_tomos = 200
    n_flats = 10
    n_darks = 10
    url = "http://192.168.0.107:8080/video"


    image_taker = ImageTaker(n_tomos, n_flats, n_darks, url)
    image_taker.get_tomos()
    #image_taker.get_flats()







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
