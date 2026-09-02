# Week 11: Supervised Go1 integration

## Milestone

Perform a controlled, instructor-supervised checkout of the validated command
pipeline on the physical Unitree Go1.

> [!CAUTION]
> This task sheet does not authorize robot operation. Proceed only when the
> instructor has approved the Week 10 plan and is present. The instructor and
> laboratory procedures override this document.

## Learning objectives

- Apply a pre-run safety checklist and team communication protocol.
- Introduce hardware output through small, reversible test steps.
- Compare physical response with simulated expectations.
- Stop, diagnose, and document unexpected behavior.

## Required authorization

Before entering hardware mode, record:

- instructor approval and date;
- approved software commit;
- approved configuration and command limits;
- test location and boundary;
- assigned operator and safety observer; and
- independent emergency-stop method.

If any item is missing, remain in simulation.

## Task 1: Pre-run inspection

Under instructor direction, inspect robot pose, battery, cables, mounts, network,
test-area clearance, and emergency-stop access. Confirm that all team members
understand the verbal callouts for **arming**, **moving**, **stopping**, and
**abort**.

## Task 2: Re-run zero-output tests

Before hardware output is enabled:

1. start all nodes in non-actuating mode;
2. verify current gesture is stop or unknown;
3. verify current command is zero;
4. stop the gesture publisher and confirm timeout behavior; and
5. show that the safety observer can independently stop the system.

## Task 3: Enable hardware at zero command

The instructor enables the approved hardware path while the requested command
remains zero. Observe for unexpected motion, messages, or timing. Abort on any
discrepancy.

## Task 4: Perform incremental motion checks

Follow the approved sequence. A typical progression is:

1. stop only;
2. one short, minimum-magnitude forward request;
3. stop and inspect;
4. one short turn request;
5. stop and inspect; and
6. one selected failure/timeout check if approved.

Return to zero between every motion. Do not improvise gestures or command values.

## Task 5: Compare simulation and hardware

For each approved test, record expected response, observed response, stop time,
and any difference from MuJoCo. Differences are engineering data, not something
to tune around during an active hardware test.

## Task 6: Post-run review

Disable hardware output, return the robot to the instructor-approved safe state,
and archive logs. Conduct a team debrief before changing code. Classify every
issue by perception, validation, mapping, communication, control, or hardware.

## Immediate abort conditions

- unexpected direction or magnitude of motion;
- delayed or ineffective stop;
- stale or missing operator feedback;
- communication loss;
- person or object entering the test boundary;
- loose hardware, low battery, or abnormal sound; or
- instructor or safety observer calls abort.

## Completion checklist

- [ ] Written instructor approval recorded.
- [ ] Pre-run inspection and team callouts completed.
- [ ] Zero-output and timeout checks passed.
- [ ] Only approved incremental motions attempted.
- [ ] Zero command restored between motions.
- [ ] Simulation/hardware comparison recorded.
- [ ] Hardware output disabled and logs archived after the run.

## Deliverables

- Signed or instructor-recorded checkout
- Test log with approved command sequence
- Simulation-versus-hardware comparison
- Issue list and corrective-action plan

## Next week

Continue to [Week 12: Final demonstration and
communication](../week-12-final-demonstration/README.md).
