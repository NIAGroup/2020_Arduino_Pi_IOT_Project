import cv2, threading

class VideoCamera(object):
    def __init__(self):
        self.isCameraActive = True
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        self.frame = cv2.flip(self.frame,flipCode=-1)
        # Adding threading to reduce demand on resources
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = cv2.flip(self.frame,flipCode=-1)
        ret, jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    def update(self):
        while self.isCameraActive:
            (self.grabbed, self.frame) = self.video.read()

def gen_frames(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
