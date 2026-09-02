# Week 4: Hand landmarks and gesture vocabulary

## Milestone

Detect a hand in webcam images, visualize its landmarks, and define a small
gesture vocabulary suitable for robot commands.

## Learning objectives

- Distinguish detection, landmark estimation, and classification.
- Visualize hand landmarks and observe detection confidence.
- Define gestures that are distinct, repeatable, and safe to use.
- Document ambiguous cases before building command logic.

## Prerequisites

- Week 3 webcam program works reliably
- Team can explain image shape, frame rate, and camera cleanup
- Companion project available:
  [`DyCo-AI/go1_gesture_tracking`](https://github.com/DyCo-AI/go1_gesture_tracking)

## Task 1: Review the system boundary

Sketch this pipeline in your engineering notes:

```text
image -> hand detection -> landmarks -> gesture label -> validated intent
```

For each arrow, write what data moves to the next block. At this stage, no label
is allowed to command a simulated or physical robot.

## Task 2: Set up the gesture workspace

Follow the current setup instructions in the companion gesture repository. Keep
gesture-perception work separate from the Go1 simulator until Week 7.

Before running code, verify:

- the webcam index is correct;
- a frame can be displayed;
- the program has a documented quit key; and
- the camera is released even if an error occurs.

## Task 3: Display hand landmarks

Run or complete the instructor-provided landmark starter. Confirm that it:

1. reads a live frame;
2. converts the color format expected by the landmark model;
3. draws detected landmarks and connections;
4. shows whether a hand is currently detected; and
5. exits cleanly.

Capture examples of an open hand, closed hand, pointing hand, and no-hand frame.

## Task 4: Propose a gesture vocabulary

Start with five abstract intents:

| Intent | Candidate gesture | Why it is distinguishable | Possible confusion |
|---|---|---|---|
| `STOP` | | | |
| `FORWARD` | | | |
| `BACKWARD` | | | |
| `LEFT` | | | |
| `RIGHT` | | | |

`STOP` must be easy to perform and recognize. It must not resemble a motion
gesture. Instructor approval is required before labels are finalized.

## Task 5: Test variation

Each team member performs every candidate gesture under at least three
conditions: normal, rotated hand, and different camera distance. Record whether
the hand and landmarks remain detectable.

Do not tune the vocabulary only for one person. Note accessibility concerns or
gestures that are uncomfortable to hold.

## Engineering questions

1. Why are landmarks more useful than raw pixels for a simple gesture model?
2. What is the difference between “no hand” and “unknown gesture”?
3. Why should `STOP` not depend on a subtle finger position?
4. Which gesture pair is most likely to be confused, and why?

## Completion checklist

- [ ] Pipeline sketch completed.
- [ ] Landmarks shown for multiple hands and poses.
- [ ] No-hand behavior observed.
- [ ] Five-gesture proposal documented.
- [ ] Variation tested across team members and conditions.
- [ ] No robot-motion output is connected.

## Deliverables

- Four annotated example images
- Proposed gesture table
- Variation-test notes
- Answers to the engineering questions

## Next week

Continue to [Week 5: Gesture classification and
validation](../week-05-gesture-classification/README.md).
