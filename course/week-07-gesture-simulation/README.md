# Week 7: Go2 hardware inventory and Windows setup

## Hardware path

This course now uses **Unitree Go2 + Windows 11 + Wi-Fi/WebRTC** for physical
navigation. The Go2's onboard camera supplies robot FPV. The Windows webcam
supplies MediaPipe hands in later gesture exercises; this week's stationary Basic
UI checkout does not run hand tracking. No laptop ROS installation or external
Jetson/ZED stack is required. This folder retains its historical name to preserve existing links.

The simulation code and the Weeks 1–6 simulation exercises are unchanged. Use the separate [Clemson DyCo-AI Go2 WebRTC starter](https://github.com/DyCo-AI/go2-webRTC) for this week's Basic UI checkout; the simulation launcher does not connect to the physical robot. This starter keeps the Week 7 setup focused on Windows and WebRTC.

## Prerequisites

- Week 6 webcam/overview/FPV simulation checkpoint with logs.
- Instructor-approved robot assignment, hardware checkout, and operating procedure.
- Direct instructor supervision and the paired remote for physical motion.

## Learning objective

Explain the roles of the Windows webcam, Go2 camera, browser, and onboard controller.

## Activities

1. Read the Clemson starter's [Windows setup guide](https://github.com/DyCo-AI/go2-webRTC/blob/main/docs/SETUP.md). Use [the course hardware guide](../GO2_HARDWARE.md) for the two-camera explanation and body-frame coordinate convention; its later Clemson gesture-panel instructions are a separate extension.
2. Clone [`DyCo-AI/go2-webRTC`](https://github.com/DyCo-AI/go2-webRTC) and follow its Basic dashboard commands; obtain the robot assignment, Wi-Fi credentials, and private AES key from the instructor.
3. Prepare the starter's local Node runtime while internet is available. The Basic browser UI does not need Conda or MediaPipe. If the instructor assigns the separate [Python examples](https://github.com/DyCo-AI/go2-webRTC/blob/main/docs/PYTHON.md), prepare `go2wifi` using that starter's root `requirements.txt`; disconnect the browser before using Python as a robot client.
4. Close other robot clients, join the assigned Go2 hotspot, and check the default endpoint `192.168.12.1`.
5. Open the Basic WebRTC UI with the instructor and inspect connection/camera/status without commanding locomotion.

## Expected evidence

A system diagram, environment/version notes, sanitized stationary connection evidence, and an explanation of which camera sees the operator versus the maze.

See the [Clemson Windows setup guide](https://github.com/DyCo-AI/go2-webRTC/blob/main/docs/SETUP.md) for this week's installation and Basic UI steps and
[COURSE_PLAN.md](../../COURSE_PLAN.md) for the course sequence. MediaPipe and the
Clemson gesture dashboard are not part of this starter's Week 7 setup. Hardware progress
depends on demonstrated readiness, not merely reaching the scheduled week.

## Completion checkpoint

Show the instructor the separate starter checkout, Basic UI connection, and live robot view. Record the setup Git commit and endpoint. This week does not require locomotion; keep keys out of evidence.

Keep the existing team-branch and weekly submission procedure. Do not include
AES/Wi-Fi credentials or raw recording ZIPs in public Git history.

Previous: [Week 6](../week-06-mock-command-mapping/README.md). Next: [Week 8](../week-08-safety-testing/README.md).

## Weekly submission

Submit your individual `week-07/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
