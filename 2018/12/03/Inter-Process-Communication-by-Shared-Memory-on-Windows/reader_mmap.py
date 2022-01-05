import mmap
from ctypes import *
import struct
import numpy as np
import cv2


shm = mmap.mmap(0, 720*480*3+12, "object_name_sean", mmap.ACCESS_READ)

print shm
if shm:
    header = shm.read(12)
    width_str = header[:4]
    height_str = header[4:8]
    channel_str = header[8:12]

    width = struct.unpack('<i', width_str)[0]
    height = struct.unpack('<i', height_str)[0]
    channel = struct.unpack('<i', channel_str)[0]

    print width, height, channel

    data = shm.read(width * height * channel)

    img_data = [ord(x) for x in data]
    print img_data[:10]

    image = np.asarray(img_data, dtype=np.uint8)
    image = image.reshape((height, width, channel))

    cv2.imshow('python image', image)
    cv2.waitKey()

shm.close()
