# Week 3: Webcam, MediaPipe, and gesture intent

## Milestone

Read live images from a laptop webcam, extract hand landmarks with MediaPipe,
classify simple gestures, and print a high-level velocity intent.

## Learning objectives

- Explain how a color image is represented as a numerical array.
- Open and release a webcam safely with OpenCV.
- Display frames, report resolution, and estimate frame rate.
- Identify lighting, framing, and background conditions that affect perception.
- Explain the difference between hand detection, landmarks, and gesture rules.
- Map a gesture label to velocity intent without commanding MuJoCo yet.

## Prerequisites

- Weeks 1 and 2 completed
- Laptop webcam available and permitted by Windows privacy settings
- `go1-mujoco-playground` environment active

## Task 1: Enter your team branch

```powershell
conda activate go1-mujoco-playground
cd C:\path\to\go1-mujoco-playground
git fetch origin
git switch --track origin/team-alpha
git pull --ff-only
git branch --show-current
```

Team Bravo should use `origin/team-bravo` instead. Do not create another branch.
Weeks 1-4 use the team branch for individual summaries only; code experiments
remain local.

Install OpenCV:

```powershell
python -m pip install opencv-python mediapipe numpy
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

## Task 4: Run the MediaPipe hand-landmark demo

From this folder, download the official Hand Landmarker model once:

```powershell
python .\download_hand_model.py
```

Run the provided webcam-to-landmarks program:

```powershell
python .\hand_landmarks_webcam.py
```

The window should show the camera image, up to 21 hand landmarks, a gesture
label, and a velocity intent. Press `q` to close it. This program uses MediaPipe
for perception and only prints intent; it does not open MuJoCo or connect to a
physical robot.

## Task 5: Explore and modify gesture rules

Open this file:

```text
course/week-03-webcam-basics/gesture_rules.py
```

The starter rules classify `OPEN_PALM`, `POINT`, `FIST`, and `OTHER`. Change one
rule or one gesture-to-intent mapping, rerun the demo, and observe the label and
`vx/vy/yaw` output. Keep `OPEN_PALM`, `FIST`, `OTHER`, and `NO_HAND` mapped to a
zero command. Do not connect the output to MuJoCo yet, and do not commit this
local code experiment.

Record at least ten trials for two gestures under normal lighting, dim lighting,
and a changed hand distance. Note correct labels, incorrect labels, and cases
where no hand was detected.

## Task 6: Explain the data

Use the debugger or add a temporary print to inspect `frame.shape`. Answer:

1. What do its three numbers represent?
2. In what order does OpenCV store the color channels?
3. Why must the program call `camera.release()`?
4. Which tested condition is likely to be hardest for gesture recognition?

## Task 7: Review the work with Git

```powershell
git status
git diff
```

Do not commit captured videos, Conda files, or code changes during Weeks 1-4.
Complete the [Week 3 worksheet](worksheet.md), copy your answers into your
individual summary at `course/student-work/team-alpha/first-last/weekly-summaries/week-03.md`,
and push only that Markdown file. The downloaded `.task` model is ignored by
Git and should not be committed.

Create the folders if they do not already exist:

```powershell
New-Item -ItemType Directory -Force .\course\student-work\team-alpha\first-last\weekly-summaries
```

```powershell
git add .\course\student-work\team-alpha\first-last\weekly-summaries\week-03.md
git diff --cached --stat
git commit -m "Add week 03 summary"
git push -u origin team-alpha
```

Team Bravo should replace `team-alpha` in the path and push command with
`team-bravo`. The instructor-provided Week 3 code remains on the team branch;
students do not upload modified code yet.

## Completion checklist

- [ ] Webcam window opens and closes with `q`.
- [ ] Resolution and average frame rate print successfully.
- [ ] Four camera conditions tested.
- [ ] MediaPipe model downloaded and hand landmarks displayed.
- [ ] Two or more gesture labels tested.
- [ ] One gesture rule or intent mapping changed and tested.
- [ ] Gesture trial data table completed.
- [ ] Camera resources release when the program exits.
- [ ] Data questions answered.
- [ ] No private or unnecessarily large video files staged in Git.

## Deliverables

- `webcam_check.py`
- `download_hand_model.py`
- `hand_landmarks_webcam.py`
- `gesture_rules.py`
- Completed condition table
- Gesture trial data table
- Answers to the four data questions
- One paragraph recommending test conditions for later gesture experiments

## Next week

Continue to [Week 4: Gesture recognition and temporal
filtering](../week-04-hand-landmarks/README.md).
