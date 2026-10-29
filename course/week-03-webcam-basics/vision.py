"""Week 3 reusable webcam worker. No robot commands or GUI calls here."""

import threading
import time
from pathlib import Path

from course import gestures, safety

MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")
CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15),
    (15, 16), (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
)


class Webcam(threading.Thread):
  def __init__(self, camera=0):
    super().__init__(daemon=True, name="webcam-mediapipe")
    self.camera = camera
    self.quit = threading.Event()
    self.lock = threading.Lock()
    self.frame = None
    self.prediction = safety.Prediction()
    self.error = "Starting webcam and MediaPipe..."
    self.fps = 0.0

  def snapshot(self):
    with self.lock:
      return self.frame, self.prediction, self.error, self.fps

  def run(self):
    camera = None
    try:
      import cv2
      import mediapipe as mp

      if not MODEL_PATH.exists():
        raise FileNotFoundError("Run course/week-03-webcam-basics/download_hand_model.py first")
      options = mp.tasks.vision.HandLandmarkerOptions(
          base_options=mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH)),
          running_mode=mp.tasks.vision.RunningMode.VIDEO,
          num_hands=2,  # Multiple hands are ambiguous and stop the robot.
          min_hand_detection_confidence=0.6,
          min_hand_presence_confidence=0.6,
          min_tracking_confidence=0.6,
      )
      camera = cv2.VideoCapture(self.camera)
      if not camera.isOpened():
        raise RuntimeError(f"Cannot open webcam {self.camera}; check camera permissions")
      camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
      camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
      camera.set(cv2.CAP_PROP_FPS, 30)  # Best effort; also pace processing below.
      camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Best effort; backend may ignore it.
      previous = time.monotonic()
      timestamp_ms = -1
      with mp.tasks.vision.HandLandmarker.create_from_options(options) as detector:
        while not self.quit.is_set():
          ok, frame = camera.read()
          acquired = time.monotonic()
          if not ok:
            raise RuntimeError("Webcam frame acquisition failed")
          frame = cv2.flip(frame, 1)
          rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          timestamp_ms = max(timestamp_ms + 1, int(acquired * 1000))
          result = detector.detect_for_video(
              mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb), timestamp_ms)
          label = "NO_HAND"
          if len(result.hand_landmarks) == 1:
            landmarks = result.hand_landmarks[0]
            label = gestures.classify(landmarks)
            height, width = rgb.shape[:2]
            points = [(int(p.x * width), int(p.y * height)) for p in landmarks]
            for a, b in CONNECTIONS:
              cv2.line(rgb, points[a], points[b], (64, 222, 190), 2)
            for point in points:
              cv2.circle(rgb, point, 4, (255, 205, 95), -1)
          elif len(result.hand_landmarks) > 1:
            label = "UNKNOWN"
          with self.lock:
            self.frame = rgb
            self.prediction = safety.Prediction(label, acquired)
            self.error = ""
            self.fps = 1.0 / max(acquired - previous, 0.001)
          previous = acquired
          # Some drivers return >60 fps; perception needs only 30 fresh frames/s.
          # Throttle without accumulating camera frames or hogging the CPU.
          self.quit.wait(max(0, acquired + 1 / 30 - time.monotonic()))
    except Exception as exc:
      with self.lock:
        self.error = str(exc)
        self.prediction = safety.Prediction("NO_HAND", time.monotonic())
    finally:
      if camera is not None:
        camera.release()
