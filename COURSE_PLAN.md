# Gesture Navigation: Go1 Simulation, Go2 Hardware

The required midpoint is **webcam gesture navigation through a baseline MuJoCo maze by the end of Week 6**. Weeks are course-relative; hardware progress depends on readiness, not dates.

| Week | Focus | Evidence |
|---|---|---|
| 1 | GitHub, Conda, keyboard simulation baseline | Working setup and stop/reset demonstration |
| 2 | Go1 controller and simulation adapter | Explain `(vx, vy, yaw_rate)`; keyboard and scripted commands |
| 3 | Webcam acquisition and MediaPipe landmarks | Live annotated video; failure observations |
| 4 | Gesture vocabulary and recognition | STOP, FORWARD, LEFT, RIGHT; test across operators |
| 5 | Validation, mapping, command supervision | Hold-time, stale-input, stop and bounds tests; command logs |
| 6 | Integrated dashboard and baseline maze | Webcam + overview + robot FPV; three repeatable navigation trials |
| 7 | Go2 hardware inventory and setup | Windows 11, go2wifi, Wi-Fi/AES access, Basic WebRTC camera and status |
| 8 | Stationary Go2 checkout | Onboard camera, telemetry, voxels, fresh feedback, and the supervised stop procedure |
| 9 | Clemson Go2 UI and supervised gestures | Preview the Go2-specific vocabulary, then incremental bounded motion after instructor qualification |
| 10 | Physical maze construction and navigation | Measured clearances; staged supervised trials |
| 11 | Reliability and final demonstration | Repeatable trials, logs, presentation and reflection |
| 12, if available | Contingency and evaluation | Resolve remaining failures; complete documentation |

## Working reference implementation

Run `python run_gesture_navigation.py` from the repository root. See [Week 6](course/week-06-mock-command-mapping/README.md) for installation, gestures, troubleshooting and checkout.

| Weekly code | Responsibility |
|---|---|
| `course/week-02-go1-controller/simulation.py` | Existing ONNX policy adapter; reset; external/FPV renders; wall contacts |
| `course/week-03-webcam-basics/vision.py` | Timestamped capture, MediaPipe, latest annotated frame |
| `course/week-04-hand-landmarks/gestures.py` | Geometric gesture rules |
| `course/week-05-gesture-classification/safety.py` | Motion hold, input expiry, command limits and stop priority |
| `course/week-06-mock-command-mapping/` | Dashboard, independent simulation worker, maze scenes and trial CSVs |

Directory names remain stable so existing course links keep working. The Week 6 folder now contains the integrated navigation lab, including mock input as an initial check. Modules are shared through `course` without copying code or changing `sys.path`.

## Week 6 completion gate

- One launcher opens the webcam, simulation overview and robot FPV.
- One hand requests forward, left turn, right turn or stop.
- Fresh motion predictions must remain consistent for 0.30 s.
- STOP, UNKNOWN, no hand, multiple hands and camera failure request zero velocity immediately on receipt; stale input or a stalled dashboard expires after 0.40 s.
- The stop button / Space / Escape latches motion off; enabling requires explicit operator action.
- Reset clears command and policy history and disarms motion.
- Wall contact is detected for body and legs; start and goal are visible.
- Three consecutive maze trials complete without contact or manual reset, supported by CSV logs and a short recording.

A zero velocity is a standing request to the locomotion policy. Measure actual stopping time and distance; it is not a motor-off command. Computer load can affect real-time performance.

## Instructor and student responsibilities

Instructors provide the runnable simulator, dashboard, webcam/landmark pipeline, reference gesture path, bounded supervisor, scenes, logs, setup and reference tests. Students evaluate and improve gesture rules, recognition stability, mappings, operator feedback and repeatable navigation experiments. Instructor-enforced bounds and expiry remain in place during experiments.

The supplied geometric rules have no calibrated classification-confidence score. MediaPipe hand detection/tracking thresholds are not gesture confidence. Confidence-based classification is an optional extension requiring evaluation.

## Hardware phase: Go2 over WebRTC

Use [the Go2 hardware guide](course/GO2_HARDWARE.md) for Windows 11, the separate
`go2wifi` environment, Go2 Wi-Fi/AES access, stationary checks, the Clemson UI,
and recording/replay. This path uses the Go2's onboard camera and WebRTC endpoint;
the operator laptop does not need ROS, an external Jetson, or a ZED camera.

Weeks 1–6 continue to use the existing Go1 simulator, policy, gesture rules, and
limits. The hardware guide explicitly documents the different Go2 vocabulary and
speed profile. Shared gesture-package extraction and Go2 simulation are later
work, not part of this documentation update. Historical weekly folder names stay
unchanged so links continue to work.

The simulation dashboard does not contain the physical robot transport. Use the
separate [Go2 GitHub setup](https://github.com/sriram-2502/unitree-go2-setup). Do not send simulated
joint targets or the Go1 ONNX output to the Go2. Physical motion requires the
instructor-approved interface, verified communication/stop behavior, and direct
supervision. The old Go1/ROS/Jetson/ZED project remains a separate reference.

Start with flat native MuJoCo scenes. More complex BARN-derived or ICRA-inspired environments are later extensions, after the baseline gesture-navigation gate is demonstrated.
