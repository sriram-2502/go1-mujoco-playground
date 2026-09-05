# Creative Inquiry: Gesture Control for a Unitree Go1

This repository is the simulation and course workspace for a Clemson Mechanical
Engineering Creative Inquiry project. Students will learn how a quadruped robot
is commanded, develop a camera-based hand-gesture interface, and test their
ideas in simulation before any supervised work with the physical Unitree Go1.

**No previous Python, AI, or robotics experience is required.** The weekly tasks
introduce the command line, Conda, Python, Git, computer vision, robot commands,
testing, and system integration one step at a time.

Our companion project is
[`DyCo-AI/go1_gesture_tracking`](https://github.com/DyCo-AI/go1_gesture_tracking).
It contains the webcam gesture-recognition and ROS interfaces used in the later
weeks of this course.

> [!IMPORTANT]
> Simulation is the first safety gate. Students must not connect software to or
> command the physical robot without instructor approval and supervision.

## Course challenge

Build and evaluate an interface that lets a human use simple hand gestures to
request bounded Go1 motions such as forward, backward, left, right, and stop.
The system must reject uncertain input, limit motion commands, prioritize stop,
and stop automatically when input or communication becomes stale.

```text
operator webcam
      |
      v
gesture model -> confidence and timing checks -> bounded motion intent
                                                   |
                              +--------------------+--------------------+
                              |                                         |
                              v                                         v
                     MuJoCo simulation                         supervised Go1 test
                     (required first)                         (instructor approval)
```

## Course outcomes

By the end of the project, students should be able to:

1. Explain how sensing, computation, inference, control, and actuation interact
   in a robotic system.
2. Use Conda, Python, Git, and GitHub in a collaborative engineering workflow.
3. Read and make small, testable changes to a Python robotics program.
4. Explain body-frame forward velocity, lateral velocity, and yaw rate.
5. Use a webcam and an AI model to detect and classify hand gestures.
6. Convert recognized gestures into bounded, interruptible robot commands.
7. Design fail-safe behavior for uncertain perception and lost communication.
8. Plan repeatable tests and measure accuracy, latency, and failure behavior.
9. Integrate simulation, perception, command logic, ROS, and robot hardware.
10. Communicate engineering decisions, results, limitations, and next steps.

## Weekly roadmap

Each linked folder contains the week's learning objectives, preparation, tasks,
deliverables, and completion checklist. Complete the weeks in order.

| Week | Milestone | Student outcome |
|:--:|---|---|
| 1 | [GitHub onboarding and Go1 baseline](course/week-01-github-onboarding/README.md) | Access the repository, enter the assigned team branch, run the existing baseline, and document the work. |
| 2 | [Go1 controller behavior, control, and reinforcement learning](course/week-02-go1-controller/README.md) | Trace keyboard input, measure command sensitivity, and make one approved change. |
| 3 | [Webcam image acquisition](course/week-03-webcam-basics/README.md) | Capture, display, and describe images from a laptop webcam. |
| 4 | [Hand landmarks and gesture vocabulary](course/week-04-hand-landmarks/README.md) | Detect a hand, visualize landmarks, and define useful gestures. |
| 5 | [Gesture classification and validation](course/week-05-gesture-classification/README.md) | Measure gesture predictions and reject uncertain or unstable classifications. |
| 6 | [Gesture-to-command mapping](course/week-06-mock-command-mapping/README.md) | Convert validated gestures into bounded abstract commands without moving a robot. |
| 7 | [Gesture-controlled Go1 simulation](course/week-07-gesture-simulation/README.md) | Replace keyboard intent with gesture intent in MuJoCo. |
| 8 | [Safety behavior and automated tests](course/week-08-safety-testing/README.md) | Verify stop priority, timeouts, confidence limits, and command bounds. |
| 9 | [Integrated system evaluation](course/week-09-system-evaluation/README.md) | Measure the complete simulated system's accuracy, latency, and robustness. |
| 10 | [ROS and hardware readiness](course/week-10-ros-hardware-readiness/README.md) | Demonstrate the ROS interfaces in a non-actuating mode and pass a safety review. |
| 11 | [Supervised Go1 integration](course/week-11-supervised-go1/README.md) | Perform a controlled, instructor-supervised robot checkout. |
| 12 | [Final demonstration and communication](course/week-12-final-demonstration/README.md) | Present a repeatable final demonstration supported by engineering evidence. |

## Safety gates

Progress is based on demonstrated readiness, not only the calendar.

| Gate | Required before moving forward |
|---|---|
| A: Local software | Week 1 simulation and stop/reset behavior work reliably. |
| B: Perception | Gestures have measured confidence and temporal-stability rules. |
| C: Simulated control | Gesture commands work in MuJoCo and fail safely. |
| D: Hardware readiness | Command limits, timeouts, stop priority, and ROS mock tests pass. |
| E: Physical robot | Instructor approves the test plan and directly supervises operation. |

Loss of a valid gesture, controller heartbeat, network connection, or operator
video must result in a stop command. Stop must override every motion request.

## How to use the weekly task folders

At the beginning of each week:

1. Open that week's `README.md`.
2. Read the objectives and prerequisites before changing code.
3. Activate the course Conda environment when instructed.
4. Complete the numbered tasks and record evidence as you work.
5. Review the completion checklist with your team.
6. Submit the listed deliverables using the instructor's requested method.

Do not copy commands blindly. Read the sentence before each command and compare
your output with the expected result.

## Repository map

```text
course/                                      weekly student task sheets
mujoco_playground/experimental/sim2sim/      Go1 ONNX simulation programs
mujoco_playground/_src/locomotion/go1/       Go1 model and environment code
learning/                                    reinforcement-learning programs
GO1_SETUP.md                                 instructor/reference setup notes
```

The Week 1 controller is
[`play_go1_keyboard.py`](mujoco_playground/experimental/sim2sim/play_go1_keyboard.py).
The bundled neural-network policy is
`mujoco_playground/experimental/sim2sim/onnx/go1_policy.onnx`.

## Getting started

Begin with [Week 1: GitHub onboarding and Go1 baseline](course/week-01-github-onboarding/README.md).
The existing Windows/MuJoCo setup instructions remain available in
[the simulation setup folder](course/week-01-windows-simulation/README.md).

## Project sources and license

This course repository is based on Google DeepMind's
[`mujoco_playground`](https://github.com/google-deepmind/mujoco_playground), an
open-source framework for robot learning and sim-to-real research. The original
project website is [playground.mujoco.org](https://playground.mujoco.org/).

The companion gesture-control architecture and course direction are documented
in [`DyCo-AI/go1_gesture_tracking`](https://github.com/DyCo-AI/go1_gesture_tracking).

The source code remains under the Apache License 2.0; see [LICENSE](LICENSE).
This repository is not an officially supported Google product.
