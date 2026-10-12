# Motion-Triggered Security Camera

A computer vision application that monitors a webcam feed (or a recorded video), detects movement in real time, and automatically saves timestamped screenshots when motion occurs.

Built with Python and OpenCV for the **CSC 126 Computer Vision Midterm Project**.

## Problem it solves

Commercial security systems are expensive, and watching camera footage all day is tiring. Recording 24/7 also wastes storage because most footage has no activity. This project uses an ordinary webcam and free software. It stays in a MONITORING state and reacts only when something moves: it highlights the moving object, shows an alert, and saves a screenshot with the date and time.

## Features

- Live webcam monitoring with **MONITORING** (green) / **MOTION DETECTED** (red) status
- Green bounding boxes around moving objects
- Moving object counter
- Date and time overlay
- Separate **Motion Mask** window showing the segmented motion
- Automatic screenshot saving with a 5-second cooldown

## OpenCV techniques used

| Topic | Functions | Purpose |
|---|---|---|
| **a. Image Operations** | `resize`, `cvtColor`, `GaussianBlur` | Standardize frames, convert to grayscale, remove noise |
| **b. Image Segmentation** | `absdiff`, `threshold`, `dilate` | Build a binary motion mask from frame differences |
| **e. Motion and Object Tracking** | `findContours`, `contourArea`, `boundingRect` | Detect, filter, and box moving objects |

## How it works

1. Read a frame and resize it to 800x600.
2. Convert it to grayscale and apply Gaussian blur (21x21).
3. Compute the absolute difference with the previous frame.
4. Apply a threshold (25) and dilate (2 iterations) to create the motion mask.
5. Find contours and ignore those smaller than 3000 pixels.
6. Draw bounding boxes, the status label, the object count, and the date and time.
7. If motion is detected and the cooldown has passed, save a screenshot to `captures/`.
8. Show the result and the motion mask. The current frame becomes the previous frame for the next loop.

## Project structure

```
motion-security-camera/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── Documentation.pdf
├── captures/        (saved motion screenshots)
├── samples/         (sample input video)
├── screenshots/     (screenshots used in the documentation)
└── testing/         (Member 2's testing notebook and results)
```

## Requirements

- Python 3.8 or newer
- A webcam (or a video file)
- OpenCV (installed through `requirements.txt`)

## Setup

1. Clone the repository:
```
   git clone <your-repository-link>
   cd motion-security-camera
```
2. Install the dependencies:
```
   pip install -r requirements.txt
```

## How to run

```
python main.py
```

- Press **Q** to quit.
- Screenshots are saved in the `captures/` folder with a timestamped filename, for example `motion_2026-10-12_14-30-05.jpg`.
- To use a recorded video instead of the webcam, change `CAMERA_INDEX` at the top of `main.py` to the video path, for example `CAMERA_INDEX = "samples/demo.mp4"`.

## Settings

All settings are at the top of `main.py`.

| Setting | Default | Description |
|---|---|---|
| `CAMERA_INDEX` | `0` | Webcam number, or a path to a video file |
| `FRAME_WIDTH` / `FRAME_HEIGHT` | `800` / `600` | Processing resolution |
| `MIN_CONTOUR_AREA` | `3000` | Smallest motion region (in pixels) that is counted |
| `THRESHOLD_VALUE` | `25` | Minimum brightness change to count as motion |
| `DILATE_ITERATIONS` | `2` | How much the motion regions are expanded |
| `CAPTURE_COOLDOWN` | `5` | Seconds between saved screenshots |

## Testing

Three settings were tested on the same 272-frame video (see the `testing/` folder):

| Test | Min area | Threshold | Dilation | Detection rate | Small movement | Large / slow movement |
|---|---|---|---|---|---|---|
| A - Sensitive | 500 | 20 | 2 | 84.93% | Detected | Detected |
| B - Original (default) | 3000 | 25 | 2 | 68.75% | Detected | Detected |
| C - Less Sensitive | 5000 | 30 | 3 | 43.01% | Not detected | Detected |

Lower values make the system more sensitive. Test B is the default because it detects small movement while giving cleaner bounding boxes. Test A is better when small movement is the priority, but it draws many more boxes per frame.

## Limitations

- Sudden lighting changes and camera auto-exposure can cause false motion.
- Moving shadows may be detected as motion.
- Stationary or very slow objects are not detected, since only consecutive frames are compared.
- Nearby moving objects may merge into one box, so the count is approximate.
- The system cannot identify what is moving (person, animal, or object).
- Camera movement makes the whole frame appear as motion.

## Possible improvements

- Background subtraction (`MOG2`) for better stability
- Region of interest, so only important areas trigger alerts
- Sound, email, or SMS alerts
- Recording short video clips
- Combining with a Haar cascade to confirm that a person is present

## Team

- **Member 1:** [Andrea Glecy Semine]
- **Member 2:** [Jecil Mae Vesagas]
- **Member 3:** [Beverly Nicole Siton]

CSC 126 - Computer Vision | [Caraga State University - BJY21 ] | [Sir Josh Tubo]