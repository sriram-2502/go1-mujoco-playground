# Course Reference Code

The simulation reference is implemented across the corresponding weekly folders.
The course hardware target is now Go2/WebRTC using a separate instructor-provided
Windows application; see [the hardware guide](course/GO2_HARDWARE.md). The authoritative schedule is [COURSE_PLAN.md](COURSE_PLAN.md).

The earlier detailed architecture proposal is preserved in [the reference archive](course/reference/STARTER_CODE_PROPOSAL.md) as historical design context; it is not the current Go2 deployment guide or an implementation inventory.

## Launch

```powershell
conda activate go1-mj-playground
python -m pip install -r course/requirements-sim.txt
python course/week-03-webcam-basics/download_hand_model.py
python run_gesture_navigation.py
```

The existing editable repository installation and Go1 assets from Week 1 are prerequisites. See [Week 6](course/week-06-mock-command-mapping/README.md) for details.

## Architecture

```text
Week 3 webcam/MediaPipe -> Week 4 gesture rules -> timestamped Prediction
                                                        |
Keyboard/mock source -----------------------------------+
                                                        v
                                              Week 5 Supervisor
                                                        |
                                                   (vx, vy, yaw)
                                                        v
                                              Week 2 Simulation
                                                        |
                                      original 48-input / 12-output ONNX
                                                        v
                                               native MuJoCo Go1
                                                        |
                                      overview + attached robot FPV
                                                        v
                                              Week 6 Dashboard
```

Webcam capture, simulation, rendering and UI run independently. Latest-value mailboxes avoid frame backlogs. The simulation worker evaluates input age and dashboard heartbeat on every loop, applies commands and logs at 10 Hz; simulation uses 0.004 s steps and the original 0.020 s policy interval. A separate OpenGL thread renders private `mjData` snapshots for two configurable-resolution views, targeting 30 Hz (640x360, 960x540 or 1280x720). Quality 1280x720 is the dashboard default. Slow graphics drops intermediate snapshots without blocking physics or its watchdog. Telemetry updates at 20 Hz; images bypass that telemetry mailbox. The UI polls the latest render frames with a precise 16 ms timer and only rescales new frames or resized panels. Absolute render deadlines avoid drift from Windows wait granularity. ONNX inference uses one CPU thread, perception is paced to 30 Hz, and logs flush once per second and on shutdown.

Rendering disables shadows, reflections and offscreen multisampling to avoid expensive graphics-driver paths. The Settings diagnostics and CSV expose simulation real-time factor (1.00 means real speed), view FPS and rendering duration in the CSV. Severe OS/CPU stalls still cap physics catch-up rather than replay a large burst of commands.

`course/__init__.py` provides imports such as `from course import simulation, vision, gestures, safety`. It uses standard `importlib` to resolve the existing hyphenated weekly directory names. No per-week package installations or runtime `sys.path` changes are needed; launch from the repository root.

## Teaching boundaries

- Week 2: trace policy observations and high-level command effects.
- Week 3: measure acquisition timing and landmark failure cases.
- Week 4: evaluate and improve `gestures.classify()`.
- Week 5: explain and test `Supervisor.approve()` using supplied unit tests.
- Week 6: integrate, navigate, log and evaluate the baseline maze.

Reference motion is limited to 0.25 m/s forward and +/-0.50 rad/s yaw; lateral velocity is zero. Backward and slow-mode gestures are extensions. The reference supervisor rejects configurations exceeding these limits.

The original `mujoco_playground/experimental/sim2sim/play_go1_keyboard.py` remains the keyboard baseline. Its policy inference is reused without modifying the model weights. Course walls use a separate collision bit for physical robot geometry while preserving baseline feet-floor and robot self-collision behavior.

## Checks

```powershell
python -m unittest discover -s course/week-05-gesture-classification -v
python -m unittest discover -s course/week-06-mock-command-mapping -v
```

The second command loads MuJoCo assets and renders both views. Live camera recognition and operator navigation need a separate manual checkout. Camera and model failures are displayed in the dashboard and inhibit gesture motion.

## Go2 hardware phase

Use [course/GO2_HARDWARE.md](course/GO2_HARDWARE.md) for the Windows 11 Go2 Wi-Fi
and WebRTC path. The companion Clemson UI supplies the camera/voxel view,
MediaPipe hand panel, explicitly enabled high-level gesture commands, and
recording/replay. It runs in the separate `go2wifi` environment and Node runtime;
these dependencies are not added to this simulator environment.

The Go1 simulation code, ONNX policy, limits, and current gesture vocabulary are
unchanged. The Go2 application has a different gesture table and speed profile,
documented in the hardware guide. Physical camera, feedback, command, and stop
behavior must be qualified on the actual Go2 before supervised motion. The
older external Jetson/ZED/ROS path is not required for this course deployment.

For repeatable live resolution comparisons, run `python -m course.week-06-mock-command-mapping.benchmark`. See the Week 6 lab for measurement definitions and limitations.

The laptop driving view uses a large simulation panel and two compact webcam/FPV panels, with only essential motion/trial controls below. Dropdowns, gesture help, metrics and logs are in the scrollable Settings dialog. Opening Settings disarms motion. The default window is maximized and keeps the full uncropped feeds.
