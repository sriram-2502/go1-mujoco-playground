# Week 10: Physical Go2 maze construction and navigation

## Hardware path

This course now uses **Unitree Go2 + Windows 11 + Wi-Fi/WebRTC** for physical
navigation. The Go2's onboard camera supplies robot FPV; the Windows webcam
supplies MediaPipe hands. No laptop ROS installation or external Jetson/ZED stack
is required. This folder retains its historical name to preserve existing links.

The simulation code and the Weeks 1–6 simulation exercises are unchanged. Use the separate [Go2 GitHub setup](https://github.com/sriram-2502/unitree-go2-setup); the simulation launcher does not connect to the physical robot.

## Prerequisites

- Week 6 webcam/overview/FPV simulation checkpoint with logs.
- Instructor-approved robot assignment, hardware checkout, and operating procedure.
- Direct instructor supervision and the paired remote for physical motion.

## Learning objective

Design a repeatable physical maze trial using the robot camera view.

## Activities

1. Build a modular maze with measured body/leg clearances and a clear instructor intervention route.
2. Use the Go2 onboard camera and the Clemson UI for the student driving view; the instructor retains direct sight and the paired remote.
3. Progress through a straight corridor, partial route, then the full maze after each stage is qualified.
4. Decide and document whether voxels are visible to the student and whether obstacle avoidance is ON or OFF. Keep conditions consistent across compared trials.
5. Use the overall Recording switch, save each run ZIP, and review trajectories, gestures, interruptions, and completion time offline.

## Expected evidence

An approved Go2 maze layout, measured clearances, recorded experimental conditions, and staged trial ZIPs with sanitized summaries.

See [the Go2 hardware guide](../GO2_HARDWARE.md) for setup and operating steps and
[COURSE_PLAN.md](../../COURSE_PLAN.md) for the course sequence. Hardware progress
depends on demonstrated readiness, not merely reaching the scheduled week.

## Completion checkpoint

Document maze layout, clearance, start/goal, robot speed settings, avoidance state, and intervention rules. Complete an instructor-approved trial with students using robot FPV and the instructor maintaining direct visual supervision; report any intervention or incomplete trial.

Keep the existing team-branch and weekly submission procedure. Do not include
AES/Wi-Fi credentials or raw recording ZIPs in public Git history.

Previous: [Week 9](../week-09-system-evaluation/README.md). Next: [Week 11](../week-11-supervised-go1/README.md).

## Weekly submission

Submit your individual `week-10/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
