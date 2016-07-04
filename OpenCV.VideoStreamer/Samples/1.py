import cv2
import numpy as np
import urllib

stream = urllib.urlopen('http://127.0.0.1:8000/mjpeg?action=stream/frame.mjpg')
bytes = ''
bufsize = 100
bufpos = 0
buf = [0 for i in range(bufsize)]

while bufpos < bufsize:
    bytes += stream.read(1024)

    # Use Start and End of Image markers to find each image in the stream...
    start = bytes.find('\xff\xd8')
    end = bytes.find('\xff\xd9')

    if start != -1 and end != -1:
        jpg = bytes[start:end + 2]
        #buf[bufpos] = jpg
        bufpos += 1

        bytes = bytes[end + 2:]        
        mat = np.fromstring(jpg, dtype=np.uint8)
        i = cv2.imdecode(mat, cv2.IMREAD_COLOR)
        cv2.imshow('i',i)

#for frame in buf:
#    mat = np.fromstring(frame, dtype=np.uint8)
#    i = cv2.imdecode(mat, cv2.IMREAD_COLOR)
#    cv2.imshow('out',i)
