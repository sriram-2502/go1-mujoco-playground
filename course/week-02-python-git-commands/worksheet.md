# Week 2 worksheet: Read, measure, and modify

Name:  
Team: `team-alpha` / `team-bravo`  
Personal branch:  

## 1. Baseline data table

Run the unchanged controller. Record the command after one input and the
observed motion. Press Enter before each trial so the command starts at zero.
Repeat each trial three times when possible.

| Trial | Input | vx forward | vy lateral | yaw rate | Observed motion |
|---:|---|---:|---:|---:|---|
| 1 | Up | | | | |
| 2 | Up | | | | |
| 3 | Up | | | | |
| 1 | Left | | | | |
| 2 | Left | | | | |
| 3 | Left | | | | |
| 1 | Down | | | | |
| 2 | Down | | | | |
| 3 | Down | | | | |
| 1 | Right | | | | |
| 2 | Right | | | | |
| 3 | Right | | | | |
| 1 | Enter | | | | |

## 2. Controller code map

Write one sentence for each function:

- `__init__`: 
- `change_command`: 
- `get_observation`: 
- `control`: 
- `key_callback`: 

## 3. Control systems

In this Go1 setup:

- Reference command: 
- Feedback/measurement: 
- Controller: 
- Plant: 
- Actuator output: 

Why is this a feedback-control system?  

## 4. Reinforcement learning

Complete these statements:

- During policy training, the agent observes: 
- The policy chooses: 
- A reward could encourage: 
- The ONNX file used in the playground is: 
- The policy returns 12 values because: 

## 5. Required challenge: increase sensitivity

With instructor approval, change one command increment:

- Forward: `0.25` to `0.50`; or
- Turning: `0.50` to `1.00`.

Record the exact value you changed:  

Before running again, check the code diff and make sure you changed only the
matching `dvx` or `dwz` value inside `key_callback`.

| Trial | Input | New vx | New vy | New yaw | Observed motion |
|---:|---|---:|---:|---:|---|
| 1 | Same input as baseline | | | | |
| 2 | Same input as baseline | | | | |
| 3 | Same input as baseline | | | | |

What changed compared with the baseline?  

Was the robot easier or harder to control? Why?  

What did you observe about the first command after pressing the key?

Did the robot's visible motion change immediately, or after the command
accumulated over several key presses?

Restore the baseline value after the experiment:  

## 6. Optional simulation challenge: stability boundary

Only if the instructor approves, gradually increase one command value and find
the smallest value that produces visibly unstable behavior. Do not perform this
experiment on the physical robot.

| Parameter changed | Values tested | First unstable value | What happened? |
|---|---|---|---|
| | | | |

## 7. Next-interface design

Choose: joystick / gesture / voice

```text
[ input ] -> [ interpretation ] -> [ vx, vy, yaw ] -> [ safety check ] -> [ Go1 policy ]
```

What happens if the input stops updating?  

One benefit:  

One risk or tradeoff:  

## Evidence

- Screenshot or recording: 
- Commit: 
