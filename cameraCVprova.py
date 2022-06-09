# Import numpy and OpenCV
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import numpy as np
import cv2
# Read input video
stream = VideoGear(source=0, stabilize = True).start()

while True:
# Capture frame-by-frame

    frame = stream.read()
    if frame is None:
        #if True break the infinite loop
        break
    frame = cv2.flip(frame, 1)
    # Display the resulting fram
    cv2.imshow('preview',frame)
    key = cv2.waitKey(1)
    #Waits for a user input to quit the application
    if key==27: 
         break 

cv2.destroyAllWindows()
stream.stop()