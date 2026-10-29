# Week 8: Stationary Go2 communication checkout

## Hardware path

This course now uses **Unitree Go2 + Windows 11 + Wi-Fi/WebRTC** for physical
navigation. The Go2's onboard camera supplies robot FPV; the Windows webcam
supplies MediaPipe hands. No laptop ROS installation or external Jetson/ZED stack
is required. This folder retains its historical name to preserve existing links.

The simulation code and the Weeks 1–6 simulation exercises are unchanged. Use the separate instructor-provided
Go2 application; the simulation launcher does not connect to the physical robot.

## Prerequisites

- Week 6 webcam/overview/FPV simulation checkpoint with logs.
- Instructor-approved robot assignment, hardware checkout, and operating procedure.
- Direct instructor supervision and the paired remote for physical motion.

## Learning objective

Distinguish live feedback, requested commands, and verified physical behavior.

## Activities

1. Complete the [stationary checklist](../GO2_HARDWARE.md#stationary-checkout-before-any-motion) with the instructor.
2. Confirm changing live Go2 video, incoming telemetry, and voxel data when the onboard service is available.
3. Start the Python hand-tracking service and Clemson UI. Preview operator gestures with control disabled.
4. Distinguish requested, supervised, transmitted, and measured velocities; identify stale/unavailable data.
5. Review Stop, disconnect, browser-focus loss, input expiry, and the paired-remote intervention procedure. Record what has actually been verified; do not infer a qualified physical stop from a stationary screenshot.

## Expected evidence

A stationary checkout record with pass/fail/untested results, software/firmware versions, and the instructor-reviewed plan for short motion checks.

See [the Go2 hardware guide](../GO2_HARDWARE.md) for setup and operating steps and
[COURSE_PLAN.md](../../COURSE_PLAN.md) for the course sequence. Hardware progress
depends on demonstrated readiness, not merely reaching the scheduled week.

## Completion checkpoint

Submit a pass/fail/untested checklist for authentication, camera freshness, state feedback, available voxels, webcam preview, and the reviewed intervention procedure. Unavailable streams or an unqualified stop path must be resolved before motion.

Keep the existing team-branch and weekly submission procedure. Do not include
AES/Wi-Fi credentials or raw recording ZIPs in public Git history.

Previous: [Week 7](../week-07-gesture-simulation/README.md). Next: [Week 9](../week-09-system-evaluation/README.md).

## Weekly submission

Submit your individual `week-08/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
