# Creative Inquiry: Go1 Simulation to Go2 Gesture Navigation

This repository is the simulation and course workspace for a Clemson Mechanical
Engineering Creative Inquiry project. Students will learn how a quadruped robot
is commanded, develop a camera-based hand-gesture interface, and test their
ideas with the existing Go1 simulation before supervised work with the physical
Unitree Go2 over Wi-Fi/WebRTC on Windows 11.

**No previous Python, AI, or robotics experience is required.** The weekly tasks
introduce the command line, Conda, Python, Git, computer vision, robot commands,
testing, and system integration one step at a time.

Our companion project is
[`DyCo-AI/go1_gesture_tracking`](https://github.com/DyCo-AI/go1_gesture_tracking).
It remains a reference for the earlier Go1/ROS/Jetson/ZED hardware path. The
current course hardware target is **Go2 with the Clemson WebRTC UI**, described
in [the Go2 hardware guide](course/GO2_HARDWARE.md). ROS and an external Jetson/ZED
setup are not required on the Windows operator laptop. The Go1 simulation and
its installation instructions remain unchanged.

> [!IMPORTANT]
> Simulation is the first safety gate. Students must not connect software to or
> command the physical robot without instructor approval and supervision.

## Course materials and instructor reference

- **Course website:** [DyCo-AI Go1 Gesture Tracking](https://dyco-ai.github.io/go1_gesture_tracking/) provides the schedule, concepts, assignments, and submission expectations.
- **This repository:** runnable simulation examples, weekly labs, and student reports.
- **Hardware setup and instructor solution:** clone [`go2-webrtc-gesture-nav`](https://github.com/sriram-2502/go2-webrtc-gesture-nav) for the Basic UI and Clemson Go2 dashboard. Follow [Go2 hardware onboarding](course/GO2_HARDWARE.md) for clone, installation, and update commands. Ask the instructor only for private robot credentials and hardware approval.

The course is intended for Go1 and Go2 experiments. This version uses **Go1 in
simulation and Go2 over Wi-Fi/WebRTC on Windows 11 for hardware**. Physical Go1
integration is under development; this is not a claim that both hardware paths
are ready. Keep the simulation and hardware environments separate.

## Course challenge

Build and evaluate an interface that lets a human use simple hand gestures to
request bounded robot motions such as forward, backward, left, right, and stop.
The current simulator uses Go1; the hardware phase uses the Go2-specific gesture
table and speed profile in [the hardware guide](course/GO2_HARDWARE.md).
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
                     MuJoCo simulation                         supervised Go2 test
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
9. Integrate simulation, perception, command logic, and a qualified hardware interface.
10. Communicate engineering decisions, results, limitations, and next steps.

## Weekly roadmap

Each linked folder contains the week's learning objectives, preparation, tasks,
deliverables, and completion checklist. Complete the weeks in order.

| Week | Milestone | Student outcome |
|:--:|---|---|
| 1 | [GitHub onboarding and Go1 baseline](course/week-01-github-onboarding/README.md) | Access the repository, enter the assigned team branch, run the existing baseline, and document the work. |
| 2 | [Go1 controller behavior, control, and reinforcement learning](course/week-02-go1-controller/README.md) | Trace keyboard input, measure command sensitivity, and make one approved change. |
| 3 | [Webcam image acquisition](course/week-03-webcam-basics/README.md) | Capture, display, and describe images from a laptop webcam. |
| 4 | [Gesture vocabulary and recognition](course/week-04-hand-landmarks/README.md) | Recognize stop, forward and turning gestures. |
| 5 | [Gesture validation and command supervision](course/week-05-gesture-classification/README.md) | Test hold time, bounded commands, input expiry and stop priority. |
| 6 | [Integrated dashboard and simulation maze](course/week-06-mock-command-mapping/README.md) | Navigate with webcam gestures, overview and simulated robot FPV. |
| 7 | [Go2 hardware setup](course/week-07-gesture-simulation/README.md) | Prepare Windows 11, go2wifi, Go2 Wi-Fi, AES access, and the Basic WebRTC UI. |
| 8 | [Stationary Go2 checkout](course/week-08-safety-testing/README.md) | Verify WebRTC, telemetry, onboard camera, voxels, and the supervised stop procedure. |
| 9 | [Go2 gesture dashboard](course/week-09-system-evaluation/README.md) | Use the Clemson UI, qualify the Go2 gesture mapping, and test short motions under supervision. |
| 10 | [Physical maze](course/week-10-ros-hardware-readiness/README.md) | Build the maze and run staged navigation trials. |
| 11 | [Reliability and demonstration](course/week-11-supervised-go1/README.md) | Complete repeatable tests and present results. |
| 12, if available | [Contingency and evaluation](course/week-12-final-demonstration/README.md) | Complete remaining validation and documentation. |

## Run the Week 6 dashboard

After the Week 1 repository installation, run from the repository root:

```powershell
conda activate go1-mj-playground
python -m pip install -r course/requirements-sim.txt
python course/week-03-webcam-basics/download_hand_model.py
python run_gesture_navigation.py
```

The dashboard displays your annotated webcam, MuJoCo maze overview and simulated
robot FPV. Motion starts disabled. See the [Week 6 lab](course/week-06-mock-command-mapping/README.md)
for gestures, keyboard/mock modes, stop behavior and navigation checkout.

## Safety gates

Progress is based on demonstrated readiness, not only the calendar.

| Gate | Required before moving forward |
|---|---|
| A: Local software | Week 1 simulation and stop/reset behavior work reliably. |
| B: Perception | Gestures have measured confidence and temporal-stability rules. |
| C: Simulated control | Gesture commands work in MuJoCo and fail safely. |
| D: Hardware readiness | Command limits, timeouts, stop priority, and hardware-interface mock tests pass. |
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

## Student branch and submission policy

Each student submits a weekly `README.md` in their own folder on the assigned
`team-alpha` or `team-bravo` branch:

```text
course/student-work/<team>/<first-last>/week-XX/README.md
```

Code experiments and full run recordings stay local throughout the course unless
the instructor requests otherwise. Optional small MP4/GIF evidence is welcome;
the final report is a Markdown report at the end of the course.
Follow [the submission and data policy](course/SUBMISSIONS.md) and
[weekly report template](course/WEEKLY_REPORT_TEMPLATE.md).

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

The earlier Go1/ROS hardware architecture is documented in
[`DyCo-AI/go1_gesture_tracking`](https://github.com/DyCo-AI/go1_gesture_tracking).
For the current Go2/WebRTC hardware phase, start with
[course/GO2_HARDWARE.md](course/GO2_HARDWARE.md).

The source code remains under the Apache License 2.0; see [LICENSE](LICENSE).
This repository is not an officially supported Google product.
