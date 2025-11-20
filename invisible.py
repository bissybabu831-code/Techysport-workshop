import cv2
import numpy as np
import time

# Start webcam
cap = cv2.VideoCapture(0)

# Check if camera works
if not cap.isOpened():
    print("Error: Camera not detected!")
    exit()

print("Capturing background... Stay out of the frame.")
time.sleep(2)

# Capture background
background = None
for i in range(50):
    ret, bg = cap.read()
    if ret:
        background = bg

# If background not captured
if background is None:
    print("Error: Could not capture background.")
    cap.release()
    exit()

# Flip background
background = cv2.flip(background, 1)

print("Starting Invisible Cloak (Blue Color Vanish)...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # BLUE color HSV range
    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])

    # Create blue mask
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Clean mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # Inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Areas
    invisible_area = cv2.bitwise_and(background, background, mask=mask)
    visible_area = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Combine final output
    final_output = cv2.addWeighted(invisible_area, 1, visible_area, 1, 0)

    # Show result
    cv2.imshow("Invisible Cloak (Blue Hide)", final_output)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()