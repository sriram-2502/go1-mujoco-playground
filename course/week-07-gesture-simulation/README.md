# Week 7: Go2 hardware inventory and Windows setup

## Hardware path

Use the **same personal [Go2 gesture UI](https://github.com/sriram-2502/go2-gesture-nav)**
for this and later hardware weeks. It runs on Windows 11 without ROS. There is
no separate Basic starter to clone and no `webrtc/` folder to navigate.
This folder keeps its historical name so existing course links work.

The Go1 simulation and Weeks 1–6 remain unchanged. The simulation launcher does
not connect to the physical Go2.

## Prerequisites

- Week 6 simulation checkpoint and individual report.
- Instructor-approved robot assignment, operating procedure, and paired remote.

## Learning objective

Explain the roles of the laptop webcam, Go2 camera, browser, and onboard walking
controller; prepare one reproducible hardware application.

## Activities

1. Follow the personal repo's [install-once quick start](https://github.com/sriram-2502/go2-gesture-nav#1-install-once) while internet is available.
2. Use root `requirements.txt` and `setup-ui.ps1`; run `python -m gesture_preview.server` and root `start-ui.ps1` in separate terminals.
3. Open port **5174** and preview the hand skeleton with movement disabled.
4. With the instructor, join the assigned Go2 hotspot, use the private key and default endpoint `192.168.12.1`, and complete [stationary checks](../GO2_HARDWARE.md#stationary-checkout-before-any-motion).
5. Record the Git commit/UI build ID and distinguish the Windows hand camera from the robot-view camera. Locate Stop, battery, Jump once, and Bound gait without activating optional behaviors.

## Completion checkpoint

Show installation, preview, authenticated connection, live robot view, and fresh
state while stationary. This week requires **no locomotion**. Keep credentials
out of screenshots and reports. Later weeks use the same checkout and launchers.

Follow [the course hardware guide](../GO2_HARDWARE.md) and
[COURSE_PLAN.md](../../COURSE_PLAN.md). Progress depends on readiness and instructor
approval, not merely reaching the scheduled week.

Previous: [Week 6](../week-06-mock-command-mapping/README.md).
Next: [Week 8](../week-08-safety-testing/README.md).

## Weekly submission

Submit your individual `week-07/README.md` in your student folder on the assigned
team branch. Code experiments and full run data stay local. Optional small media
and the final report follow [the submission/data policy](../SUBMISSIONS.md).
