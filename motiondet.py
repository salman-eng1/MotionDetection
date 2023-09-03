import pygetwindow as gw
import subprocess
import cv2

ps_command = "taskkill /im PhotoScreensaver.scr /f"

# Initialize the camera (outside the loop)
camera = cv2.VideoCapture(0)  # You might need to adjust the camera index

# Set the desired frame rate for the camera
desired_frame_rate = 10
camera.set(cv2.CAP_PROP_FPS, desired_frame_rate)

# Set the initial state for motion detection and screen saver
motion_detected = False
prev_screen_saver_state = False  # Assuming the screen saver is initially off

while True:
    # Check screen saver state
    screen_saver_state = gw.getActiveWindow() is None

    if screen_saver_state and not prev_screen_saver_state:
        # Screen saver turned on
        # Initialize camera and previous frame
        camera.release()  # Release any existing camera capture
        camera = cv2.VideoCapture(0)
        ret, prev_frame = camera.read()
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    if not screen_saver_state and prev_screen_saver_state:
        # Screen saver turned off
        camera.release()  # Release the camera

    prev_screen_saver_state = screen_saver_state

    if screen_saver_state:
        # Capture a frame from the camera
        ret, frame = camera.read()

        # Convert the frame to grayscale for motion detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise and improve accuracy
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # Calculate the absolute difference between the previous frame and the current frame
        frame_delta = cv2.absdiff(prev_gray, gray_frame)

        # Apply a threshold to the frame delta
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Check for motion in the bottom 160 pixels
        detected = False
        if thresh[thresh.shape[0] - 70:, :].any():  # Check if there's any motion in the bottom 160 pixels
            detected = True

        if detected and not motion_detected:
            subprocess.call(["powershell.exe", ps_command])
            print("Motion detected")
            motion_detected = True
        elif not detected and motion_detected:
            subprocess.call(["powershell.exe", "tasklist", "/fi", "imagename eq PhotoScreensaver.scr"])
            motion_detected = False

        # Update the previous frame
        prev_gray = gray_frame.copy()

    # Introduce a delay without interruption
    cv2.waitKey(int(1000 / desired_frame_rate))  # Delay in milliseconds

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
camera.release()
cv2.destroyAllWindows()
