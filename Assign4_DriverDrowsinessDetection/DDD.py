import cv2
import mediapipe as mp
import numpy as np
import os

# ===================== USER SETTINGS =====================
drowsy_folder = r"C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\DDD Database\Driver Drowsiness Dataset (DDD)\Drowsy"
non_drowsy_folder = r"C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\DDD Database\Driver Drowsiness Dataset (DDD)\Non Drowsy"

output_video_path = r"C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\output_video.avi"

FPS = 10
VIDEO_DURATION_SEC = 120  # 2 minutes

DEBUG_SHOW_FRAMES = True   # set False if too many popups
DEBUG_PRINT = True

# ===================== MEDIAPIPE =====================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]

# ===================== FUNCTIONS =====================
def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def compute_EAR(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def compute_MAR(mouth):
    A = euclidean(mouth[0], mouth[1])
    B = euclidean(mouth[2], mouth[3])
    return A / B

def get_head_pose(landmarks):
    nose_x = landmarks[1].x
    if nose_x < 0.4:
        return "Left"
    elif nose_x > 0.6:
        return "Right"
    else:
        return "Forward"

# ===================== LOAD IMAGES =====================
def load_images():
    image_paths = []

    for f in os.listdir(drowsy_folder):
        image_paths.append(os.path.join(drowsy_folder, f))

    for f in os.listdir(non_drowsy_folder):
        image_paths.append(os.path.join(non_drowsy_folder, f))

    image_paths = sorted(image_paths)

    if DEBUG_PRINT:
        print(f"Total images loaded: {len(image_paths)}")

    return image_paths

# ===================== MAIN =====================
def run():
    image_paths = load_images()

    # ---- check first valid image ----
    first_frame = None
    for path in image_paths:
        img = cv2.imread(path)
        if img is not None:
            first_frame = img
            break

    if first_frame is None:
        print("❌ No valid images found")
        return

    h, w, _ = first_frame.shape

    out = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*'XVID'),
        FPS,
        (w, h)
    )

    total_frames_needed = FPS * VIDEO_DURATION_SEC
    img_index = 0

    print("🎥 Generating video...")

    for frame_count in range(total_frames_needed):

        img_path = image_paths[img_index % len(image_paths)]
        frame = cv2.imread(img_path)

        if frame is None:
            if DEBUG_PRINT:
                print(f"Skipping: {img_path}")
            continue

        frame = cv2.resize(frame, (w, h))

        # ---- PROCESS ----
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        status = "Non-Drowsy"
        ear_val, mar_val = 0, 0
        head_pose = "Unknown"

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                pts = [(int(l.x * w), int(l.y * h)) for l in face_landmarks.landmark]

                left_eye = [pts[i] for i in LEFT_EYE]
                right_eye = [pts[i] for i in RIGHT_EYE]
                mouth = [pts[i] for i in MOUTH]

                ear_val = (compute_EAR(left_eye) + compute_EAR(right_eye)) / 2.0
                mar_val = compute_MAR(mouth)
                head_pose = get_head_pose(face_landmarks.landmark)

                # ---- DECISION ----
                if ear_val < 0.22 or mar_val > 0.6:
                    status = "DROWSY"
                else:
                    status = "Non-Drowsy"

        # ---- OVERLAY ----
        cv2.putText(frame, f"EAR: {ear_val:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, f"MAR: {mar_val:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

        cv2.putText(frame, f"Head: {head_pose}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.putText(frame, f"Status: {status}", (10, h-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0,0,255) if status=="DROWSY" else (0,255,0), 2)

        # ---- DEBUG VIEW ----
        if DEBUG_SHOW_FRAMES:
            cv2.imshow("Processing", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        out.write(frame)

        img_index += 1

    out.release()
    cv2.destroyAllWindows()

    print("✅ Output video saved at:", output_video_path)

# ===================== RUN =====================
if __name__ == "__main__":
    run()