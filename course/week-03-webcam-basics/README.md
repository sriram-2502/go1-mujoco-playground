# Week 3: Webcam image acquisition

## Milestone

Read live images from a laptop webcam and measure basic camera behavior before
adding gesture recognition.

## Learning objectives

- Explain how a color image is represented as a numerical array.
- Open and release a webcam safely with OpenCV.
- Display frames, report resolution, and estimate frame rate.
- Identify lighting, framing, and background conditions that affect perception.

## Prerequisites

- Weeks 1 and 2 completed
- Laptop webcam available and permitted by Windows privacy settings
- `go1-mujoco-playground` environment active

## Task 1: Prepare a team branch and folder

```powershell
conda activate go1-mujoco-playground
cd C:\path\to\go1-mujoco-playground
git switch creative-inquiry-dev
git pull
git switch -c week-03/TEAM-NAME
New-Item -ItemType Directory -Force .\student_work\webcam
```

Install OpenCV:

```powershell
python -m pip install opencv-python
```

## Task 2: Create a camera check

Create `student_work/webcam/webcam_check.py` in your editor:

```python
import time

import cv2


camera = cv2.VideoCapture(0)
if not camera.isOpened():
  raise RuntimeError("Could not open webcam 0")

frame_count = 0
start_time = time.monotonic()

try:
  while True:
    ok, frame = camera.read()
    if not ok:
      raise RuntimeError("Could not read a webcam frame")

    frame_count += 1
    cv2.imshow("Week 3 webcam check", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
      break
finally:
  elapsed = time.monotonic() - start_time
  height, width = frame.shape[:2]
  print(f"Resolution: {width} x {height}")
  print(f"Average FPS: {frame_count / elapsed:.1f}")
  camera.release()
  cv2.destroyAllWindows()
```

Run it and press `q` to close the window:

```powershell
python .\student_work\webcam\webcam_check.py
```

## Task 3: Test camera conditions

Record resolution, approximate frame rate, and observations for at least four
conditions:

| Condition | Resolution | FPS | What changed? |
|---|---:|---:|---|
| Normal room lighting | | | |
| Dimmer lighting | | | |
| Bright background | | | |
| Hand close to image edge | | | |

Do not record people without their permission. Keep test videos local unless the
instructor explicitly requests an upload.

## Task 4: Explain the data

Use the debugger or add a temporary print to inspect `frame.shape`. Answer:

1. What do its three numbers represent?
2. In what order does OpenCV store the color channels?
3. Why must the program call `camera.release()`?
4. Which tested condition is likely to be hardest for gesture recognition?

## Task 5: Review the work with Git

```powershell
git status
git diff
```

Do not commit captured videos or Conda files. Commit the small Python program and
your instructor-approved notes only.

## Completion checklist

- [ ] Webcam window opens and closes with `q`.
- [ ] Resolution and average frame rate print successfully.
- [ ] Four camera conditions tested.
- [ ] Camera resources release when the program exits.
- [ ] Data questions answered.
- [ ] No private or unnecessarily large video files staged in Git.

## Deliverables

- `webcam_check.py`
- Completed condition table
- Answers to the four data questions
- One paragraph recommending test conditions for later gesture experiments

## Next week

Continue to [Week 4: Hand landmarks and gesture
vocabulary](../week-04-hand-landmarks/README.md).
