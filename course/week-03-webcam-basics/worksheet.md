# Week 3 worksheet: Webcam, MediaPipe, and gesture intent

Name:  
Team: `team-alpha` / `team-bravo`  
Personal branch:  

## 1. Camera conditions

| Condition | Resolution | FPS | What changed? |
|---|---:|---:|---|
| Normal room lighting | | | |
| Dimmer lighting | | | |
| Bright background | | | |
| Hand close to image edge | | | |

## 2. MediaPipe observations

- Number of landmarks displayed: 
- What does one landmark's normalized `x` value represent? 
- What does one landmark's normalized `y` value represent? 
- Why does the program convert BGR to RGB? 

## 3. Gesture trial data

Record at least ten trials for each of two gestures.

| Trial | Intended gesture | Predicted label | Correct? | Hand condition | Printed vx/vy/yaw |
|---:|---|---|:---:|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |

Gesture 1 accuracy: ____ / 10  
Gesture 2 accuracy: ____ / 10  

## 4. Code change

File changed:

```text
course/week-03-webcam-basics/gesture_rules.py
```

What rule or mapping did you change?  

What changed in the output?  

## 5. Safety and next step

Why should `NO_HAND`, `OTHER`, and uncertain input produce a zero command?  

What additional filtering is needed before connecting gesture intent to MuJoCo?  

## Evidence

- Screenshot: 
- Commit: 
