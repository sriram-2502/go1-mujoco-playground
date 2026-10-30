# Week 11: Go2 reliability testing and final demonstration

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

Evaluate repeatability rather than selecting only the best demonstration.

## Activities

1. Run repeated supervised trials with the qualified Go2 profile and the same stated maze/avoidance conditions.
2. Measure completion time, contacts, resets/interventions, recognition errors, and observed stopping time/distance.
3. Use CSVs and replay to compare requested, transmitted, and measured motion. Treat a sent command as a request, not proof of execution.
4. Present the complete webcam → MediaPipe → gesture → supervised velocity → WebRTC → Go2 loop.
5. Explain differences from the Go1 simulation: locomotion controller, command limits, gesture vocabulary, video latency, and real stopping behavior.

## Expected evidence

Repeatable Go2 trials, a concise analysis, a final demonstration, and a team presentation supported by logs and limitations.

See [the Go2 hardware guide](../GO2_HARDWARE.md) for setup and operating steps and
[COURSE_PLAN.md](../../COURSE_PLAN.md) for the course sequence. Hardware progress
depends on demonstrated readiness, not merely reaching the scheduled week.

## Completion checkpoint

Report all attempted trials, completion time, contacts, recognition errors, and manual interventions under recorded conditions. Compare simulation and Go2 behavior while accounting for different gesture mappings and speeds. Include sanitized replay evidence and unresolved failures.

Keep the existing team-branch and weekly submission procedure. Do not include
AES/Wi-Fi credentials or raw recording ZIPs in public Git history.

Previous: [Week 10](../week-10-ros-hardware-readiness/README.md). Next: [Week 12](../week-12-final-demonstration/README.md).

## Weekly submission

Submit your individual `week-11/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
