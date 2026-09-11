"""Show MediaPipe hand landmarks and print a simple velocity intent."""

import time
from pathlib import Path

import cv2
import mediapipe as mp

from gesture_rules import classify_gesture, gesture_to_velocity


MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")
CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
)


def draw_hand(frame, landmarks) -> None:
  height, width = frame.shape[:2]
  points = [
      (int(point.x * width), int(point.y * height)) for point in landmarks
  ]
  for start, end in CONNECTIONS:
    cv2.line(frame, points[start], points[end], (80, 220, 80), 2)
  for point in points:
    cv2.circle(frame, point, 4, (0, 180, 255), -1)


def main() -> None:
  if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Missing {MODEL_PATH}. Run download_hand_model.py first."
    )

  base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH))
  options = mp.tasks.vision.HandLandmarkerOptions(
      base_options=base_options,
      running_mode=mp.tasks.vision.RunningMode.VIDEO,
      num_hands=1,
      min_hand_detection_confidence=0.5,
      min_hand_presence_confidence=0.5,
      min_tracking_confidence=0.5,
  )

  camera = cv2.VideoCapture(0)
  if not camera.isOpened():
    raise RuntimeError("Could not open webcam 0")

  frame_count = 0
  start_time = time.monotonic()
  timestamp_ms = 0

  try:
    with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker:
      while True:
        ok, frame = camera.read()
        if not ok:
          raise RuntimeError("Could not read a webcam frame")

        frame_count += 1
        timestamp_ms += 33
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = landmarker.detect_for_video(image, timestamp_ms)

        label = "NO_HAND"
        if result.hand_landmarks:
          landmarks = result.hand_landmarks[0]
          draw_hand(frame, landmarks)
          label = classify_gesture(landmarks)

        vx, vy, yaw = gesture_to_velocity(label)
        cv2.putText(
            frame,
            f"Gesture: {label}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Intent: vx={vx:+.2f} vy={vy:+.2f} yaw={yaw:+.2f}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        cv2.imshow("Week 3 MediaPipe hand landmarks", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
          break
  finally:
    elapsed = time.monotonic() - start_time
    print(f"Frames: {frame_count}")
    print(f"Average FPS: {frame_count / max(elapsed, 1e-6):.1f}")
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
  main()
