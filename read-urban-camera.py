import numpy as np
import cv2

def rescale_frame(frame, percent=20):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

cap = cv2.VideoCapture("C:/Users/USER/Downloads/street_camera.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
while(True):
    rec, frame1 = cap.read()
    rec, frame2 = cap.read()

    resized_frame1 = rescale_frame(frame1)
    resized_frame2 = rescale_frame(frame2)

    frame_diff = cv2.absdiff(resized_frame1, resized_frame2)
    frame_diff_gr = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(frame_diff_gr, (9,9), 1)
    _, mask = cv2.threshold(blurred_frame, 10, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    for contour in contours:
        if cv2.contourArea(contour)>1000:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(resized_frame1, (x + w -100, y + h-50), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('frame', resized_frame1)
    cv2.imshow('frame_diff', frame_diff)
    cv2.imshow('mask', mask)
    keyexit = cv2.waitKey(5) & 0xFF
    if keyexit == 27:
        break

cv2.destroyAllWindows()
cap.release()