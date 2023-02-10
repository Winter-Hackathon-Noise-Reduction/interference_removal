import os, sys
import numpy as np
import cv2
import imutils
from datetime import datetime
from PIL import Image


from imagePreprocessing import perform_preprocessing
from image_reconstruction import main
from netcdf import create_net_CDF

## function to overlap the images from the three radars together
def overlap_maps(images):
    final_images = []
    for image_path in images:
        cap = cv2.VideoCapture(image_path)
        ret, image = cap.read()
        cap.release()
        
        if ret:
            final_images.append(image)
        
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(final_images)

    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

radar_names = ["ba", "pm", "va"]

data_path = r"C:\Users\upech\Downloads\transfer_221072_files_ec30eaf2\dataset_v1\aemet\10min"

year = [2022]
month_day_mappings = {1: 31, 2: 28, 3:31, 4: 30, 5: 31}

complete_missing_data = {}

time_stamps = [format(num, "04") for num in range(0, 2400, 10)]

year = 2022
dry_months = [1,2]
wet_months = [4,5]

dry_months_data = {}
wet_months_data = {}

# function to get the months data files
def get_month_data(months):
    months_data = {}
    for month in months:
        num_days = month_day_mappings[month]
        for day in range(1, num_days+1):
            for radar in radar_names:
                specific_folder_path = os.path.join(data_path, radar)
                date = "{0}{1}{2}".format(year, format(month, "02"), format(day, "02"))
                for stamp in time_stamps:
                    time_stamp_data = []
                    possible_file_name = "aemet_{0}_{1}{2}.gif".format(radar, date, stamp)
                    image_file_path = os.path.join(data_path, radar, date, possible_file_name)
                    if os.path.isfile(image_file_path):
                        date_time_stamp = "{0}{1}".format(date, stamp)
                        if date_time_stamp not in months_data:
                            months_data[date_time_stamp] = {}
                        months_data[date_time_stamp][radar] = image_file_path

    return months_data

dry_months_data = get_month_data(dry_months)

image_path = r"dataset_v1\aemet\10min\ba\20220101\aemet_ba_202201010010.gif"
preprocessed_image_path = perform_preprocessing(image_path)
refilled_image = main(preprocessed_image_path)
cv2.imshow('image', refilled_image)
cv2.waitKey(0)
refilled_image_array = np.array(refilled_image)

ds = create_net_CDF(refilled_image_array, 0)
print(ds)