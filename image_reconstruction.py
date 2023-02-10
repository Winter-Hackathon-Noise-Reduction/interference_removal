# Necessary imports
import math
import random
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Random seed
random.seed(1337)


def read_images(path):
    """
    TODO: currently implemented to read one image only. Will be edited to read a bunch of images
    from the folder
    """
    image = cv2.imread(path)
    return image


def get_pixels(image):
    """
    This function returns the list of the pixel that needs to be refilled
    """
    l = []
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            pos = (x, y)
            rgba = image[x][y]
            if rgba[0] == 0 and rgba[1] == 0 and rgba[2] == 0:
                l.append(pos)
    return l


def get_neighboring_pixel(img, x, y, current_window_size):
    """
    Getting the values of the neighbouring pixels
    """
    x_rand, y_rand = 0,0
    max_num_tries = 10000000000
    max_tries_per_neighbourhood = 1000
    neighbourhood_size_increment = 50
    current_window_size = 10
    total_tries = 0

    # Going through the neighbouring pixels
    for _ in range(math.ceil(max_num_tries/max_tries_per_neighbourhood)):
        for _ in range(max_tries_per_neighbourhood):
            min_x = max(0, x-current_window_size)
            max_x = min(img.shape[0], x+current_window_size)
            min_y = max(0, y-current_window_size)
            max_y = min(img.shape[1], y+current_window_size)

            # Finding a random sample inside the given window
            x_rand = random.randint(min_x, max_x-1)
            y_rand = random.randint(min_y, max_y-1)
            total_tries += 1

            # Return the sample if it is not 0,0,0 i.e. black
            if not(img[x_rand][y_rand][0]==0 and img[x_rand][y_rand][1]==0 and img[x_rand][y_rand][2]==0):
                return x_rand, y_rand
        current_window_size += neighbourhood_size_increment
    return x_rand, y_rand


def fill_swath_with_neighboring_pixel(img, left=10, right=100, top=10, bottom=100, color = {0,0,0}, current_window_size = 10):
    """
    Filling method 3:
    Input: image with missing data (numpy array)
    Output: numpy array with missing data filled by random RGB values from non-missing pixel portions of the image selected with probability inversely proportional to distance
    """
    img_with_neighbor_filled = np.array(img.copy())
    l = get_pixels(img)

    for k in l:
        x,y = k
        x_rand, y_rand = get_neighboring_pixel(img, x, y, current_window_size)
        if x >= left and x <= right and y >= top and y <= bottom:
            img_with_neighbor_filled[x][y] = img[x_rand][y_rand]
    return img_with_neighbor_filled


def main(image):
    """
        The main function that can be called as a normal function as well
    """
    neighborfill = fill_swath_with_neighboring_pixel(image, left=0, right=7680, top=0, bottom=7680, color={0, 0, 0},
                                                     current_window_size=3)
    return neighborfill


if __name__ == "__main__":
    image = read_images("images/ImageOverlayOutput.png")
    image = main(image)
    cv2.imwrite("result.png", image)