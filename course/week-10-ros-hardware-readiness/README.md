# Week 10: ROS and hardware readiness

## Milestone

Demonstrate the intended ROS interfaces and safety supervision without enabling
physical robot motion, then complete an instructor safety review.

## Learning objectives

- Explain ROS nodes, topics, messages, publishers, and subscribers.
- Separate abstract gesture intent from Unitree hardware commands.
- Verify message timing, timeout, and stop behavior in a non-actuating mode.
- Prepare a controlled physical-test procedure with assigned team roles.

## Prerequisites

- Week 9 recommendation supports ROS integration
- Week 8 automated safety tests pass at the selected configuration
- Companion repository reviewed:
  [`DyCo-AI/go1_gesture_tracking`](https://github.com/DyCo-AI/go1_gesture_tracking)
- Instructor has provided the laboratory ROS workspace and network procedure

## Task 1: Review the distributed architecture

Document which computer owns each responsibility:

| Responsibility | Operator laptop | Go1 Jetson |
|---|:--:|:--:|
| Laptop-webcam gesture recognition | X | |
| Gesture validation and mapping | X | |
| ROS master | X | |
| Robot-view ZED camera | | X |
| Unitree high-level bridge | instructor-defined | instructor-defined |

Update this table to match the actual laboratory configuration.

## Task 2: Document interfaces

For every topic used, record name, message type, publisher, subscribers, rate,
units, coordinate frame, and stale-data behavior. Gesture recognition must
publish abstract intent; it must not directly publish a Unitree hardware command.

## Task 3: Build in a non-actuating workspace

Follow the companion repository and laboratory workspace instructions. Build and
source the ROS workspace. Keep hardware output disabled. Resolve dependency or
message-type errors before connecting to the robot network.

## Task 4: Exercise mock topics

Use recorded or synthetic messages to verify:

- topic names and message types;
- expected publish rates;
- timestamp handling;
- stop priority;
- timeout after publisher shutdown; and
- no output on the hardware command channel.

Save topic inspection output and a short message-flow log.

## Task 5: Write the physical-test plan

The plan must include:

1. test objective and pass/fail conditions;
2. approved command limits;
3. cleared test area and robot starting pose;
4. operator, software observer, safety observer, and instructor roles;
5. independent emergency-stop method;
6. communication-loss response;
7. incremental test sequence beginning with zero motion; and
8. abort criteria.

## Task 6: Instructor readiness review

Demonstrate the non-actuating interface and safety tests. The instructor records
approval, restrictions, required corrections, or a decision to remain in
simulation. No approval means no physical motion test.

## Completion checklist

- [ ] Computer responsibilities documented.
- [ ] ROS interface table is complete.
- [ ] Workspace builds and sources successfully.
- [ ] Mock topics pass timing and stop tests.
- [ ] Hardware command output remains disabled.
- [ ] Physical-test plan assigns roles and abort criteria.
- [ ] Instructor readiness decision recorded.

## Deliverables

- Architecture and ROS interface tables
- Build and mock-topic evidence
- Physical-test plan
- Instructor review record

## Next week

With explicit instructor approval, continue to [Week 11: Supervised Go1
integration](../week-11-supervised-go1/README.md). Otherwise, repeat the required
simulation or safety work.
