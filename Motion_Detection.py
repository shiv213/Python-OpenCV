import cv2
import numpy as np

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

def read_img(cam):
  _, frame=  cam.read()
  return cv2.GaussianBlur(frame, (5, 5), 0)


cam = cv2.VideoCapture(2)

winName = "main"

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

while True:
  diff = diffImg(t_minus, t, t_plus)
  number = (np.mean(diff))
  string = str (number)
  cv2.putText(diff, "Mean: " + string, (105, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
  print (number)
  font = cv2.FONT_HERSHEY_SIMPLEX
  # Read next image
  t_minus = t
  t = t_plus
  img = cam.read()[1]
  t_plus = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  hls_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
  cv2.imshow("original", t)
  av_sat = np.mean(hls_img[:,:,2])
  av_lum = np.mean(hls_img[:,:,1])
  cv2.putText(diff, "Sat: " + str(av_sat), (105, 160), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
  cv2.putText(diff, "Lum: " + str(av_lum), (105, 200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
  cv2.imshow( winName, diff)
  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break
