import os
import reportlab.lib.pagesizes
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, KeepTogether)
from reportlab.lib.utils import ImageReader

# ---------- EDIT THESE ----------
MEMBERS = ["Andrea Glecy Semine", "Beverly Nicole Siton", "Jecil Mae Vesagas"]
COURSE_INFO = "CSC 126 (BJY21) - Computer Vision | Midterm Project"
OUTPUT = "Documentation.pdf"
# --------------------------------

SHOT_DIR = "screenshots"
FIGURES = [
    ("01_monitoring", "Figure 1. Normal monitoring state (green MONITORING label, count of 0)."),
    ("02_motion_detected", "Figure 2. Motion detected: red MOTION DETECTED label, bounding box, object count, date and time."),
    ("03_bounding_box", "Figure 3. Close-up of the green bounding box drawn around a moving object."),
    ("04_motion_mask", "Figure 4. Motion Mask window: white regions are pixels that changed between frames."),
    ("05_saved_capture", "Figure 5. Automatically saved screenshot in the captures folder (timestamped filename)."),
]

ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=10,
                      leading=13.5, alignment=TA_JUSTIFY, spaceAfter=5)
h1 = ParagraphStyle("h1", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12.5,
                    textColor=colors.HexColor("#1F3A5F"), spaceBefore=9, spaceAfter=4)
title = ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=18,
                       textColor=colors.HexColor("#1F3A5F"), spaceAfter=2, leading=22)
sub = ParagraphStyle("sub", parent=body, alignment=TA_CENTER, fontSize=9.5,
                     textColor=colors.HexColor("#444444"), spaceAfter=2)
cap = ParagraphStyle("cap", parent=body, fontSize=8, leading=10, alignment=TA_CENTER,
                     textColor=colors.HexColor("#333333"), spaceAfter=6)
cell = ParagraphStyle("cell", parent=body, fontSize=8.7, leading=11, alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=2.5)

def P(t, s=body): return Paragraph(t, s)
def B(t): return Paragraph(t, bullet, bulletText="\u2022")

def figure(key, caption, w=3.2 * inch, h=2.1 * inch):
    path = None
    for ext in (".png", ".jpg", ".jpeg"):
        p = os.path.join(SHOT_DIR, key + ext)
        if os.path.exists(p):
            path = p
            break
    if path:
        iw, ih = ImageReader(path).getSize()
        scale = min(w / iw, h / ih)
        img = Image(path, width=iw * scale, height=ih * scale)
    else:
        img = Table([[P("[ Insert screenshot: %s ]" % key, cap)]], colWidths=[w], rowHeights=[h])
        img.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.grey),
                                 ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F2F2")),
                                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    t = Table([[img], [P(caption, cap)]], colWidths=[3.35 * inch])
    t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t

story = []

# ---------------- Title ----------------
story += [P("Motion-Triggered Security Camera Using OpenCV", title),
          P(COURSE_INFO, sub),
          P("Members: " + "; ".join(MEMBERS), sub),
          Spacer(1, 4)]

# ---------------- 1. Objectives ----------------
story.append(P("1. Project Title and Objectives", h1))
story.append(P("<b>Title:</b> Motion-Triggered Security Camera Using Frame Differencing in OpenCV."))
story.append(P("<b>General objective:</b> To design and implement a working computer vision application "
               "in Python and OpenCV that monitors a webcam feed (or a recorded video), detects movement in "
               "real time, and automatically saves evidence of the detected motion."))
story.append(P("<b>Specific objectives:</b>", ParagraphStyle("x", parent=body, spaceAfter=2)))
story += [B("Apply image operations (resizing, grayscale conversion, Gaussian blur) to prepare each frame for analysis."),
          B("Segment moving regions from the static background using frame differencing, thresholding, and dilation."),
          B("Detect and track moving objects using contours and bounding boxes, and count them on every frame."),
          B("Display a clear on-screen status (MONITORING / MOTION DETECTED), object count, and date and time."),
          B("Automatically save timestamped screenshots when motion occurs, with a cooldown to prevent flooding the storage.")]

# ---------------- 2. Problem ----------------
story.append(P("2. Description of the Problem / Use Case", h1))
story.append(P("Small homes, shops, offices, and school rooms often need basic surveillance, but commercial "
               "security systems can be expensive, and manually watching camera footage for long hours is "
               "tiring and unreliable. Recording continuously also wastes storage because most footage "
               "contains nothing happening. This project addresses the problem with a low-cost solution that "
               "uses only an ordinary webcam and free software. The system stays idle in a MONITORING state and "
               "reacts only when something moves: it highlights the moving object, raises a visible alert, and "
               "stores a screenshot with the date and time, so a person only needs to review the saved captures "
               "instead of hours of video."))

# ---------------- 3. Techniques ----------------
story.append(P("3. Techniques Used", h1))
story.append(P("The project uses three of the laboratory topics: <b>(a) Image Operations</b>, "
               "<b>(b) Image Segmentation</b>, and <b>(e) Motion and Object Tracking</b>. The table below "
               "summarizes the OpenCV functions applied and the reason for each."))

rows = [
    [P("Topic", cellb), P("OpenCV function", cellb), P("Purpose in this project", cellb)],
    [P("a. Image Operations", cell), P("<font face='Courier'>cv2.resize</font>", cell),
     P("Scales every frame to 800x600 so processing speed and thresholds are consistent regardless of camera resolution.", cell)],
    [P("a. Image Operations", cell), P("<font face='Courier'>cv2.cvtColor</font> (BGR to gray)", cell),
     P("Removes color information. Motion is detected from brightness changes, so one channel is enough and it is faster to process.", cell)],
    [P("a. Image Operations", cell), P("<font face='Courier'>cv2.GaussianBlur</font> (21x21)", cell),
     P("Smooths the image to suppress camera sensor noise and tiny lighting flicker that would otherwise appear as false motion.", cell)],
    [P("b. Image Segmentation", cell), P("<font face='Courier'>cv2.absdiff</font>", cell),
     P("Computes the absolute pixel difference between the previous and current frame. Static areas become near-black; moving areas become bright.", cell)],
    [P("b. Image Segmentation", cell), P("<font face='Courier'>cv2.threshold</font> (25, binary)", cell),
     P("Converts the difference image into a binary motion mask: pixels that changed by more than 25 intensity levels become white (255), the rest black (0).", cell)],
    [P("b. Image Segmentation", cell), P("<font face='Courier'>cv2.dilate</font> (2 iterations)", cell),
     P("Expands the white regions so that fragmented parts of one moving object merge into a single solid blob.", cell)],
    [P("e. Motion and Object Tracking", cell), P("<font face='Courier'>cv2.findContours</font> (RETR_EXTERNAL)", cell),
     P("Extracts the outer boundary of every white blob in the mask. Each contour is a candidate moving object.", cell)],
    [P("e. Motion and Object Tracking", cell), P("<font face='Courier'>cv2.contourArea</font>", cell),
     P("Filters out small blobs below MIN_CONTOUR_AREA (3000 pixels) so only meaningful movement is counted.", cell)],
    [P("e. Motion and Object Tracking", cell), P("<font face='Courier'>cv2.boundingRect</font>, <font face='Courier'>cv2.rectangle</font>", cell),
     P("Finds and draws a green bounding box around each moving object, which also provides the per-frame moving object count.", cell)],
    [P("Output / Visualization", cell), P("<font face='Courier'>cv2.putText</font>, <font face='Courier'>cv2.imshow</font>, <font face='Courier'>cv2.imwrite</font>", cell),
     P("Draws the status, object count, and date/time overlays; shows the live feed and the motion mask; saves timestamped screenshots.", cell)],
]
t = Table(rows, colWidths=[1.35 * inch, 1.75 * inch, 3.9 * inch], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6FA")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
]))
story += [t, Spacer(1, 6)]

story.append(P("<b>Processing pipeline.</b> For every frame the program (1) reads and resizes the frame, "
               "(2) converts it to grayscale and blurs it, (3) computes the absolute difference with the "
               "previous grayscale frame, (4) thresholds and dilates the difference to build the motion mask, "
               "(5) finds contours and discards small ones, (6) draws bounding boxes, the status text, the "
               "moving object count, and the date and time, (7) saves a screenshot if motion is present and the "
               "5-second cooldown has passed, and (8) displays the result and the motion mask. The current "
               "grayscale frame then becomes the previous frame for the next iteration. The program exits when "
               "the user presses Q."))

# ---------------- 4. Screenshots ----------------
story.append(P("4. Screenshots of Results", h1))
grid = [[figure(*FIGURES[0]), figure(*FIGURES[1])],
        [figure(*FIGURES[2]), figure(*FIGURES[3])],
        [figure(*FIGURES[4]), ""]]
g = Table(grid, colWidths=[3.5 * inch, 3.5 * inch])
g.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
story.append(g)

# ---------------- 5. Discussion ----------------
story.append(P("5. Testing, Accuracy, Behavior, and Limitations", h1))
story.append(P("<b>Behavior.</b> When the scene is still, the difference image is almost entirely black, the "
               "motion mask is empty, and the display shows the green MONITORING label with a count of 0. When "
               "a person or object moves, the changed pixels form white regions in the mask, a green bounding "
               "box appears around each region larger than the minimum area, the label changes to a red MOTION "
               "DETECTED, and the moving object count updates every frame. A screenshot is saved at most once "
               "every 5 seconds, so a long movement produces a small number of useful captures instead of "
               "hundreds of nearly identical files."))

story.append(P("<b>Testing and tuning.</b> To see how the settings affect detection, three configurations were "
               "run on the same recorded video (272 frames): Test A (Sensitive), Test B (Original, the program's "
               "default), and Test C (Less Sensitive). For each run, the program counted the frames in which "
               "motion was flagged, the approximate motion events, and the bounding boxes drawn."))

def tbl(rows, widths, hl=None):
    out = []
    for i, r in enumerate(rows):
        out.append([P(str(c), cellb if i == 0 else cell) for c in r])
    t = Table(out, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
          ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6FA")]),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    t.setStyle(TableStyle(st))
    return t

res_rows = [
    ["Test", "Min area", "Threshold", "Dilation", "Frames with motion", "Detection rate", "Motion events (approx.)", "Boxes drawn"],
    ["A - Sensitive", "500", "20", "2", "231 / 272", "84.93%", "44", "2106"],
    ["B - Original", "3000", "25", "2", "187 / 272", "68.75%", "50", "418"],
    ["C - Less Sensitive", "5000", "30", "3", "117 / 272", "43.01%", "41", "164"],
]
story += [tbl(res_rows, [1.15*inch, 0.6*inch, 0.85*inch, 0.8*inch, 0.9*inch, 0.75*inch, 1.1*inch, 0.65*inch]),
          P("Table 1. Results of the three settings on the same 272-frame video.", cap)]

obs_rows = [
    ["Observation", "Test A - Sensitive", "Test B - Original", "Test C - Less Sensitive"],
    ["Small movement", "Detected", "Detected", "Not detected"],
    ["Large movement", "Detected", "Detected", "Detected"],
    ["Slow movement", "Detected", "Detected", "Detected"],
    ["False detections", "Few", "Few", "Few"],
    ["Bounding box accuracy", "Good", "Good", "Good"],
]
story += [tbl(obs_rows, [1.6*inch, 1.8*inch, 1.8*inch, 1.8*inch]),
          P("Table 2. Observations from reviewing the output of each test.", cap)]

story.append(P("<b>Accuracy.</b> Lowering the threshold and the minimum contour area made the system more "
               "sensitive: motion was flagged in 84.93% of frames in Test A, 68.75% in Test B, and 43.01% in "
               "Test C. Tests A and B detected small movements, while Test C missed them because its larger "
               "minimum area (5000) and higher threshold (30) filter them out. All three tests detected large "
               "and slow movements, with few false detections and good bounding box placement. The detection "
               "rate is the share of frames where motion was flagged; it measures sensitivity, not correctness "
               "against a ground truth, so a higher rate does not automatically mean a better result. Test A "
               "also drew 2106 boxes over 231 motion frames (about 9 per frame) compared with about 2 per "
               "frame in Test B, which likely means its very small area limit splits one movement into many "
               "small boxes. For this reason, <b>Test B was kept as the program's default</b>: it still "
               "detects small movements while giving cleaner boxes and a more readable object count. "
               "<b>Test A is recommended when detecting small movement is the main priority</b>, provided the "
               "output is checked for false detections. The object count is the number of motion regions, "
               "not an exact count of individual people or objects."))
story.append(P("<b>Limitations.</b>", ParagraphStyle("y", parent=body, spaceAfter=2)))
story += [B("<b>Lighting changes:</b> sudden brightness changes, camera auto-exposure adjustment, or flickering lights can be detected as motion."),
          B("<b>Shadows:</b> moving shadows change pixel brightness and may be detected as motion."),
          B("<b>Stationary or very slow objects:</b> because only two consecutive frames are compared, an object that stops moving, or moves very slowly, produces little difference and disappears from detection."),
          B("<b>Merged or split detections:</b> two nearby moving objects can merge into one blob, and with a very small minimum area one object can split into many boxes, so the count is approximate."),
          B("<b>No identification:</b> the system detects that something moved, but cannot tell whether it is a person, an animal, or a curtain moved by wind."),
          B("<b>Camera movement:</b> if the camera itself shakes or moves, the whole frame changes and everything appears as motion."),
          B("<b>Limited testing:</b> all three tests used a single video. Other lighting conditions, scenes, and movement speeds still need to be tested.")]

# ---------------- 6. Conclusion ----------------
story.append(P("6. Conclusion", h1))
story.append(P("The project successfully combined image operations, image segmentation, and motion tracking "
               "to build a functional motion-triggered security camera using only classical OpenCV techniques. "
               "It processes a live webcam feed (or a recorded video), visualizes its results with bounding "
               "boxes, labels, overlays, and a motion mask, and automatically stores timestamped evidence. "
               "Through this work, the team learned how preprocessing strongly affects detection quality "
               "(blurring removes noise, and thresholding and dilation shape the final mask), how parameter "
               "tuning balances sensitivity against false alarms (the more sensitive Test A flagged motion in 84.93% of frames, compared with 43.01% for the less sensitive Test C), and how simple methods can solve a practical "
               "problem without machine learning."))
story.append(P("<b>Possible improvements:</b> replace frame differencing with background subtraction "
               "(<font face='Courier'>cv2.createBackgroundSubtractorMOG2</font>) to handle slow movement and "
               "lighting changes better; add a region-of-interest zone so only important areas trigger alerts; "
               "add sound, email, or SMS notifications; record short video clips instead of single images; and "
               "combine the system with a Haar cascade or other detector to confirm that the moving object is a person."))

doc = SimpleDocTemplate(OUTPUT, pagesize=reportlab.lib.pagesizes.letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                        topMargin=0.65 * inch, bottomMargin=0.65 * inch,
                        title="Motion-Triggered Security Camera - Documentation", author=", ".join(MEMBERS))
def footer(c, d):
    c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
    c.drawCentredString(reportlab.lib.pagesizes.letter[0] / 2, 0.4 * inch, "%s  |  Page %d" % (COURSE_INFO, d.page))
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Created", OUTPUT)