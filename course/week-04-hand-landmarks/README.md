# Week 4: Gesture Vocabulary and Recognition

## Compare vocabularies before switching robots

Use the simulation gesture table below for this exercise. The Go2 dashboard
has a different mapping: pointing up requests forward, pointing left with one
or two fingers selects sideways motion, and thumb up/down selects rotation.
Compare the two tables in your notes and identify one confusing transition to
test. Do not replace the simulation classifier with the hardware rules.

See [Go2 hardware onboarding](../GO2_HARDWARE.md) for the later hardware path.

## Milestone

Recognize STOP, FORWARD, LEFT and RIGHT from the Week 3 hand landmarks. Evaluate the rules before connecting motion in the Week 6 integration lab.

## Reference code

`gestures.py` provides `classify(landmarks) -> label`. It compares finger-tip distances from the wrist with middle-joint distances. It ignores the thumb and is more tolerant of image rotation than the Week 3 vertical-coordinate rules. These rules are still a baseline and can fail under occlusion or unusual hand orientation.

| Pose | Label |
|---|---|
| Open palm or fist | STOP |
| Index extended | FORWARD |
| Index and middle extended | LEFT |
| Index, middle and ring extended | RIGHT |
| Other pose | UNKNOWN |

No hand and multiple hands are handled by `vision.py`; neither requests motion. Backward and slow mode are optional later extensions.

## Activities

1. Trace image -> landmarks -> raw label -> validated command.
2. Inspect `gestures.classify()` and explain the distance threshold.
3. Run the dashboard with motion disabled: `python run_gesture_navigation.py`.
4. Record labels for every team member at two distances, two lighting conditions and rotated hand poses.
5. Identify confusion pairs, transitions and comfortable stop gestures.
6. Propose one rule improvement and evaluate it on examples not used for tuning.

The classifier has no calibrated confidence output. Do not use MediaPipe hand tracking thresholds as gesture-classification confidence.

## Verification

```powershell
python -m unittest discover -s course/week-04-hand-landmarks -v
```

Synthetic geometry checks verify the reference mapping and rotation/scale behavior; they do not establish real-world recognition accuracy.

## Deliverables

Gesture table, annotated examples, confusion counts across operators/conditions and a proposed improvement. Keep motion disabled during perception evaluation.

Next: [Week 5 validation and command supervision](../week-05-gesture-classification/README.md).

## Weekly submission

Submit your individual `week-04/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
