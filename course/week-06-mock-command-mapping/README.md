# Week 6: Integrated Gesture Navigation in MuJoCo

## Handoff to the Go2 hardware phase

Complete the simulation checkout and evidence below before starting Week 7.
With your instructor, review the Go2 gesture table, different speed limits,
two-camera layout, and separate `go2wifi` environment. List what the simulation
evidence establishes and what still needs physical qualification: connection,
video/feedback freshness, gesture recognition, and actual motion/stopping.
The simulation launcher remains a Go1 simulator and does not connect to Go2.

See [Go2 hardware onboarding](../GO2_HARDWARE.md) for the later hardware path.

## Milestone

Use webcam gestures to navigate a Go1 through the baseline two-turn maze while viewing the webcam, external simulation and simulated robot FPV in one dashboard. This folder keeps its original name for existing course links.

## Setup and launch

From the repository root, after completing the Week 1 editable installation:

```powershell
conda activate go1-mj-playground
python -m pip install -r course/requirements-sim.txt
python course/week-03-webcam-basics/download_hand_model.py
python run_gesture_navigation.py
```

The launcher opens the dashboard, starts webcam/MediaPipe capture, and loads the Go1 policy and both simulation views. Startup is asynchronous so model loading cannot freeze the window. Motion starts disabled.

Options:

```powershell
python run_gesture_navigation.py --quality quality
python run_gesture_navigation.py --quality performance
python run_gesture_navigation.py --camera 1
python run_gesture_navigation.py --scene arena
python run_gesture_navigation.py --scene corridor --input keyboard
python run_gesture_navigation.py --scene arena --input mock
```

The original keyboard baseline remains available through the Week 1 instructions.

## Dashboard

- Quality presets: Performance 640x360, Balanced 960x540, Quality 1280x720 (default) for each simulated camera.
- Laptop layout: simulation occupies roughly 70% of the width, with webcam and FPV stacked beside it. Video stays uncropped; the window opens maximized. Click Enlarge on the smaller simulation/FPV panel to swap the large view. F11 toggles fullscreen.
- The main window shows only the three feeds, the detected gesture, short motion status, and large Enable/Stop/Reset/Trial/Settings controls. Camera and simulation errors remain visible.
- Settings holds quality, input and course dropdowns, the gesture guide, trial metrics, performance diagnostics and log location. Opening Settings disarms motion; re-enable after closing it.
- Changing quality, input or scene reloads the simulation and disarms motion; finish/save the trial first.
- External overview: blue start, green goal and physical maze walls.
- Operator webcam: mirrored preview with hand landmarks.
- Brackets beneath the gesture compare the approved velocity command (`cmd`) with measured simulator motion (`sim`): forward `vx` in m/s and turning `yaw` in rad/s. These values also show residual motion after a stop; they are actual sensor readings, not copies of the requested command.
- Robot FPV: body-mounted camera looking forward through the course.
- Telemetry in Settings: approved command, elapsed trial time, wall contact episodes, input age and position.
- Controls: explicit motion enable, latched stop, reset, scene selection and trial start/end.
- CSV: automatically written under ignored `logs/`; trial IDs distinguish scored runs from practice.

## Reference gestures

Use one hand with the palm visible. Keep the indicated fingers extended and the other fingers folded; thumb position is ignored.

| Pose | Intent | Command |
|---|---|---|
| Open palm or closed fist | STOP | Zero |
| Index finger | FORWARD | vx = 0.25 m/s |
| Index + middle (V) | LEFT | yaw = +0.50 rad/s |
| Index + middle + ring | RIGHT | yaw = -0.50 rad/s |
| No hand, multiple hands, other pose | Invalid / stop | Zero |

Motion gestures require 0.30 seconds of fresh consistent input. Stop/invalid input bypasses this hold. A 0.40-second frame or UI heartbeat timeout requests zero command. New motion after invalid input must satisfy the hold again. These are geometric rules, not confidence-scored recognition; measure mistakes across people and lighting conditions.

## Checkout sequence

1. In the flat arena, leave motion disabled and verify labels/landmarks.
2. Enable motion, request forward, then open palm. Confirm actual motion and stopping distance.
3. Test both turning directions, returning to stop between gestures.
4. Test hand loss, unknown pose, a second hand, camera failure and stale input. Record stop latency.
5. Press STOP, Space or Escape. Motion must stay disabled until Enable motion is clicked again. Loss of window focus also disarms motion.
6. Reset. The pose, command, previous policy action, contact count and trial state must reset.
7. Practice the straight corridor, then select the maze.
8. Start a trial, enable motion and navigate from blue to green: forward, left turn, forward, right turn, forward. Entering the goal disarms motion. Reset before the next run.
9. Complete three consecutive trials without wall contact or manual reset; save logs and a short video.

Arrow keys in `--input keyboard` mode request forward/left/right while held; releasing stops. Mock mode repeats STOP, FORWARD, STOP, LEFT, STOP, RIGHT, STOP in two-second intervals. Mock mode checks integration; it does not autonomously solve the maze. Camera loss does not disable the explicitly selected keyboard/mock sources.

A zero velocity requests standing through the locomotion policy, not motor-off. The policy does not track requested velocities perfectly. Wall contacts count transitions into contact, not every physics frame. Reset starts a new contact count; reset events are also logged. Goal completion currently uses the robot root position inside the goal radius.

## Weekly source map

- Week 2 `simulation.py`: model, policy, reset, collision masks and cameras.
- Week 3 `vision.py`: webcam capture and MediaPipe worker.
- Week 4 `gestures.py`: reference gesture rules.
- Week 5 `safety.py`: timestamps, hold, bounds and stop priority.
- This week `runtime.py`: independent stepping, watchdogs, input sources and CSV.
- This week `dashboard.py`: UI and controls.
- This week `scenes/`: flat arena, straight corridor and two-turn maze.

## Verification

```powershell
python -m unittest discover -s course/week-05-gesture-classification -v
python -m unittest discover -s course/week-06-mock-command-mapping -v
```

Physics checks cover forward movement and stopping, reset history, robot-wall contacts, all scenes, both rendered cameras and a test-only waypoint pilot that reaches the maze goal using bounded symbolic commands. The pilot is a traversability test, not an autonomous dashboard mode. Automated checks do not replace live recognition and navigation trials.

## Troubleshooting

- Missing model: run the Week 3 model downloader; it needs internet access once.
- Webcam unavailable: close other camera apps, check Windows camera permissions, try `--camera 1`, then restart the launcher. Keyboard mode can check the simulator independently.
- Import error: activate the course environment, install the course requirements and launch from the repository root.
- Missing robot meshes: finish the original Week 1 asset setup; the adapter reuses `get_assets()` from the existing simulator.
- Blank/error simulation views: check the displayed error and graphics/OpenGL support. Rendering needs a working graphics context.
- Slow simulation: open Settings and check `Sim: ...× real time` (target 1.00) and display/render FPS in diagnostics. The two views target 30 Hz on a separate thread; slow graphics skips old snapshots without blocking physics. Shadows, reflections and offscreen multisampling are disabled. Close heavy applications if simulation speed remains low. CSV fields `real_time_factor`, `render_fps` and `render_ms` support diagnosis.
- Robot fell: reset before enabling motion again.

## Deliverables

Architecture sketch, gesture evaluation, failure-case log, three trial CSVs, wall-contact/reset counts, measured stopping behavior and a short demonstration. Review the midpoint gate with the instructor before starting hardware work.

Next: [Week 7 Go2 hardware setup](../week-07-gesture-simulation/README.md), using Windows 11 and Wi-Fi/WebRTC.

## Repeatable live display benchmark

```powershell
python -m course.week-06-mock-command-mapping.benchmark
```

This opens the real dashboard, keeps motion disabled and measures all three resolutions after warm-up. Results are saved to ignored `logs/dashboard-benchmark-*.json`. Use `--preset balanced` to test one preset, or `--seconds 15` for a longer interval. Close other webcam apps before testing. GUI checks use a placeholder webcam and do not establish live gesture accuracy.

Measurements include simulation speed, new frames submitted to Qt, pair-render duration, render-completion-to-UI delivery age, UI image conversion/scaling cost, input frame age and process CPU time. These are not monitor scanout timings or gesture-to-motion latency. CPU percentages use 100% for one core, and GPU utilization is not sampled. Lighting and hand visibility affect MediaPipe tracking/detection cost, so camera timing comparisons need controlled conditions.

## Weekly submission

Submit your individual `week-06/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
