# Week 1 Windows 11 setup

Complete this setup before running the Go1 MuJoCo baseline. Use a Windows 11
computer and install software for your own user account unless your instructor
or lab administrator says otherwise.

## 1. Install Git for Windows

1. Download Git for Windows from <https://git-scm.com/install/windows>.
2. Run the installer.
3. The recommended default options are appropriate for this course.
4. When asked how Git should be used from the command line, keep the option that
   allows Git to work from Git Bash, Command Prompt, and other programs.
5. Finish the installation and open **Git Bash** or **Miniconda Prompt**.

Verify Git:

```powershell
git --version
```

A version number should appear. If Windows says that `git` is not recognized,
close and reopen the terminal. If it still fails, ask the instructor.

## 2. Install Visual Studio Code

Download and install [Visual Studio Code](https://code.visualstudio.com/download)
for Windows. The default installer choices are appropriate for this course.

During installation, enable these options if they are offered:

- Add `Open with Code` to the Windows Explorer context menu.
- Register Code as an editor for supported file types.
- Add VS Code to the PATH.

Open VS Code once after installation and install these extensions from the
Extensions panel:

| Extension | Publisher | Why we use it |
|---|---|---|
| Python | Microsoft | Run and debug Python programs |
| Pylance | Microsoft | Python code completion and type information |
| Markdown All in One | Yu Zhang | Write and preview weekly summaries |
| YAML | Red Hat | Read configuration files later in the course |

The **Git Graph** extension is optional. Git commands in the worksheet remain
the primary way to learn the workflow.

To open the repository in VS Code later:

```powershell
code .
```

If the `code` command is not recognized, open VS Code from the Start menu and
choose **File → Open Folder** instead.

## 3. Install Miniconda

1. Download the **Miniconda Windows 64-bit graphical installer** from
   <https://docs.anaconda.com/miniconda/install/>.
2. Choose **Just Me** unless your computer administrator requires another choice.
3. Keep the default installation location unless you have a reason to change it.
4. Do not add Miniconda to the system PATH when the installer asks.
5. Allow the installer to create the Miniconda Prompt entry.
6. Open **Miniconda Prompt** from the Windows Start menu.

Verify Conda:

```powershell
conda --version
```

A version number should appear. Use Miniconda Prompt for the remaining course
commands. Do not install the full Anaconda distribution for this course.

## 4. Create the course environment

Run this once:

```powershell
conda create -n go1-mujoco-playground python=3.12 pip setuptools wheel -y
```

Activate it:

```powershell
conda activate go1-mujoco-playground
python --version
```

The Python version should begin with `3.12`. You must activate this environment
whenever you open a new terminal for the course.

## 5. Get the course code

```powershell
cd $HOME\Downloads
git clone https://github.com/sriram-2502/go1-mujoco-playground.git
cd .\go1-mujoco-playground
git fetch origin
git switch main
git pull --ff-only origin main
```

Then follow the [Week 1 Git Worksheet](git-worksheet.md) to enter
`team-alpha` or `team-bravo`.

## 6. Install the MuJoCo course dependencies

From the repository root, with `go1-mujoco-playground` active:

```powershell
python -m pip install --upgrade pip
python -m pip install "orbax-checkpoint==0.11.22"
python -m pip install -e . onnxruntime
python -c "from mujoco_playground._src import mjx_env; mjx_env.ensure_menagerie_exists()"
```

The commands install the Python package, CPU ONNX Runtime, and the pinned robot
model assets used by the baseline.

## 7. Verify the baseline files

```powershell
Test-Path .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
Test-Path .\mujoco_playground\experimental\sim2sim\onnx\go1_policy.onnx
```

Both commands should return `True`.

## Common Windows notes

- `conda` not recognized: open **Miniconda Prompt**, not a new uninitialized shell.
- `git` not recognized: close and reopen the terminal after installing Git.
- Windows Defender or an administrator prompt: follow your lab's computer policy.
- This setup runs CPU inference and does not require CUDA or an NVIDIA GPU.

