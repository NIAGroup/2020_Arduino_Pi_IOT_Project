import cv2
#from imutils.video import WebcamVideoStream
#import threading
#import time

# initialize the output frame and create a Lock to allow mutiple connections to the stream
# outputFrame = None
# lock = threading.Lock()

def gen_frames(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0)

    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
           #extracting frames
            ret, frame = self.video.read()
            frame = cv2.flip(frame, flipCode=-1)

            # encode OpenCV raw frame to jpg and displaying it
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
