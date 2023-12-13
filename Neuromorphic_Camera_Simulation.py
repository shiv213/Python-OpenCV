import cv2
import numpy as np


def calculate_flux_change(current_frame, previous_frame):
    # Convert both frames to grayscale
    gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray_previous = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

    # Calculate the difference in intensity (flux)
    flux_change = cv2.absdiff(gray_current, gray_previous)

    return flux_change


def main(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    ret, previous_frame = cap.read()
    if not ret:
        print("Error reading first frame")
        return

    while cap.isOpened():
        ret, current_frame = cap.read()
        if not ret:
            break

        # Calculate the change in flux
        flux_change_view = calculate_flux_change(current_frame, previous_frame)

        # Display the resulting frames
        cv2.imshow('Normal View', current_frame)
        cv2.imshow('Flux Change View', flux_change_view)

        # Update the previous frame
        previous_frame = current_frame.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = 'people_walking.mp4'
    main(video_path)
