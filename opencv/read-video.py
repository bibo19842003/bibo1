import sys
import cv2
#import numpy as np

cap = cv2.VideoCapture("112.mp4") 

# Returns true if video capturing has been initialized already
if not cap.isOpened(): 
    sys.exit()

rate=cap.get(cv2.CAP_PROP_FPS) 
delay = int(1000 / rate)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

# Closes video file or capturing device.
cap.release()

cv2.destroyAllWindows()
