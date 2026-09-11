"""Beginner-friendly gesture rules for the Week 3 webcam activity."""

from collections.abc import Sequence


def _finger_is_extended(landmarks: Sequence[object], tip: int, pip: int) -> bool:
  return landmarks[tip].y < landmarks[pip].y


def classify_gesture(landmarks: Sequence[object]) -> str:
  """Return a simple label from 21 normalized MediaPipe hand landmarks."""
  index_up = _finger_is_extended(landmarks, 8, 6)
  middle_up = _finger_is_extended(landmarks, 12, 10)
  ring_up = _finger_is_extended(landmarks, 16, 14)
  pinky_up = _finger_is_extended(landmarks, 20, 18)

  if index_up and middle_up and ring_up and pinky_up:
    return "OPEN_PALM"
  if index_up and not middle_up and not ring_up and not pinky_up:
    return "POINT"
  if not index_up and not middle_up and not ring_up and not pinky_up:
    return "FIST"
  return "OTHER"


def gesture_to_velocity(label: str) -> tuple[float, float, float]:
  """Map a label to (forward, lateral, yaw) intent for display only."""
  commands = {
      "OPEN_PALM": (0.0, 0.0, 0.0),
      "FIST": (0.0, 0.0, 0.0),
      "POINT": (0.25, 0.0, 0.0),
      "OTHER": (0.0, 0.0, 0.0),
      "NO_HAND": (0.0, 0.0, 0.0),
  }
  return commands.get(label, (0.0, 0.0, 0.0))
