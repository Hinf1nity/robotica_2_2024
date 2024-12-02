import cv2
import numpy as np

# Take a picture everytime the letter p is pressed and quite when q is pressed
cap = cv2.VideoCapture(2)
i = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Take a picture", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('p'):
        # Save the image in calibration_images folder
        saved = cv2.imwrite(f"calibration_images/picture_{i}.jpg", frame)
        if not saved:
            print("Error: Image not saved.")
        else:
            print(f"Picture {i} taken.")
            i += 1
    elif key == ord('q'):
        break
