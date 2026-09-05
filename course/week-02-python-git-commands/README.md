# Week 2: Read, measure, and modify the Go1 controller

## Milestone

Trace a keyboard press through the Python controller, connect the code to basic
control and reinforcement-learning ideas, make one controlled change, and
measure the result.

## Learning objectives

- Recognize variables, functions, classes, conditionals, and arrays in Python.
- Explain the three command values: forward, lateral, and yaw velocity.
- Explain the difference between a high-level command, a controller, an
  observation, and an actuator action.
- Describe at a high level how the ONNX locomotion policy was developed with
  reinforcement learning.
- Create a personal work branch from the assigned team branch and inspect a
  code change.
- Change one controller parameter and test its effect in simulation.

## Prerequisites

- Week 1 checklist completed
- Go1 simulator runs from the `go1-mujoco-playground` Conda environment
- A text editor such as Visual Studio Code installed

## Task 1: Prepare your workspace

```powershell
conda activate go1-mujoco-playground
cd C:\path\to\go1-mujoco-playground
git fetch origin
git switch --track origin/team-alpha
git pull --ff-only
git status
```

Team Bravo should use `origin/team-bravo` instead. Create a personal work branch
from your assigned team branch. Replace `YOUR-NAME` with a short lowercase name:

```powershell
git switch -c week-02/YOUR-NAME
```

Do not push directly to `main` or to the shared team branch while experimenting.
Ask the instructor before pushing an approved code change.

## Task 2: Establish a baseline

Run the unmodified controller. Record the printed command and observed motion
in the [Week 2 worksheet](worksheet.md). Repeat the important trials so you can
compare baseline and modified behavior.

```powershell
python .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

| Input | Forward | Lateral | Yaw |
|---|---:|---:|---:|
| Up | | | |
| Down | | | |
| Left | | | |
| Right | | | |
| Enter | | | |

Press **Enter** before each trial so the command starts at zero. One Up-arrow
press should add `0.25` to forward velocity (`vx`), and one Left-arrow press
should add `0.50` to yaw rate. The command persists until another command or
Enter is pressed.

## Task 3: Read the controller

Open
`mujoco_playground/experimental/sim2sim/play_go1_keyboard.py` and find:

1. `KeyboardController.__init__`, where controller state is initialized;
2. `change_command`, where commands are added and limited;
3. `get_observation`, where robot measurements and commands become policy input;
4. `control`, where the ONNX policy produces joint actions; and
5. `key_callback`, where key codes are mapped to command changes.

In your own words, write one sentence explaining each item. Then complete the
[Week 2 worksheet](worksheet.md), including the control-systems and
reinforcement-learning questions.

### Find the code you will change

Open this file in VS Code:

```text
mujoco_playground/experimental/sim2sim/play_go1_keyboard.py
```

For the required experiment, edit only the four command-increment values inside
`key_callback`:

```python
if keycode == glfw.KEY_UP:
  controller.change_command(dvx=0.25)
elif keycode == glfw.KEY_DOWN:
  controller.change_command(dvx=-0.25)
elif keycode == glfw.KEY_LEFT:
  controller.change_command(dwz=0.50)
elif keycode == glfw.KEY_RIGHT:
  controller.change_command(dwz=-0.50)
```

Do not edit `action_scale`, the ONNX model, the observation vector, the MuJoCo
XML, or the command limits for the required experiment.

### Control-systems connection

The keyboard does not directly command individual motors. It produces a desired
body velocity. The pretrained locomotion policy uses that desired velocity plus
robot measurements to produce joint actions. In control language, the desired
velocity is a reference, the measured robot state is feedback, the policy is the
controller, and the simulated robot is the plant.

### Reinforcement-learning connection

The ONNX file is a frozen neural-network policy trained before this course. In
training, an agent observes the simulated robot state, chooses joint actions,
receives rewards for stable motion and command tracking, and repeats this over
many simulated episodes. In this course, students use the trained policy; they
are not retraining it. Week 2 focuses on understanding its inputs and outputs.

## Task 4: Required challenge - increase sensitivity

Choose **one** instructor-approved change:

- increase the forward increment from `0.25` to `0.50`; or
- increase the yaw increment from `0.50` to `1.00`.

Change only the matching argument in `key_callback`. Save the file, rerun the
simulator, and complete the before/after data tables in the worksheet. Use the
same input and number of trials as the baseline. Press Enter between trials.
The first Up press should now be approximately `+0.50`, or the first Left press
approximately `+1.00`. Observe whether motion becomes faster, sharper, harder
to stop, or harder to align. Restore the original value after recording results.

## Task 5: Inspect and record the change

```powershell
git diff
git status
```

Check that the diff contains only the intended edit. Then record it:

```powershell
git add .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
git commit -m "Adjust keyboard command increment"
```

Follow the instructor's directions before pushing a student branch to GitHub.

Your diff should normally show only one changed number. If it shows changes to
the policy, action scaling, robot model, or other files, stop and ask the
instructor before continuing.

## Task 6: Optional stability challenge

With instructor approval, gradually increase one command value until the
simulated robot becomes visibly unstable. Start from the original value, test
one value at a time, and use Enter to reset between tests. Record the smallest
value that causes instability and describe what happened. This is
simulation-only: never try to make the physical robot fall.

## Task 7: End-of-session design challenge

Use your measurements to design the next input interface. Choose a joystick,
gesture, or voice command interface and specify:

1. what its input values are;
2. how those values become `vx`, `vy`, and `yaw`; and
3. what should happen when the input stops updating.

Draw the design as a five-box block diagram and write one tradeoff. This is a
design exercise only; do not implement the new interface yet.

## Engineering questions

1. Why does a smaller increment make the robot easier or harder to command?
2. What is the difference between command increment and command limit?
3. Why should one experiment change only one value at a time?
4. What happens to the command when Enter is pressed?
5. What are the reference, feedback signal, controller, and plant here?
6. What does the RL policy receive as input, and what does it return?
7. Why can a policy trained in simulation still require safety limits at runtime?

## Completion checklist

- [ ] Baseline command table completed.
- [ ] Five controller sections identified and explained.
- [ ] Only one approved command increment changed.
- [ ] Modified behavior measured in simulation.
- [ ] `git diff` reviewed before committing.
- [ ] Engineering questions answered.
- [ ] Before/after data table completed.
- [ ] Original parameter restored.
- [ ] Five-box input-interface design completed.

## Deliverables

- Baseline and modified command tables
- Five-sentence controller explanation
- Git commit identifier from `git log -1 --oneline`
- Answers to the engineering questions
- Before/after sensitivity data table
- Five-box input-interface design

## Next week

Continue to [Week 3: Webcam image acquisition](../week-03-webcam-basics/README.md).
