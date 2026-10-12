"""
Motion-Triggered Security Camera (CSC 126 Midterm Project)

Detects movement from a webcam (or a video file) using classical OpenCV:
  a. Image Operations     - resize, grayscale, Gaussian blur
  b. Image Segmentation   - frame differencing, thresholding, dilation
  e. Motion Tracking      - contours, bounding boxes, object count

When motion is detected, a timestamped screenshot is saved to the captures folder.
Press Q to quit.
"""
try:
    import cv2  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
         "OpenCV is required for this project. Install it with: pip install opencv-python"
    ) from exc

import os
import time
from datetime import datetime


# =============================
# SETTINGS
# =============================

CAMERA_INDEX = 0            # 0 = default webcam, or a path such as "samples/demo.mp4"

FRAME_WIDTH = 800
FRAME_HEIGHT = 600

MIN_CONTOUR_AREA = 3000     # ignore motion regions smaller than this (pixels)
THRESHOLD_VALUE = 25        # minimum brightness change to count as motion
DILATE_ITERATIONS = 2       # how much the white motion regions are expanded

CAPTURE_FOLDER = "captures"
CAPTURE_COOLDOWN = 5        # seconds between saved screenshots

os.makedirs(CAPTURE_FOLDER, exist_ok=True)

last_capture_time = 0


# =============================
# OPEN CAMERA
# =============================

camera = cv2.VideoCapture(CAMERA_INDEX)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()


# =============================
# READ FIRST FRAME
# =============================

ret, previous_frame = camera.read()

if not ret:
    print("ERROR: Could not read camera.")
    camera.release()
    exit()


previous_frame = cv2.resize(
    previous_frame,
    (FRAME_WIDTH, FRAME_HEIGHT)
)

# Convert first frame to grayscale
previous_gray = cv2.cvtColor(
    previous_frame,
    cv2.COLOR_BGR2GRAY
)

# Apply blur
previous_gray = cv2.GaussianBlur(
    previous_gray,
    (21, 21),
    0
)


# =============================
# MAIN LOOP
# =============================

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read frame (or the video has ended).")
        break


    # =============================
    # RESIZE FRAME
    # =============================

    frame = cv2.resize(
        frame,
        (FRAME_WIDTH, FRAME_HEIGHT)
    )


    # =============================
    # IMAGE OPERATIONS
    # =============================

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (21, 21),
        0
    )


    # =============================
    # FRAME DIFFERENCE
    # =============================

    frame_difference = cv2.absdiff(
        previous_gray,
        gray
    )


    # =============================
    # IMAGE SEGMENTATION
    # =============================

    _, threshold = cv2.threshold(
        frame_difference,
        THRESHOLD_VALUE,
        255,
        cv2.THRESH_BINARY
    )

    # Make motion regions clearer
    threshold = cv2.dilate(
        threshold,
        None,
        iterations=DILATE_ITERATIONS
    )


    # =============================
    # FIND CONTOURS
    # =============================

    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    motion_detected = False
    moving_objects = 0


    # =============================
    # PROCESS CONTOURS
    # =============================

    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore small movements
        if area < MIN_CONTOUR_AREA:
            continue

        motion_detected = True
        moving_objects += 1

        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


    # =============================
    # STATUS TEXT
    # =============================

    if motion_detected:
        status = "MOTION DETECTED"
        status_color = (0, 0, 255)      # red
    else:
        status = "MONITORING"
        status_color = (0, 255, 0)      # green

    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        status_color,
        2
    )


    # =============================
    # OBJECT COUNT
    # =============================

    cv2.putText(
        frame,
        f"Moving Objects: {moving_objects}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # =============================
    # DATE AND TIME
    # =============================

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cv2.putText(
        frame,
        current_time,
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # =============================
    # SAVE SCREENSHOT
    # (done after all overlays are drawn, so the saved image
    #  shows the status, boxes, object count, and date/time)
    # =============================

    if motion_detected:

        current_timestamp = time.time()

        if current_timestamp - last_capture_time >= CAPTURE_COOLDOWN:

            filename = datetime.now().strftime(
                "motion_%Y-%m-%d_%H-%M-%S.jpg"
            )

            filepath = os.path.join(
                CAPTURE_FOLDER,
                filename
            )

            cv2.imwrite(
                filepath,
                frame
            )

            print(f"Motion captured: {filepath}")

            last_capture_time = current_timestamp


    # =============================
    # DISPLAY WINDOWS
    # =============================

    cv2.imshow(
        "Motion Detection Security Camera",
        frame
    )

    cv2.imshow(
        "Motion Mask",
        threshold
    )


    # Current frame becomes previous frame
    previous_gray = gray.copy()


    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =============================
# CLEAN UP
# =============================

camera.release()
cv2.destroyAllWindows()