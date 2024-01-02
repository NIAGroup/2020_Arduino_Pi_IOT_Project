import cv2 
import numpy as np
 
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read() ##~ This line creates an instance of the frame to display the camera feed
    frame = cv2.flip(frame,flipCode=-1)
    cv2.imshow('Frame', frame)
    
    if (key := cv2.waitKey(1)) == 115:
        break
    
cap.release()
cv2.destroyAllWindows()
