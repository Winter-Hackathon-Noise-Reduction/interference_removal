# -*- coding: utf-8 -*-
"""netCDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QtE985fn2j4RRVE9BL3q2Ie5EVEpgk-U
"""

import netCDF4 as nc
import numpy as np
from PIL import Image

jpeg = Image.open(r"/content/WhatsApp Image 2023-02-09 at 7.51.52 PM.jpeg")
gif = jpeg.save("img.gif")
im = np.array(Image.open("img.gif"))
print(im.shape[0])

def initialise_CDF(img_shape):
  fn = 'netCDF.nc'
  ds = nc.Dataset(fn, 'w', format='NETCDF4')

  time = ds.createDimension('time', None)
  lat = ds.createDimension('lat', img_shape[0])
  lon = ds.createDimension('lon', img_shape[1])

  times = ds.createVariable('time', 'f4', ('time',))
  lats = ds.createVariable('lat', 'f4', ('lat',))
  lons = ds.createVariable('lon', 'f4', ('lon',))
  value = ds.createVariable('value', 'f4', ('time', 'lat', 'lon',))
  value.units = 'Unknown'

  return (ds, value)

def create_net_CDF(img, index):
  ds, value = initialise_CDF(img.shape)
  value[index, :, :] = img
  return ds

ds = create_net_CDF(im, 0)
print(ds)

# time = ds.createDimension('time', None)
# lat = ds.createDimension('lat', 530)
# lon = ds.createDimension('lon', 480)

# times = ds.createVariable('time', 'f4', ('time',))
# lats = ds.createVariable('lat', 'f4', ('lat',))
# lons = ds.createVariable('lon', 'f4', ('lon',))
# value = ds.createVariable('value', 'f4', ('time', 'lat', 'lon',))
# value.units = 'Unknown'
# value[0, :, :] = im

