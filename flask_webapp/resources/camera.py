from flask_restful import Resource
from models.camera import VideoCamera

class Camera(Resource):
    def get(self):
        print('Turn on Webcam')
        # return the response generated along with the specific  media
        # type (mime type)
        return Response(gen_frames(VideoCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')
