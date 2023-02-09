import os
import sys

import numpy as np
from PIL import Image
import cv2

import datetime
from datetime import date


def pol2cart(rho, phi, origin):
    x = origin[0]+rho*np.cos(phi)
    y = origin[1]+rho*np.sin(phi)
    return (x,y)

# Only for dry months- detect contours and generate a mask (one for each radar)
# Use radial path information 

w = 480
centre = (w//2, w//2)
N = 360
thresholded_image = []
threshold_percent_white = 0.1

thresholded_image = np.array(Image.open(r"colourThresholdResult.png"))

def findRadialInterferences(thresholded_image, threshold_percent_white):
    """
       Given a binarized image, this function finds radial interferences
       by computing the percentage of white pixels in every circular sector
       across the image. Sectors where the percentage of white pixels is
       below a thresold are discarded

       Input:
        thresholded_image (np.array): binary image after color thesolding
        threshold_percent_white (float): a value between 0 and 1 indicating
                            the ratio of white pixels to include a sector
    """

    # create an image of zeros to store the output
    cleaned_img = np.zeros(thresholded_image.shape, dtype=np.uint8)
    w = np.min(thresholded_image.shape)

    # step over circular sectors of 1 degree
    for i in range(0,N,1):
        # get cartesian coordinates of the circular sectors
        p1 = pol2cart(w//2, np.deg2rad(i), origin=(w//2, w//2))
        p2 = pol2cart(w//2, np.deg2rad(i+1), origin=(w//2, w//2))
        
        # draw polygon mask for the sector
        contours = np.array([centre, p1, p2])
        contours = np.int32([contours])
        radial_mask = np.zeros(thresholded_image.shape, dtype=np.uint8)
        cv2.fillPoly(radial_mask, pts = contours, color =(255))
        n_white_pix_total = np.sum(radial_mask == 255)
        
        # compute btiwise and
        result = cv2.bitwise_and(thresholded_image, radial_mask)
        
        # find ratio of white pixels
        percent_white_pix = np.sum(result == 255)/ n_white_pix_total
        
        # compare with threshold
        if percent_white_pix> threshold_percent_white:
            #keep contours if the ratio of white pixels is higher
            cleaned_img = cv2.bitwise_or(result, cleaned_img)
    return cleaned_img

cleaned_img = findRadialInterferences(thresholded_image, threshold_percent_white)
cv2.imshow('image',cleaned_img)
cv2.waitKey(0)



