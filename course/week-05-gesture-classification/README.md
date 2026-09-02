# Week 5: Gesture classification and validation

## Milestone

Classify the approved gesture vocabulary and prevent weak or unstable
predictions from becoming commands.

## Learning objectives

- Explain labels, confidence, thresholds, and temporal consistency.
- Build a labeled test set that includes different people and conditions.
- Calculate per-gesture accuracy and identify common confusion pairs.
- Convert raw predictions into validated intent or `UNKNOWN`.

## Prerequisites

- Week 4 gesture vocabulary approved by the instructor
- Landmark pipeline works with multiple team members
- No perception output is connected to robot motion

## Task 1: Define the interface

Every prediction record should contain at least:

```text
timestamp, predicted_label, confidence, hand_detected
```

Validated intent must be one of:

```text
STOP, FORWARD, BACKWARD, LEFT, RIGHT, UNKNOWN
```

Document how `no hand`, `unknown gesture`, and low confidence are represented.

## Task 2: Create a test plan

Collect instructor-approved test samples for every gesture and for `UNKNOWN`.
Include:

- every consenting team member;
- at least two lighting conditions;
- at least two hand distances or orientations; and
- transitions between gestures.

Keep training and evaluation samples separate if the classifier is trained on
student-collected data.

## Task 3: Measure raw predictions

Run the classifier without command output. Save expected label, predicted label,
confidence, and timestamp to CSV. Complete a confusion table:

| Expected | STOP | FORWARD | BACKWARD | LEFT | RIGHT | UNKNOWN |
|---|---:|---:|---:|---:|---:|---:|
| STOP | | | | | | |
| FORWARD | | | | | | |
| BACKWARD | | | | | | |
| LEFT | | | | | | |
| RIGHT | | | | | | |
| UNKNOWN | | | | | | |

Report overall accuracy and per-gesture accuracy. Do not hide failed samples.

## Task 4: Add confidence validation

Begin with the companion project's conservative development threshold:

```text
minimum confidence = 0.80
```

Predictions below the threshold become `UNKNOWN`. Recalculate accepted accuracy
and report what fraction of samples is rejected. Explain the tradeoff between
rejecting too much and accepting incorrect commands.

## Task 5: Add temporal validation

Require a gesture to remain consistent for an initial hold time of 0.30 seconds
before it becomes valid. Reset the hold timer when the label changes, the hand
disappears, or confidence falls below the threshold.

Measure:

- false transitions before and after validation;
- time from gesture presentation to validated intent; and
- behavior when the operator rapidly changes gestures.

## Task 6: Review safety semantics

At this stage, validated intent is still printed or logged only. It must not
publish a velocity or Go1 command. Decide with the instructor whether a confident
`STOP` should be accepted faster than motion gestures.

## Completion checklist

- [ ] Prediction record format documented.
- [ ] Test set covers gestures, unknown cases, people, and conditions.
- [ ] Confusion table and per-class accuracy completed.
- [ ] Confidence threshold implemented and evaluated.
- [ ] Temporal consistency implemented and evaluated.
- [ ] Output remains in non-actuating mock mode.

## Deliverables

- Test protocol and sample counts
- Confusion table and accuracy results
- Threshold/rejection analysis
- Short plot or table of validation delay
- Recommendation for Week 6 parameters

## Next week

Continue to [Week 6: Gesture-to-command
mapping](../week-06-mock-command-mapping/README.md).
