# Week 1: Run the Go1 simulation on Windows 11

## Milestone

Set up the course software and command a simulated Unitree Go1 with the keyboard.

## Learning objectives

By the end of this week, you should be able to:

- explain what MuJoCo, ONNX, Python, and a Conda environment do;
- activate a Conda environment and run a Python program;
- verify that a pretrained policy produces 12 Go1 joint actions; and
- start, command, stop, and reset the simulated robot.

## Before you begin

You need a Windows 11 laptop, internet access, and enough permission to install
user-level software. Install:

1. [Git for Windows](https://git-scm.com/download/win)
2. [Miniconda for Windows](https://docs.conda.io/projects/miniconda/en/latest/)

Open **Miniconda Prompt** from the Windows Start menu. Use it for every command
in this task sheet.

> [!NOTE]
> A Conda environment is an isolated Python installation for one project. MuJoCo
> is the physics simulator. ONNX is the format of the trained neural-network
> policy that chooses the robot's 12 joint actions.

## Task 1: Verify Git and Conda

```powershell
git --version
conda --version
```

Both commands should print version numbers. If either is not recognized, stop
and ask for help before continuing.

## Task 2: Get the course repository

New students can clone the course branch over HTTPS:

```powershell
cd $HOME\Downloads
git clone --branch creative-inquiry-dev https://github.com/sriram-2502/go1-mujoco-playground.git
cd .\go1-mujoco-playground
```

If the repository is already on your laptop:

```powershell
cd C:\path\to\go1-mujoco-playground
git switch creative-inquiry-dev
git pull
```

Replace `C:\path\to` with the actual location on your laptop.

Confirm that you are in the correct folder:

```powershell
git branch --show-current
Test-Path .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

Expected results are `creative-inquiry-dev` and `True`.

## Task 3: Create the Python environment

```powershell
conda create -n go1-mujoco-playground python=3.12 pip setuptools wheel -y
conda activate go1-mujoco-playground
python --version
```

The last command should report Python 3.12. You create this environment once,
but activate it whenever you open a new terminal for the course.

## Task 4: Install the software

Run these commands from the repository root:

```powershell
python -m pip install --upgrade pip
python -m pip install "orbax-checkpoint==0.11.22"
python -m pip install -e . onnxruntime
```

The first Orbax command avoids a Windows path-length problem in a newer release.
The installation may take several minutes.

Download the pinned robot-model assets:

```powershell
python -c "from mujoco_playground._src import mjx_env; mjx_env.ensure_menagerie_exists()"
```

## Task 5: Validate the ONNX policy

Confirm that the pretrained model exists:

```powershell
Test-Path .\mujoco_playground\experimental\sim2sim\onnx\go1_policy.onnx
```

Expected result: `True`.

Run one policy inference without opening the simulator:

```powershell
python -c "import numpy as np, onnxruntime as ort; s=ort.InferenceSession(r'.\mujoco_playground\experimental\sim2sim\onnx\go1_policy.onnx', providers=['CPUExecutionProvider']); y=s.run(['continuous_actions'], {'obs':np.zeros((1,48), dtype=np.float32)})[0]; print('Action shape:', y.shape); assert y.shape == (1,12); print('ONNX policy: OK')"
```

Expected output includes:

```text
Action shape: (1, 12)
ONNX policy: OK
```

The 48 values describe the robot and its command. The policy returns one action
for each of the 12 actuated joints.

## Task 6: Run the keyboard controller

```powershell
python .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

Click inside the MuJoCo window so it receives keyboard input.

| Key | Command |
|---|---|
| Up arrow | Increase forward speed |
| Down arrow | Increase backward speed |
| Left arrow | Turn left |
| Right arrow | Turn right |
| Enter | Stop motion |
| Backspace | Stop and reset the simulation |

Commands persist. Pressing an arrow repeatedly increases its command within the
controller limits. Press **Enter** to return every commanded velocity to zero.

## Task 7: Record evidence

Capture a screenshot or short recording that shows:

1. the Go1 viewer;
2. at least one forward command;
3. at least one turning command; and
4. the robot stopping after Enter is pressed.

Write three short notes: one thing that worked, one problem you encountered, and
how you addressed it.

## Completion checklist

- [ ] The `go1-mujoco-playground` environment activates.
- [ ] The ONNX test returns an action shape of `(1, 12)`.
- [ ] The MuJoCo viewer opens.
- [ ] The four arrow-key commands change the robot's motion.
- [ ] Enter stops the robot.
- [ ] Backspace resets the simulation.
- [ ] The required evidence and notes are complete.

## Troubleshooting

### `conda` is not recognized

Use **Miniconda Prompt**, not an uninitialized PowerShell terminal.

### `WinError 206` or a filename is too long

```powershell
python -m pip install "orbax-checkpoint==0.11.22"
python -m pip install -e . onnxruntime
```

### The viewer opens, but the keys do nothing

Click inside the viewer window to give it keyboard focus.

### Robot assets are missing

Check your internet connection and rerun:

```powershell
python -c "from mujoco_playground._src import mjx_env; mjx_env.ensure_menagerie_exists()"
```

## Daily startup

```powershell
conda activate go1-mujoco-playground
cd C:\path\to\go1-mujoco-playground
python .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

## Deliverables

- Completed checklist
- Screenshot or short recording
- Three troubleshooting/reflection notes

## Next week

Continue to [Week 2: Go1 controller behavior, control, and reinforcement
learning](../week-02-go1-controller/README.md).
