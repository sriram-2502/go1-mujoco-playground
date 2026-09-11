"""Download the MediaPipe Hand Landmarker model used by Week 3."""

from pathlib import Path
from urllib.request import urlopen


MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")


def main() -> None:
  if MODEL_PATH.exists():
    print(f"Model already exists: {MODEL_PATH}")
    return

  print("Downloading the MediaPipe Hand Landmarker model...")
  with urlopen(MODEL_URL, timeout=60) as response:
    MODEL_PATH.write_bytes(response.read())
  print(f"Saved: {MODEL_PATH}")


if __name__ == "__main__":
  main()
