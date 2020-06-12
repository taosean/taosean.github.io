import cv2
import numpy as np
from ctypes import *

FILE_MAP_ALL_ACCESS = 0xF001F
SHMEMSIZE = 720*480*3
szName = c_char_p('Local\object_name_sean')


hMapObject = windll.kernel32.OpenFileMappingA(FILE_MAP_ALL_ACCESS, False, szName)
if hMapObject == 0:
    print 'Could not open file mapping object'
    raise windll.WindowsError()

pBuf = windll.kernel32.MapViewOfFile(hMapObject, FILE_MAP_ALL_ACCESS, 0, 0, 0)

print pBuf

if pBuf == 0:
    print 'Could not map view of file'
    windll.kernel32.GetLastError()
else:
    pBuf_int = cast(pBuf, POINTER(c_int))
    width, height, channel = pBuf_int[:3]

    data_len = width * height * channel
    pBuf_ubyte = cast(pBuf, POINTER(c_ubyte))
    data_ubyte = pBuf_ubyte[: data_len]  # The pointer is already incremented by 12 bytes, not sure why.

    image = np.asarray(data_ubyte, dtype=np.uint8)
    image = image.reshape((height, width, channel))

    cv2.imshow('python image', image)
    cv2.waitKey()

windll.kernel32.UnmapViewOfFile(pBuf)
windll.kernel32.CloseHandle(hMapObject)