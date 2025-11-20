import cv2
import mediapipe as mp
import numpy as np

mp_face = mp.solutions.face_mesh

# Try opening webcam safely
def get_camera():
    for i in range(3):   # try 0,1,2
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            return cap
    print("Error: No webcam found!")
    exit()

cap = get_camera()

# FaceMesh Model
with mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Warning: Failed to read frame. Trying again...")
            continue

        # Now safe because frame is valid
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            face = results.multi_face_landmarks[0]

            left_ids = [105, 65, 52]
            right_ids = [334, 296, 285]

            # Center calculation
            def center(ids):
                xs, ys = [], []
                for idx in ids:
                    lm = face.landmark[idx]
                    xs.append(int(lm.x * w))
                    ys.append(int(lm.y * h))
                return int(np.mean(xs)), int(np.mean(ys))

            lx, ly = center(left_ids)
            rx, ry = center(right_ids)

            # Final Bindi position
            cx = (lx + rx) // 2
            cy = (ly + ry) // 2 - 20

            # Draw bindi only
            cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)

        cv2.imshow("Eyebrow Center (Bindi)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()