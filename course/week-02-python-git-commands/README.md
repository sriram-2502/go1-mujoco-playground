# Week 2: Python, Git, and robot commands

## Milestone

Trace a keyboard press through the Python controller, make one controlled change,
and document it with Git.

## Learning objectives

- Recognize variables, functions, classes, conditionals, and arrays in Python.
- Explain the three command values: forward, lateral, and yaw velocity.
- Create a Git branch and inspect a code change.
- Change one controller parameter and test its effect in simulation.

## Prerequisites

- Week 1 checklist completed
- Go1 simulator runs from `go1-mujoco-playground`
- A text editor such as Visual Studio Code installed

## Task 1: Prepare your workspace

```powershell
conda activate go1-mujoco-playground
cd C:\path\to\go1-mujoco-playground
git switch creative-inquiry-dev
git pull
git status
```

Create a work branch. Replace `TEAM-NAME` with the name assigned by the
instructor, using lowercase letters and hyphens:

```powershell
git switch -c week-02/TEAM-NAME
```

## Task 2: Establish a baseline

Run the unmodified controller. Record the printed command after one press of
each arrow key and after Enter.

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

## Task 3: Read the controller

Open
`mujoco_playground/experimental/sim2sim/play_go1_keyboard.py` and find:

1. `KeyboardController.__init__`, where controller state is initialized;
2. `change_command`, where commands are added and limited;
3. `get_observation`, where robot measurements and commands become policy input;
4. `control`, where the ONNX policy produces joint actions; and
5. `key_callback`, where key codes are mapped to command changes.

In your own words, write one sentence explaining each item.

## Task 4: Make one measured change

Choose **one** instructor-approved change:

- reduce the forward increment from `0.25` to `0.10`; or
- reduce the yaw increment from `0.50` to `0.25`.

Change only the matching argument in `key_callback`. Save the file, rerun the
simulator, and repeat the measurement table. Do not increase the command limits.

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

## Engineering questions

1. Why does a smaller increment make the robot easier or harder to command?
2. What is the difference between command increment and command limit?
3. Why should one experiment change only one value at a time?
4. What happens to the command when Enter is pressed?

## Completion checklist

- [ ] Baseline command table completed.
- [ ] Five controller sections identified and explained.
- [ ] Only one approved command increment changed.
- [ ] Modified behavior measured in simulation.
- [ ] `git diff` reviewed before committing.
- [ ] Engineering questions answered.

## Deliverables

- Baseline and modified command tables
- Five-sentence controller explanation
- Git commit identifier from `git log -1 --oneline`
- Answers to the engineering questions

## Next week

Continue to [Week 3: Webcam image acquisition](../week-03-webcam-basics/README.md).
