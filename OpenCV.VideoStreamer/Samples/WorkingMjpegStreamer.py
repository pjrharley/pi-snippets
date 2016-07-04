from gevent import monkey; monkey.patch_all()
from bottle import route, response, run
from time import sleep
import cv2

BOUNDARY = "arflebarfle"
CRLF = "\r\n"
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

class MJPEG(object):
    def __init__(self):
        pass

    def __iter__(self):
        return self

    def next(self):
        sleep(30.0 / 1000)
        cap_succeded, raw_frame = cap.read()
        convert_succeded, jpg_frame = cv2.imencode(".jpg", raw_frame)

        out = "--" + BOUNDARY + CRLF
        out += "Content-type: image/jpeg" + CRLF
        out += "Content-length: " + str(len(jpg_frame)) + CRLF + CRLF
        return out + jpg_frame.tostring() + CRLF

    def stop(self):
        pass


@route('/')
def index():
    return '<html><body><img src="/mjpeg" /></body></html>'

@route('/mjpeg')
def mjpeg():
    response.content_type = "multipart/x-mixed-replace;boundary=" + BOUNDARY
    return iter(MJPEG())


run(host='127.0.0.1', port=8000, debug=True)