# Go2 hardware onboarding for Creative Inquiry students

The hardware phase uses a **Unitree Go2, Windows 11 laptop, and Go2 Wi-Fi/WebRTC**.
You continue learning from the existing Go1 simulator, but the physical robot is
Go2. This guide does not change the simulation installation, ONNX policy, limits,
gesture rules, team-branch policy, or weekly submission procedure.

## Understand the two cameras and computers

```text
Windows webcam -> MediaPipe -> gesture -> supervised velocity request
                                            |
                                  local Clemson web UI
                                            |
                                    Wi-Fi / WebRTC
                                            |
                                           Go2
                                            |
                      onboard camera + robot state + available voxels
                                            |
                                  local Clemson web UI
```

| Component | Its job |
| --- | --- |
| Windows laptop webcam | Sees the operator's hand; MediaPipe runs locally |
| Go2 onboard camera | Sees the maze; the robot view appears in the browser |
| Browser UI | Displays robot video/voxels and extracted hand skeletons; uses one robot connection |
| Go2 onboard controller | Carries out supported high-level motion requests |

The operator laptop needs no ROS, WSL, Docker, external Jetson, or ZED camera for
this path. The older Go1/ROS/Jetson AGX/ZED project is a separate hardware reference.
Do not copy Go1 joint targets or ONNX outputs into the Go2 interface.

## What to obtain from the instructor

- Assigned Go2, charged battery, paired remote, and supervised operating area.
- Go2 hotspot name/password and the assigned robot's private 32-hex AES key.
- An approved copy of the companion `unitree_go2_setup` folder and its version.
- Confirmation of which firmware, camera, feedback, motion, and stop checks have passed.

The repository separation is planned, not completed: use the supplied bundle
rather than guessing a future GitHub URL. Keep it separate from this simulation
repo. The commands below assume it is under your Windows Downloads folder; adapt
the path if the instructor places it elsewhere. No AES key is included here.

## Install while connected to the internet

Keep the existing `go1-mj-playground` simulation environment. Create a separate
hardware environment in **Anaconda Prompt / Miniconda Prompt**:

```bat
cd /d "%USERPROFILE%\Downloads\unitree_go2_setup"
conda create -n go2wifi python=3.11 pip -y
conda activate go2wifi
python -m pip install --upgrade pip
python -m pip install -r webrtc\requirements.txt -r webrtc\requirements-gestures.txt
python -m webrtc.gesture_preview.download_model
python -m pip check
```

If `go2wifi` already exists, activate it instead of recreating it. Install the
instructor-approved requirements; do not independently upgrade the working
driver/MediaPipe/OpenCV combination during a trial.

Install Git for Windows if absent. In **PowerShell**, from the companion folder:

```powershell
Set-Location "$env:USERPROFILE\Downloads\unitree_go2_setup"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\webrtc\setup-ui.ps1 -Edition all
```

This obtains the pinned Basic UI and Clemson source plus a workspace-local Node
runtime. The execution-policy flag affects this process only. Stop dashboard
servers before rerunning setup. Detailed dependency versions and troubleshooting
are in the companion `webrtc/DEPENDENCIES.md`; the course does not duplicate its
dependency lock or vendor UI source.

## Connect to Go2 Wi-Fi

1. With the instructor, power on the Go2 and complete the normal robot/remote checks.
2. Connect Windows to the assigned **Go2 Wi-Fi hotspot** using the private Wi-Fi credentials.
3. The hotspot's default robot IP is **`192.168.12.1`**. This is different from the
   onboard Jetson's Ethernet address used in the separate research/ROS path.
4. Close the phone app and disconnect other robot scripts/dashboard tabs before
   opening a robot connection. Use one client at a time.

Install software before switching networks; the robot hotspot may not provide
internet access. Ethernet and Jetson SSH are not required for this course path.

## Stationary checkout before any motion

Start Basic first, in **PowerShell from the companion folder**:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\webrtc\start-ui.ps1 -Edition basic
```

Open Chrome at `http://127.0.0.1:5173/`. Choose Connect, Go2, and Access Point
(Direct), then use `192.168.12.1`. Enter the assigned AES key if prompted.
Follow the supplied bundle's `webrtc/UI_SETUP.md` if its pinned interface differs.

With locomotion disabled, record each check as **pass / fail / untested**:

- Correct assigned robot and successful authenticated WebRTC connection.
- Changing live onboard video, rather than a frozen image.
- Robot battery/state feedback arriving; identify unavailable or stale values.
- LiDAR/voxel display when the onboard stream is available. Do not infer full
  mapping/localization/navigation support from the presence of voxel graphics.
- Known paired-remote intervention procedure and instructor-reviewed software Stop.

Do not experiment with actions, gait modes, autonomous goals, or patrol during
stationary onboarding. Basic's upstream controls are not the same as the Clemson
gesture supervisor. A stationary screenshot does not qualify physical stopping.

Basic follows upstream key-cache behavior. Do not publish browser logs, screenshots,
passwords, keys, or cloud tokens. Clear saved site data after using a shared lab PC.

## Open the Clemson gesture UI

Disconnect Basic from the robot and stop its server with Ctrl+C. Use two terminals,
both in the companion `unitree_go2_setup` folder:

**Terminal 1 — Anaconda Prompt:**

```bat
conda activate go2wifi
python -m webrtc.gesture_preview.server
```

**Terminal 2 — PowerShell:**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\webrtc\start-ui.ps1 -Edition clemson
```

Open `http://127.0.0.1:5174/`. Hand tracking starts automatically when the side
panel opens; only skeletons and labels are displayed, not webcam video. Close
the simulator or another application using the webcam first. For another webcam,
launch the service with `--camera 1` instead of the default device 0.

Preview your gestures with robot control disabled. In the Go2 connection form,
leave the editable IP at **`192.168.12.1`**, enter the private AES key, and select
**Connect and open web view**. Successful validation opens camera/voxels directly.
The Clemson key is held in page memory until disconnect/reload. A valid key does
not authorize unsupervised motion.

The main-view overlay distinguishes **requested**, **supervised**, **transmitted**,
and **measured** velocities. A transmitted command is not proof of execution.
Recognition details explain which fingers and directions were detected; check
these before enabling motion. Hiding the hand panel stops its webcam tracking.

## Go2 gestures and velocity settings

This is the Go2 hardware vocabulary. Weeks 1–6 currently retain the original
simulation gestures; do not assume their LEFT/RIGHT labels mean the same motion.
Compare the two tables explicitly before changing robot backends.

| Hand pose in the mirrored panel | Go2 request at default settings |
| --- | --- |
| Index straight up; other fingers curled; palm facing webcam | Forward: `(vx, vy, wz) = (+0.5, 0, 0)` |
| Index pointing left | Sideways left: `(0, +0.5, 0)` |
| Index and middle both pointing left | Sideways right: `(0, -0.5, 0)` |
| Thumb up; other fingers curled | Turn left in place: `(0, 0, +0.8)` |
| Thumb down; other fingers curled | Turn right in place: `(0, 0, -0.8)` |
| Open palm or closed fist | Zero/stop request |
| No hand, two hands, or uncertain pose | Zero/stop request |

`vx` and `vy` use **m/s**; `wz` uses **rad/s**. Directions are relative to the
robot: +vx forward, +vy its left, and +wz counterclockwise viewed from above.
The robot's left can differ from the operator's left in the room.

- Forward magnitude: **0.5–1.0 m/s**, default **0.5**.
- Sideways magnitude: **fixed at 0.5 m/s**, sign chosen by the gesture.
- Turn magnitude: **0.5–1.0 rad/s**, default **0.8**.
- Inactive axes: zero. One gesture controls one axis; no ramps are added.
- A clear movement gesture must persist for **300 ms**. A held gesture continues
  requesting movement; it is not a fixed-distance step.
- Missing/uncertain hands request zero without a movement hold; input older than
  **400 ms** is rejected. Robot camera/state checks also gate control.

These are programmed request limits, not verified physical capability limits.
Do not raise settings merely because the UI accepts them. The visual guide and
beginner Python examples are in the companion `webrtc/clemson/README.md` and
`webrtc/gesture_preview/README.md`. No backward gesture is assigned in this version.

## First supervised motion checks

Only proceed after the instructor approves the physical setup and communication,
standing, feedback, video, and intervention checks. Keep a clear, level operating
area and the paired remote in the instructor's hands. The interface does not
stand the robot up or provide a leg controller.

1. If required by the instructor, first run the companion's bounded script from
   Anaconda Prompt: `python webrtc\go2_wifi_velocity_test.py --vel 0.5 --time 1`.
   It is a motion command. Disconnect the dashboard first; inspect actual travel
   and stopping, with clear space for more than the nominal requested distance.
2. Reconnect only the Clemson UI, then preview each intended pose without enabling.
3. Show an open palm/fist. Click **Enable gesture control** below the hand view and
   keep the stop pose while the motion-service check completes.
4. Test one brief motion at a time, starting with defaults. Return to a stop pose
   and visually confirm stopping before proceeding to another axis.
5. Use **Stop** (below Disconnect or under the hand view) to revoke gesture control.
   Inspect the stop result and actual robot. The guarded sequence requests zero,
   StopMove, and only then BalanceStand if low-speed upright feedback is confirmed.
6. If any stop/stance is unconfirmed, use the paired remote and resolve the cause
   with the instructor before another trial. Browser/network/power failures can
   prevent software stopping; the screen button is not a hardware emergency stop.

Changing speed settings or obstacle avoidance disables gesture control. The
avoidance switch reads back the robot's state; OFF disables avoidance behavior,
and ON does not guarantee every obstacle will be avoided. Do not change it merely
to get past an unexplained refusal to move. Record its state for each experiment.

## Record, replay, and submit evidence

Before enabling gesture control, turn the overall **Recording** switch ON and
choose the Clemson dashboard tab in Chrome's capture chooser. The chooser may
trigger the focus-loss stop, so enable control separately afterward. Turn
Recording OFF to stop and save the video and available data together as one ZIP.

Use **Replay** to open the ZIP without a robot command connection. Review the
dashboard video or interactive recorded hands/voxels/telemetry, and inspect the
CSV files. Native MP4 is preferred, WebM fallback is supported, and the companion
`webrtc/RECORDING.md` describes local conversion, data coverage, size/duration
limits, and approximate timestamp alignment. Try the synthetic replay demo first.

Record robot assignment without exposing its key, software/firmware versions,
speed settings, gesture mapping, avoidance state, operator, conditions, result,
and interventions. Separate simulation evidence, stationary checks, and actual
supervised motion. Submit sanitized summaries using the existing team/weekly
policy; keep run ZIPs, keys, and account credentials out of public Git history.

## What is and is not qualified

The companion implementation has offline gesture/supervision, recording-format,
and build checks. That is not a claim that every feature has passed on this Go2.
The instructor maintains the hardware qualification record. Actual recognition,
physical motion/stopping, firmware-specific services, browser capture, and combined
recording performance must be checked for the supplied hardware and bundle version.

Go2 simulation and a shared cross-repository gesture package remain future work.
The current Go1 simulation controller and lessons are intentionally preserved.

## Course reports and local data

Follow [the submission and data policy](SUBMISSIONS.md): weekly README reports
in your student folder, optional small sanitized media, full runs stored locally,
and a final Markdown report. Ask the instructor for the AES key. Install while
on internet, then join the assigned Go2 hotspot for robot access; do not use
Clemson campus Wi-Fi for the robot connection. Campus firewall/client isolation
can interfere; do not disable security controls to work around it.
