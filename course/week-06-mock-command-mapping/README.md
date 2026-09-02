# Week 6: Gesture-to-command mapping in mock mode

## Milestone

Convert validated gestures into bounded abstract motion commands without moving
the simulator or physical robot.

## Learning objectives

- Map discrete human intent to continuous velocity commands.
- Distinguish requested intent from an approved command.
- Apply command bounds, stop priority, and stale-input behavior.
- Test command logic independently from perception and actuation.

## Prerequisites

- Week 5 classifier produces validated intent or `UNKNOWN`
- Confidence and hold-time behavior documented
- Gesture output is not connected to actuation

## Task 1: Define an abstract command

Use a command with three components:

```text
forward velocity, lateral velocity, yaw rate
```

Create an instructor-approved mapping table. Start with conservative simulation
values, not hardware values:

| Validated intent | Forward | Lateral | Yaw | Reason |
|---|---:|---:|---:|---|
| `STOP` | 0 | 0 | 0 | Stop has priority. |
| `FORWARD` | | 0 | 0 | |
| `BACKWARD` | | 0 | 0 | |
| `LEFT` | 0 | 0 | | |
| `RIGHT` | 0 | 0 | | |
| `UNKNOWN` | 0 | 0 | 0 | Invalid input cannot request motion. |

## Task 2: Separate modules

Keep these responsibilities separate:

```text
gesture source -> validator -> command mapper -> mock command sink
```

The mock sink prints or logs commands. It does not import a robot SDK, publish a
ROS hardware command, or call MuJoCo control code.

## Task 3: Add command bounds

Clamp every mapped command to named maximum magnitudes. Do not scatter unexplained
numbers through the code. Store limits in one configuration location and include
units in comments or documentation.

Test values below, at, and above each limit.

## Task 4: Add stop priority and expiration

Implement these rules:

1. `STOP` immediately produces zero command.
2. `UNKNOWN` and no-hand input produce zero command.
3. A command expires if it is not refreshed before the timeout.
4. A new stop cancels any earlier motion request.
5. Restarting motion requires a new valid motion intent.

Use timestamps rather than counting frames; camera frame rate can vary.

## Task 5: Run a scripted sequence

Test at least this sequence without using the webcam:

```text
FORWARD -> FORWARD -> UNKNOWN -> LEFT -> stale input -> STOP
```

Record input time, validated intent, output command, and reason. The command must
be zero after `UNKNOWN`, stale input, and `STOP`.

## Task 6: Connect perception to mock mode

Connect Week 5 validated intent to the mock mapper. Perform gestures while a team
member watches the command log. Verify that uncertain transitions do not create
brief motion commands.

## Engineering review

Explain:

1. why a classifier should not directly produce a hardware command;
2. why expiration is needed even if the classifier is accurate;
3. why limits belong in one configuration location; and
4. how the team can test the mapper without a webcam.

## Completion checklist

- [ ] Mapping table reviewed by the instructor.
- [ ] Perception, validation, mapping, and output are separate.
- [ ] All command components are bounded.
- [ ] Unknown, no-hand, stale, and stop cases produce zero.
- [ ] Scripted sequence passes.
- [ ] Webcam-to-mock demonstration passes.
- [ ] No simulator or robot actuation is connected.

## Deliverables

- Mapping and limits table
- Command-mapper source and configuration
- Scripted-sequence log
- Answers to the engineering-review questions

## Next week

Continue to [Week 7: Gesture-controlled Go1
simulation](../week-07-gesture-simulation/README.md).
