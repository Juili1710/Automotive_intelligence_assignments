import cv2
import random
import time
import sys
# ---------------------------------
# USER SETTINGS
# ---------------------------------
INPUT_VIDEO  = "flowerbloom.mp4"
OUTPUT_VIDEO = "output_assignment0.mp4"

BOTTOM_TEXT = "python assignment, version 0"
RANDOM_TEXT = "AI"

FONT = cv2.FONT_HERSHEY_SIMPLEX

# ---------------------------------
# OPEN INPUT VIDEO
# ---------------------------------
cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    print("ERROR: Cannot open input video")
    sys.exit()

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

# ---------------------------------
# VIDEO WRITER (SAVE OUTPUT)
# ---------------------------------
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

# ---------------------------------
# DISPLAY WINDOW (RESIZABLE)
# ---------------------------------
cv2.namedWindow("Python Assignment 0", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Python Assignment 0", width, height)

# ---------------------------------
# SCROLLING RIBBON SETUP
# ---------------------------------
(ribbon_w, ribbon_h), _ = cv2.getTextSize(BOTTOM_TEXT, FONT, 0.7, 2)
ribbon_x = width   # start from right edge
ribbon_y = height - 15
scroll_speed = 4   # pixels per frame

# ---------------------------------
# FRAME COUNTER & TIME
# ---------------------------------
frame_count = 0
start_time = time.time()

# ---------------------------------
# PROCESS VIDEO
# ---------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    elapsed_time = time.time() - start_time

    # -----------------------------
    # RANDOM TEXT POSITION (SAFE)
    # -----------------------------
    (tw, th), _ = cv2.getTextSize(RANDOM_TEXT, FONT, 1, 2)
    x = random.randint(0, max(1, width - tw))
    y = random.randint(th + 10, height - ribbon_h - 20)

    cv2.putText(frame, RANDOM_TEXT,
                (x, y),
                FONT,
                1,
                (0, 255, 0),
                2)

    # -----------------------------
    # SCROLLING RIBBON
    # -----------------------------
    cv2.putText(frame, BOTTOM_TEXT,
                (ribbon_x, ribbon_y),
                FONT,
                0.7,
                (255, 255, 255),
                2)

    ribbon_x -= scroll_speed
    if ribbon_x < -ribbon_w:
        ribbon_x = width

    # -----------------------------
    # FRAME COUNT + TIMESTAMP
    # -----------------------------
    overlay_text = f"Frame: {frame_count} | Time: {elapsed_time:.2f}s"

    cv2.putText(frame, overlay_text,
                (10, 30),
                FONT,
                0.7,
                (0, 255, 255),
                2)

    # -----------------------------
    # SHOW + SAVE FRAME
    # -----------------------------
    cv2.imshow("Python Assignment 0", frame)
    out.write(frame)

    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
        break

# ---------------------------------
# CLEANUP
# ---------------------------------
cap.release()
out.release()
cv2.destroyAllWindows()

print("Output saved as:", OUTPUT_VIDEO)
