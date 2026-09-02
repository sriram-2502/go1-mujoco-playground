# Week 9: Integrated system evaluation

## Milestone

Evaluate the complete gesture-to-simulation system with repeatable engineering
metrics rather than relying on a successful demonstration alone.

## Learning objectives

- Define measurable system-level requirements.
- Measure end-to-end latency, command accuracy, rejection, and stop behavior.
- Compare performance across users and environmental conditions.
- Use results to justify one focused design improvement.

## Prerequisites

- Gesture-controlled simulation passes Week 7
- Safety test suite passes Week 8
- Logging includes timestamps, raw prediction, validated intent, command, and reason

## Task 1: Freeze a test version

Record the Git commit, environment package list, configuration values, camera,
and laptop used for testing:

```powershell
git rev-parse HEAD
python -m pip freeze > environment-week-09.txt
```

Do not change code during a test run. If code changes, assign a new test version.

## Task 2: Define metrics

At minimum measure:

- per-gesture accepted accuracy;
- false-motion command count;
- rejection rate;
- gesture-to-command latency;
- stop latency;
- stale-input stop latency; and
- simulator update or command rate.

Define exactly how each metric is calculated before collecting data.

## Task 3: Create a test matrix

Include multiple consenting operators and relevant conditions:

| Factor | Example levels |
|---|---|
| Operator | Team members |
| Lighting | normal, dim, bright background |
| Distance | near, nominal, far |
| Gesture | five approved gestures plus unknown |
| Transition | stop-to-motion, motion-to-stop, motion-to-motion |

Use enough repeated trials to reveal variability. Record unsuccessful trials.

## Task 4: Run and analyze tests

Use one person to operate and another to record protocol compliance. Save raw
data before calculating summaries. Plot at least:

1. accuracy or rejection by gesture;
2. latency distribution; and
3. failure count by condition.

Report median and worst-case stop latency, not only an average.

## Task 5: Make one evidence-based improvement

Choose the largest important weakness supported by the data. Change one factor,
such as gesture definition, confidence threshold, hold time, or user feedback.
Repeat the relevant subset of tests and compare before/after results.

Do not improve apparent accuracy by silently removing hard cases.

## Task 6: Hardware-readiness recommendation

Conclude one of:

- ready to begin non-actuating ROS integration;
- ready with listed restrictions; or
- not ready, with corrective work identified.

This is a team recommendation, not permission to operate the robot.

## Completion checklist

- [ ] Test version and environment recorded.
- [ ] Metrics defined before data collection.
- [ ] Test matrix covers operators, conditions, gestures, and transitions.
- [ ] Raw data and summary plots saved.
- [ ] Worst-case stop behavior reported.
- [ ] One change evaluated with before/after evidence.
- [ ] Hardware-readiness recommendation justified.

## Deliverables

- Reproducible test protocol
- Raw data and analysis plots
- Before/after comparison
- Hardware-readiness recommendation

## Next week

Continue to [Week 10: ROS and hardware
readiness](../week-10-ros-hardware-readiness/README.md).
