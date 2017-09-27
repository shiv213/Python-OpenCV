import cv2
import numpy as np
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime

pics_folder_id = "0B2Li-r7tPLlaWG00WlpaS1dhblk"

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)


def diffImg(t0, t1):
    return cv2.absdiff(t1, t0)


def upload_and_save(img):
    im_name = "img_" + datetime.now().strftime("%y-%m-%d-%I-%M-%S-%p") + ".jpg"
    cv2.imwrite(im_name, img)
    file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": pics_folder_id}]})
    file.SetContentFile(im_name)
    file.Upload()


def read_img(cam):
    _, frame = cam.read()
    return cv2.GaussianBlur(frame, (5, 5), 0)


cam = cv2.VideoCapture(0)

for i in range(10):
    cam.read()
    time.sleep(0.1)
print("Start")


# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

DELAY_TIME = 5
MOTION_WAIT_FRAMES = 10

frames_with_motion = MOTION_WAIT_FRAMES

MOTION_THRESHOLD = 0.8

LUMINOSITY_THRESHOLD = 120

while True:
    # Read next image
    t_minus = t
    img = cam.read()[1]
    t = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    diff = diffImg(t_minus, t)
    mean_motion = np.mean(diff)
    cv2.putText(diff, "Mean: " + str(mean_motion), (105, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
    print("Average motion", mean_motion)
    hls_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    cv2.imshow("original", t)
    av_sat = np.mean(hls_img[:, :, 2])
    av_lum = np.mean(hls_img[:, :, 1])
    print("Luminosity", av_lum)
    cv2.putText(diff, "Sat: " + str(av_sat), (105, 160), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
    cv2.putText(diff, "Lum: " + str(av_lum), (105, 200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (225, 0, 0))
    cv2.imshow("motion cam", diff)
    upload = True
    if mean_motion < MOTION_THRESHOLD:
        frames_with_motion -= 1
        if frames_with_motion <= 0:
            upload = False
    else:
        frames_with_motion = MOTION_WAIT_FRAMES
    upload = upload and av_lum > LUMINOSITY_THRESHOLD
    if upload:
        print("Uploading...")
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break
    time.sleep(DELAY_TIME)
