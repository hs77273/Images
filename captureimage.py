import cv2
from datetime import datetime
import os

cap1 = cv2.VideoCapture(0)
if not cap1.isOpened():
    print("Error: Could not open camera 1")
    exit()

cap2 = cv2.VideoCapture(1)
if not cap2.isOpened():
    print("Error: Could not open camera 2")
    exit()

save_folder = "captures"

while True:
    ret1, frame1 = cap1.read()
    if not ret1:
        print("Error: Unable to read frame from camera 1")
        break

    ret2, frame2 = cap2.read()
    if not ret2:
        print("Error: Unable to read frame from camera 2")
        break

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    seat_coordinates = [(15, 508, 320, 10, "A1"),(564, 508, 896, 10, "A2"),(920, 508, 1234, 5, "B1"),(1429, 508, 1767, 11, "B2")]
    concatenated_frame = cv2.hconcat([frame1, frame2])
    os.makedirs(save_folder, exist_ok=True)

    for i, ((x1, y1, x2, y2, name), color) in zip(seat_coordinates, colors):
        seat_roi = concatenated_frame[y2:y1, x1:x2]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"{save_folder}/Seat_{name}_{timestamp}.png"
        cv2.imwrite(image_filename, seat_roi)

        cv2.rectangle(concatenated_frame, (x1, y2), (x2, y1), color, 5)
        cv2.putText(concatenated_frame, f"Seat {name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

    cv2.imshow('Concatenated Frames', concatenated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
