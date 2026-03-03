import cv2
import numpy as np

# --- Helper function to create trackbars ---
def nothing(x):
    pass

# Open camera stream (IP Webcam)
url = "http://192.168.137.67:8080/video"
cap = cv2.VideoCapture(url)

# --- Create a window for trackbars ---
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trackbars", 500, 600)

# Create HSV range trackbars for each color
# RED (needs two ranges because red wraps around 0)
cv2.createTrackbar("Red H Low1", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Red H High1", "Trackbars", 10, 179, nothing)
cv2.createTrackbar("Red H Low2", "Trackbars", 160, 179, nothing)
cv2.createTrackbar("Red H High2", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Red S Low", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("Red S High", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Red V Low", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("Red V High", "Trackbars", 255, 255, nothing)

# YELLOW
cv2.createTrackbar("Yellow H Low", "Trackbars", 20, 179, nothing)
cv2.createTrackbar("Yellow H High", "Trackbars", 30, 179, nothing)
cv2.createTrackbar("Yellow S Low", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("Yellow S High", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Yellow V Low", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("Yellow V High", "Trackbars", 255, 255, nothing)

# GREEN
cv2.createTrackbar("Green H Low", "Trackbars", 35, 179, nothing)
cv2.createTrackbar("Green H High", "Trackbars", 85, 179, nothing)
cv2.createTrackbar("Green S Low", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("Green S High", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Green V Low", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("Green V High", "Trackbars", 255, 255, nothing)

# BLUE
cv2.createTrackbar("Blue H Low", "Trackbars", 100, 179, nothing)
cv2.createTrackbar("Blue H High", "Trackbars", 130, 179, nothing)
cv2.createTrackbar("Blue S Low", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("Blue S High", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Blue V Low", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("Blue V High", "Trackbars", 255, 255, nothing)

# BLACK - Improved parameters
cv2.createTrackbar("Black S Low", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Black S High", "Trackbars", 80, 255, nothing)
cv2.createTrackbar("Black V Low", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Black V High", "Trackbars", 80, 255, nothing)

# Minimum contour area
cv2.createTrackbar("Min Area", "Trackbars", 300, 2000, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- Read Trackbar positions ---
    # Red (two ranges)
    red_h_low1 = cv2.getTrackbarPos("Red H Low1", "Trackbars")
    red_h_high1 = cv2.getTrackbarPos("Red H High1", "Trackbars")
    red_h_low2 = cv2.getTrackbarPos("Red H Low2", "Trackbars")
    red_h_high2 = cv2.getTrackbarPos("Red H High2", "Trackbars")
    red_s_low = cv2.getTrackbarPos("Red S Low", "Trackbars")
    red_s_high = cv2.getTrackbarPos("Red S High", "Trackbars")
    red_v_low = cv2.getTrackbarPos("Red V Low", "Trackbars")
    red_v_high = cv2.getTrackbarPos("Red V High", "Trackbars")

    # Yellow
    yellow_h_low = cv2.getTrackbarPos("Yellow H Low", "Trackbars")
    yellow_h_high = cv2.getTrackbarPos("Yellow H High", "Trackbars")
    yellow_s_low = cv2.getTrackbarPos("Yellow S Low", "Trackbars")
    yellow_s_high = cv2.getTrackbarPos("Yellow S High", "Trackbars")
    yellow_v_low = cv2.getTrackbarPos("Yellow V Low", "Trackbars")
    yellow_v_high = cv2.getTrackbarPos("Yellow V High", "Trackbars")

    # Green
    green_h_low = cv2.getTrackbarPos("Green H Low", "Trackbars")
    green_h_high = cv2.getTrackbarPos("Green H High", "Trackbars")
    green_s_low = cv2.getTrackbarPos("Green S Low", "Trackbars")
    green_s_high = cv2.getTrackbarPos("Green S High", "Trackbars")
    green_v_low = cv2.getTrackbarPos("Green V Low", "Trackbars")
    green_v_high = cv2.getTrackbarPos("Green V High", "Trackbars")

    # Blue
    blue_h_low = cv2.getTrackbarPos("Blue H Low", "Trackbars")
    blue_h_high = cv2.getTrackbarPos("Blue H High", "Trackbars")
    blue_s_low = cv2.getTrackbarPos("Blue S Low", "Trackbars")
    blue_s_high = cv2.getTrackbarPos("Blue S High", "Trackbars")
    blue_v_low = cv2.getTrackbarPos("Blue V Low", "Trackbars")
    blue_v_high = cv2.getTrackbarPos("Blue V High", "Trackbars")

    # Black - now with all parameters
    black_s_low = cv2.getTrackbarPos("Black S Low", "Trackbars")
    black_s_high = cv2.getTrackbarPos("Black S High", "Trackbars")
    black_v_low = cv2.getTrackbarPos("Black V Low", "Trackbars")
    black_v_high = cv2.getTrackbarPos("Black V High", "Trackbars")

    min_area = cv2.getTrackbarPos("Min Area", "Trackbars")

    # --- Create masks for each color ---
    # Red mask (two ranges combined)
    red_mask1 = cv2.inRange(hsv, (red_h_low1, red_s_low, red_v_low), (red_h_high1, red_s_high, red_v_high))
    red_mask2 = cv2.inRange(hsv, (red_h_low2, red_s_low, red_v_low), (red_h_high2, red_s_high, red_v_high))
    mask_red = cv2.bitwise_or(red_mask1, red_mask2)

    mask_yellow = cv2.inRange(hsv, (yellow_h_low, yellow_s_low, yellow_v_low), 
                             (yellow_h_high, yellow_s_high, yellow_v_high))
    mask_green = cv2.inRange(hsv, (green_h_low, green_s_low, green_v_low), 
                            (green_h_high, green_s_high, green_v_high))
    mask_blue = cv2.inRange(hsv, (blue_h_low, blue_s_low, blue_v_low), 
                           (blue_h_high, blue_s_high, blue_v_high))
    
    # Improved black mask - focus on low saturation AND low value
    mask_black = cv2.inRange(hsv, (0, black_s_low, black_v_low), (180, black_s_high, black_v_high))

    # Combine all masks
    combined_mask = cv2.bitwise_or(mask_red, mask_yellow)
    combined_mask = cv2.bitwise_or(combined_mask, mask_green)
    combined_mask = cv2.bitwise_or(combined_mask, mask_blue)
    combined_mask = cv2.bitwise_or(combined_mask, mask_black)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # Apply to frame
    result = cv2.bitwise_and(frame, frame, mask=combined_mask)

    # Draw contours and label colors
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(c)
            
            # Create individual mask for this contour
            contour_mask = np.zeros(combined_mask.shape[:2], np.uint8)
            cv2.drawContours(contour_mask, [c], -1, 255, -1)
            
            # Get mean HSV values for this contour
            mean_hue = cv2.mean(hsv[:,:,0], mask=contour_mask)[0]
            mean_sat = cv2.mean(hsv[:,:,1], mask=contour_mask)[0]
            mean_val = cv2.mean(hsv[:,:,2], mask=contour_mask)[0]
            
            # Color classification logic - CHECK BLACK FIRST
            label = "Unknown"
            color = (128, 128, 128)  # Default gray
            
            # Check black first (most restrictive)
            if black_s_low <= mean_sat <= black_s_high and black_v_low <= mean_val <= black_v_high:
                label = "Black"
                color = (0, 0, 0)
            # Check red (two ranges)
            elif ((red_h_low1 <= mean_hue <= red_h_high1) or 
                  (red_h_low2 <= mean_hue <= red_h_high2)) and \
                 red_s_low <= mean_sat <= red_s_high and \
                 red_v_low <= mean_val <= red_v_high:
                label = "Red"
                color = (0, 0, 255)
            # Check yellow
            elif yellow_h_low <= mean_hue <= yellow_h_high and \
                 yellow_s_low <= mean_sat <= yellow_s_high and \
                 yellow_v_low <= mean_val <= yellow_v_high:
                label = "Yellow"
                color = (0, 255, 255)
            # Check green
            elif green_h_low <= mean_hue <= green_h_high and \
                 green_s_low <= mean_sat <= green_s_high and \
                 green_v_low <= mean_val <= green_v_high:
                label = "Green"
                color = (0, 255, 0)
            # Check blue
            elif blue_h_low <= mean_hue <= blue_h_high and \
                 blue_s_low <= mean_sat <= blue_s_high and \
                 blue_v_low <= mean_val <= blue_v_high:
                label = "Blue"
                color = (255, 0, 0)

            # Draw bounding box and label
            cv2.rectangle(result, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(result, f"{label}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"{label}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)
            
            # Debug information for black detection
            if label == "Black":
                print(f"Black detected - Saturation: {mean_sat:.1f}, Value: {mean_val:.1f}")

    # Show output windows
    cv2.imshow("Original", frame)
    cv2.imshow("Detected Colors", result)
    cv2.imshow("Combined Mask", combined_mask)
    
    # Show individual masks for debugging
    cv2.imshow("Red Mask", mask_red)
    cv2.imshow("Yellow Mask", mask_yellow)
    cv2.imshow("Green Mask", mask_green)
    cv2.imshow("Blue Mask", mask_blue)
    cv2.imshow("Black Mask", mask_black)

    # Display current black detection parameters
    params_display = np.zeros((100, 400, 3), np.uint8)
    cv2.putText(params_display, f"Black S: {black_s_low}-{black_s_high}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(params_display, f"Black V: {black_v_low}-{black_v_high}", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.imshow("Black Params", params_display)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()