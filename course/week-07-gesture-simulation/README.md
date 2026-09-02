# Week 7: Gesture-controlled Go1 simulation

## Milestone

Use validated hand gestures instead of keyboard input to command the Go1 in
MuJoCo.

## Learning objectives

- Integrate perception and control through a small, documented interface.
- Preserve the existing ONNX locomotion policy while changing command input.
- Manage camera and simulator timing without freezing either interface.
- Demonstrate stop and reset behavior in simulation.

## Prerequisites

- Keyboard simulation passes Week 1
- Gesture validation passes Week 5
- Mock command mapping passes Week 6
- Instructor approves the mapping and initial simulated limits

## Task 1: Draw the integration

Update the system diagram with actual team module and file names:

```text
webcam -> classifier -> validator -> mapper -> command[3]
                                               |
                                               v
robot state -> ONNX locomotion policy -> 12 joint actions -> MuJoCo
```

The gesture system supplies only the three high-level command values. It does
not replace the 48-input, 12-output ONNX locomotion policy.

## Task 2: Preserve a baseline

Run the keyboard controller and save a short baseline recording. Do not remove
the known-working keyboard program. Create a separate gesture-simulation entry
point or an input-source abstraction, following instructor guidance.

## Task 3: Connect a mock gesture source first

Before opening the webcam, connect a scripted intent sequence to the simulator:

```text
STOP -> FORWARD -> STOP -> LEFT -> STOP
```

Verify sign conventions, command limits, and stopping. Correct mapping errors in
simulation, never on physical hardware.

## Task 4: Connect live validated intent

Connect the Week 5 validator output to the same command interface. Ensure that:

- camera processing does not block MuJoCo stepping;
- MuJoCo closure releases the camera;
- camera failure sends stop;
- the last motion command cannot persist indefinitely; and
- printed diagnostics show current gesture, confidence, and approved command.

## Task 5: Demonstrate the vocabulary

From a zero command, demonstrate each approved gesture and return to stop between
motions. A second team member records observed motion and any mismatch.

| Gesture | Expected motion | Observed motion | Pass? |
|---|---|---|:--:|
| STOP | zero command | | |
| FORWARD | forward | | |
| BACKWARD | backward | | |
| LEFT | turn left | | |
| RIGHT | turn right | | |

## Task 6: Test failure cases

In simulation, test:

1. hand leaves the image;
2. confidence drops below threshold;
3. gesture changes during hold time;
4. webcam is intentionally closed; and
5. command source stops updating.

All five cases must produce or preserve a zero command within the documented
timeout.

## Completion checklist

- [ ] Integration diagram uses actual module names.
- [ ] Original keyboard baseline remains available.
- [ ] Scripted gesture source works before webcam integration.
- [ ] Five gestures produce expected simulated behavior.
- [ ] Five failure cases stop safely.
- [ ] Camera and viewer close cleanly.
- [ ] No physical robot interface is enabled.

## Deliverables

- Architecture diagram
- Gesture-controlled simulation code
- Gesture-motion results table
- Failure-case log
- Short demonstration video

## Next week

Continue to [Week 8: Safety behavior and automated
tests](../week-08-safety-testing/README.md).
