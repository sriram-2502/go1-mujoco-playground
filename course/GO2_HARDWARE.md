# Go2 hardware onboarding for Creative Inquiry students

The hardware phase uses a Go2, Windows 11, and the
[personal Go2 gesture UI](https://github.com/sriram-2502/go2-gesture-nav).
**One setup for Weeks 7 onward; no ROS or separate Basic UI repo.** Go1 simulation
and student reports stay in this playground checkout.

## Which setup to use

The [personal repo README](https://github.com/sriram-2502/go2-gesture-nav#1-install-once)
is the source of installation and daily launch commands. Use it rather than
copying older `webrtc/` instructions. The app now has root-level scripts and
one `requirements.txt`.

| Course stage | Same app, different readiness gate |
| --- | --- |
| Week 7 | Install, preview hand tracking, and inspect robot camera/state while stationary; leave movement disabled |
| Week 8 | Review freshness, control state, feedback, stopping, and intervention procedures |
| Week 9 onward | Supervised gesture walking, recording/replay, and flat-maze trials |
| Optional extension | Existing Jump once / Bound gait buttons, only after separate instructor approval |

The playground's `creative-inquiry-dev` branch is instructor course authoring.
The runnable Go2 UI is the separate personal repo, not a playground branch.
Students keep the [assigned team-branch/report procedure](UPDATES.md).

## Visual guide for your first session

Use the [screen guide](https://github.com/sriram-2502/go2-gesture-nav/blob/main/docs/STUDENT_ORIENTATION.md)
and [illustrated gestures](https://github.com/sriram-2502/go2-gesture-nav/blob/main/dashboard/README.md#gesture-guide-what-your-hand-commands).
The Windows webcam sees your hand; the Go2 camera sees the operating area.
The app requests body motion; Unitree's onboard controller handles the joints.

## Install and start the same project

Install while internet is available, before joining the Go2 hotspot. Follow
[the complete quick start](https://github.com/sriram-2502/go2-gesture-nav#1-install-once):
clone the personal repo, create/activate `go2wifi`, install root
`requirements.txt`, download the hand model, and run root `setup-ui.ps1`.

From that personal repo root, keep two terminals open:

**Terminal 1 — Anaconda / Miniconda Prompt:**

```bat
conda activate go2wifi
python -m gesture_preview.server
```

**Terminal 2 — PowerShell:**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\start-ui.ps1
```

Open **http://127.0.0.1:5174/**. The gesture service uses **8766** through the
dashboard proxy. Close another webcam app first. No `-Edition` flag is required.
Do not merge the hardware application's files into the playground.

If you used the old layout, update and rerun the root setup once. Reuse the
`go2wifi` environment; old generated `webrtc/` checkouts are no longer used.
See the [migration/update note](https://github.com/sriram-2502/go2-gesture-nav#update-and-restart).

## Stationary checkout before any motion

With the instructor, power on the assigned Go2 and complete the normal remote/
standing checks. Obtain its private hotspot password and AES key. Join the
**Go2 hotspot**, not Clemson campus Wi-Fi; the default robot IP is
**192.168.12.1**. Close the phone app and other robot clients before connecting.

Keep control disabled and record **pass / fail / untested** for:

- Authenticated connection to the assigned robot.
- Changing onboard camera video and fresh body-state feedback.
- Available voxels; these do not establish an automatic obstacle planner.
- Hand skeleton/labels in preview and requested/supervised/transmitted/measured velocity displays.
- Battery display, Stop, optional behavior buttons, and the UI build ID.
- Paired-remote intervention procedure and the plan to verify physical stopping.

Match **Navigation | UI build ID** with the launcher, then record the Git commit.
If they differ, stop the old server, restart, and hard-refresh Chrome.
Do not activate Jump/Bound or other actions during stationary onboarding.

## Bring your gesture work from previous weeks

Follow [the integration guide](https://github.com/sriram-2502/go2-gesture-nav/blob/main/docs/STUDENT_INTEGRATION.md).
Reuse recognition functions, not the Go1 simulation runtime or ONNX outputs.
Keep the hardware timestamps, hold/freshness checks, limits, explicit enable,
and stop/feedback checks. Preview locally before reviewed motion trials.

## Go2 gestures and velocity settings

Match the mirrored hand panel. Directions use the robot's body frame:
+vx forward, +vy left, +wz counterclockwise from above.

| Pose | Default request |
| --- | --- |
| Index up, other fingers curled, palm toward webcam | Forward, 0.5 m/s |
| Index pointing left | Sideways left, 0.5 m/s |
| Index + middle fingers pointing left | Sideways right, 0.5 m/s |
| Thumb up / down | Turn left / right, 0.8 rad/s |
| Open palm, fist, no hand, or unclear pose | Stop request |

One gesture requests one axis. Movement needs 300 ms consistency; input older
than 400 ms is rejected. Forward/turn speed settings differ from the unchanged
Go1 simulator. See [the full gesture guide](https://github.com/sriram-2502/go2-gesture-nav/blob/main/dashboard/README.md)
for configured limits. No backward gesture is assigned.

## First supervised motion checks

After instructor approval, use a clear, level area and keep the paired remote
with the supervisor. The app does not stand the robot up.

1. Preview every intended gesture with navigation disabled.
2. Click **Enable gesture control** directly. There is no palm/fist startup pose; new frames, the consistency hold, and fresh video/state still gate motion.
3. Test one brief axis at a time, return to Stop, and verify actual stopping before proceeding.
4. Check Stop and read its recovery result. A transmitted or acknowledged request is not proof of a physical stop.
5. If recovery is unconfirmed, use the paired remote and resolve it before another trial.

Obstacle avoidance has separate state readback. Do not infer protection from
voxels or change settings merely to bypass an unexplained refusal to move.
Record its reported state in each experiment.

## Optional Forward Jump and Bound gait

These buttons already exist below the battery; they are not default gestures.

- **Jump once:** pauses gesture navigation and requests one forward jump. Repeat actions remain locked until Stop/recovery is confirmed.
- **Bound gait:** pauses navigation, requires successful reply/new mode feedback, then requires explicit gesture enabling to navigate. Stop requests exit.

Read [behavior and recovery](https://github.com/sriram-2502/go2-gesture-nav/blob/main/dashboard/CONTROL_EXTENSIONS.md).
Missing foot-contact data or unconfirmed recovery leaves navigation locked.
Restore standing using the paired remote before the explicit remote-recovery
acknowledgement; that acknowledgement sends no motion and does not enable walking.

The maintainer reported a successful forward jump/landing, which does not
qualify every firmware or recovery case. Bound needs its own supervised checks.
Keep ordinary walking in a flat maze as the required baseline. These extensions
require separate approval; Stationary Look Around remains disabled.

## Record, replay, and submit evidence

Turn Recording ON before enabling gestures and choose the dashboard tab in
Chrome. Turn it OFF to save the local ZIP. Replay is offline and sends no robot
commands. See [recording details](https://github.com/sriram-2502/go2-gesture-nav/blob/main/docs/RECORDING.md).
Browser receive timing is not synchronized sensor acquisition timing.

Record commit/build ID, assigned robot without credentials, gesture mapping,
speeds, avoidance state, conditions, results, and interventions. Full runs remain
local. Follow [the submission policy](SUBMISSIONS.md) for individual weekly README
reports on the assigned team branch and optional small sanitized media.

## What is and is not qualified

The navigation baseline has maintainer-confirmed hardware operation and offline
application tests. This does not qualify all optional behaviors, stopping cases,
or Go2 firmware. Version changes still need a supervised checkout. Software Stop
depends on communication and is not a hardware emergency stop.
