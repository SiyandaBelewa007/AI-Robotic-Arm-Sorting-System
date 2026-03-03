import cv2
import serial
import numpy as np

# Initialize serial communication with Arduino
ser = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino's port

# Initialize webcam
cap = cv2.VideoCapture(0)

# Define the color range for object detection (e.g., yellow)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)


    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)
        # Get the bounding box
        x, y, w, h = cv2.boundingRect(c)
        # Calculate the center of the object
        cx = x + w // 2
        cy = y + h // 2

        # Draw the contour and center on the frame
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        # Map the center position to servo angles
        base_angle = np.interp(cx, [0, 640], [0, 180])
        elbow_angle = np.interp(cy, [0, 480], [0, 180])

        # Send the angles to Arduino
        ser.write(bytes([int(base_angle), int(elbow_angle), int(elbow_angle)]))

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
