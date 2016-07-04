from gevent import monkey
from bottle import route, response, run
from time import sleep
monkey.patch_all()

import cv2
import urllib
import gevent

BOUNDARY = "arflebarfle"
CRLF = "\r\n"
jpg = []

def background():
    stream = urllib.urlopen('http://127.0.0.1:8000/mjpeg?action=stream/frame.mjpg')
    bytes = ''

    while True:
        bytes += stream.read(1024)

        # Use Start and End of Image markers to find each image in the stream...
        start = bytes.find('\xff\xd8')
        end = bytes.find('\xff\xd9')

        if start != -1 and end != -1:
            global jpg 
            jpg = bytes[start:end + 2]
            bytes = bytes[end + 2:]        
            gevent.sleep(1.0 / 30)

@route('/')
def index():
    return '<html><body><img src="/mjpeg" /></body></html>'

@route('/mjpeg')
def mjpeg():
    response.content_type = "multipart/x-mixed-replace;boundary=" + BOUNDARY
    while True:
        out = "--" + BOUNDARY + CRLF
        out += "Content-type: image/jpeg" + CRLF
        out += "Content-length: " + str(len(jpg)) + CRLF + CRLF
        yield out + jpg + CRLF
        gevent.sleep(1.0 / 30)
        
background_task = gevent.spawn(background)    
main_task = run(host='127.0.0.1', port=8001, debug=False, server='gevent')
gevent.joinall([main_task, background_task])