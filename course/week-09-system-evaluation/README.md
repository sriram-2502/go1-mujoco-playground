# Week 9: Clemson Go2 dashboard and supervised gesture navigation

## Hardware path

This course now uses **Unitree Go2 + Windows 11 + Wi-Fi/WebRTC** for physical
navigation. The Go2's onboard camera supplies robot FPV; the Windows webcam
supplies MediaPipe hands. No laptop ROS installation or external Jetson/ZED stack
is required. This folder retains its historical name to preserve existing links.

The simulation code and the Weeks 1–6 simulation exercises are unchanged. Use the separate [Go2 GitHub setup](https://github.com/sriram-2502/go2-webrtc-gesture-nav); the simulation launcher does not connect to the physical robot.

## Prerequisites

- Week 6 webcam/overview/FPV simulation checkpoint with logs.
- Instructor-approved robot assignment, hardware checkout, and operating procedure.
- Direct instructor supervision and the paired remote for physical motion.

## Learning objective

Map each Go2 hand pose to one body-frame velocity axis and evaluate recognition.

## Activities

1. Review the [Go2 gesture table and speed settings](../GO2_HARDWARE.md#go2-gestures-and-velocity-settings); they differ from the unchanged simulation reference.
2. Validate each gesture across operators in preview, including palm orientation, no hand, two hands, and transitions.
3. After instructor qualification, perform the bounded script checkout and short one-axis trials described in the hardware guide.
4. Show a stop pose, explicitly enable gesture control, and verify forward, sideways, and turn-in-place requests individually.
5. Verify stopping and stale-input behavior under supervision. Keep obstacle-avoidance changes deliberate; changing its switch disables gesture control.
6. Record a short run, save its ZIP, and inspect offline replay and the requested/transmitted/measured velocity data.

## Expected evidence

A Go2 gesture qualification table, short supervised trial evidence, and a replay/log review identifying recognition errors and command-response differences.

See [the Go2 hardware guide](../GO2_HARDWARE.md) for setup and operating steps and
[COURSE_PLAN.md](../../COURSE_PLAN.md) for the course sequence. Hardware progress
depends on demonstrated readiness, not merely reaching the scheduled week.

## Completion checkpoint

Submit a gesture table with operator/lighting conditions, correct and incorrect recognitions, and supervised one-axis motion/stop observations. Include a short saved recording and replay check. Instructor approval is required before maze trials.

Keep the existing team-branch and weekly submission procedure. Do not include
AES/Wi-Fi credentials or raw recording ZIPs in public Git history.

Previous: [Week 8](../week-08-safety-testing/README.md). Next: [Week 10](../week-10-ros-hardware-readiness/README.md).

## Weekly submission

Submit your individual `week-09/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
