\# Week 3 Worksheet: Webcam, MediaPipe, and Gesture Intent



Name: Camden Norris

Team: `team-alpha`

Team branch: `team-alpha`



\## 1. Camera Conditions



| Condition                | Resolution |  FPS | What changed?                                            |

| ------------------------ | ---------- | ---: | -------------------------------------------------------- |

| Normal room lighting     | 640 x 480  | 23.2 | Clear image under normal lighting                        |

| Dimmer lighting          | 640 x 480  | 24.2 | Image was darker with less visible detail                |

| Bright background        | 640 x 480  | 26.2 | Subject appeared darker because of the bright background |

| Hand close to image edge | 640 x 480  | 25.4 | Hand became partially cut off near the edge              |



\## 2. MediaPipe Observations



Number of landmarks displayed: 21



Normalized `x` represents the horizontal position of a landmark relative to the image width, typically from 0 to 1.



Normalized `y` represents the vertical position of a landmark relative to the image height, typically from 0 to 1.



The program converts BGR to RGB because OpenCV reads images in BGR format while MediaPipe expects RGB input.



\## 3. Gesture Trial Data



\### POINT



| Trial | Intended Gesture | Predicted Label | Correct? | Hand Condition | Printed vx/vy/yaw  |

| ----- | ---------------- | --------------- | -------- | -------------- | ------------------ |

| 1     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 2     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 3     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 4     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 5     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 6     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 7     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 8     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 9     | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |

| 10    | POINT            | POINT           | Yes      | Normal         | 0.25 / 0.00 / 0.00 |



POINT accuracy: 10 / 10



\### OPEN\_PALM



| Trial | Intended Gesture | Predicted Label | Correct? | Hand Condition | Printed vx/vy/yaw  |

| ----- | ---------------- | --------------- | -------- | -------------- | ------------------ |

| 1     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 2     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 3     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 4     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 5     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 6     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 7     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 8     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 9     | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |

| 10    | OPEN\_PALM        | OPEN\_PALM       | Yes      | Normal         | 0.00 / 0.00 / 0.00 |



OPEN\_PALM accuracy: 10 / 10



\## 4. Code Change



File changed:



`course/week-03-webcam-basics/gesture\_rules.py`



What rule or mapping did you change?



I changed the POINT forward velocity command from vx = 0.25 to vx = 0.50.



What changed in the output?



After the change, the point gesture produced vx = 0.50 instead of vx = 0.25.



\## 5. Safety and Next Step



Why should `NO\_HAND`, `OTHER`, and uncertain input produce a zero command?



They should produce a zero command so that a missing gesture does not accidentally cause the robot to move.



What additional filtering is needed before connecting gesture intent to MuJoCo?



The system should require a gesture to remain consistently detected for several consecutive frames before accepting it as a command. A timeout should also return the command to zero if valid hand input disappears.



\## Evidence



Screenshot:



Video: Camera Testing


Commit:


f79c869



