import cv2
import numpy as np

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)

winName = "Motion Detection"

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

while True:
  diff = diffImg(t_minus, t, t_plus)
  number = (np.mean(diff))
  string = str (number)
  cv2.putText(diff, "Mean: " + string, (105, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
  cv2.imshow( winName, diff)
  # print (number)
  font = cv2.FONT_HERSHEY_SIMPLEX
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
  if number > 1.5:
    cv2.putText(diff, "Motion Detected", (105, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break
