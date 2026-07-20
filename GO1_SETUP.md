
# MuJoCo Playground Go1: Local Setup, Keyboard Controller, and Training

This guide sets up Google DeepMind's MuJoCo Playground on Ubuntu 22.04 with an NVIDIA RTX 2070. It covers:

- installing the source checkout and CUDA-enabled JAX;
- running the bundled pretrained Go1 ONNX policy with the keyboard;
- running a short PPO training smoke test;
- training, saving, resuming, and playing back native Brax checkpoints.

The paths below assume the Linux username is `sriramk` and the repository will be located at:

```text
/home/sriramk/go1_playground/mujoco_playground
```

## 1. System prerequisites

Verify that Ubuntu can see the GPU:

```bash
nvidia-smi
```

For JAX CUDA 12 wheels on Linux, use an NVIDIA driver version of at least 525. A separate system CUDA Toolkit is not required because JAX can install its CUDA runtime libraries through Python packages.

If the NVIDIA driver is missing:

```bash
sudo ubuntu-drivers autoinstall
sudo reboot
```

Install the required Ubuntu packages:

```bash
sudo apt update
sudo apt install -y \
  git build-essential ffmpeg patchelf \
  libgl1 libegl1 libglfw3 libglfw3-dev \
  libglew-dev libosmesa6-dev
```

## 2. Clone MuJoCo Playground

Skip the clone command if the repository already exists.

```bash
mkdir -p /home/sriramk/go1_playground
cd /home/sriramk/go1_playground
git clone https://github.com/google-deepmind/mujoco_playground.git
cd /home/sriramk/go1_playground/mujoco_playground
```

Record the source revision for reproducibility:

```bash
git rev-parse HEAD
```

Official repository: [https://github.com/google-deepmind/mujoco_playground](https://github.com/google-deepmind/mujoco_playground)

## 3. Create the Conda environment

MuJoCo Playground requires Python 3.11 or newer. Python 3.12 is recommended for this setup.

```bash
conda create -n go1-playground python=3.12 -y
conda activate go1-playground
python -m pip install --upgrade pip setuptools wheel
```

All subsequent commands assume `go1-playground` is active.

## 4. Install CUDA-enabled JAX

Remove an inherited CUDA library override before installing and testing JAX:

```bash
unset LD_LIBRARY_PATH
python -m pip install --upgrade "jax[cuda12]"
```

Verify GPU execution:

```bash
python - <<'PY'
import jax

print("JAX version:", jax.__version__)
print("Backend:", jax.default_backend())
print("Devices:", jax.devices())
assert jax.default_backend() == "gpu"
PY
```

Expected output includes:

```text
Backend: gpu
Devices: [CudaDevice(id=0)]
```

Do not continue to GPU training if the backend is `cpu`.

## 5. Install MuJoCo Playground and runtime dependencies

From the repository root:

```bash
cd /home/sriramk/go1_playground/mujoco_playground
python -m pip install -e ".[notebooks,learning]"
python -m pip install onnxruntime
```

The keyboard controller does not require `hidapi`. That dependency is only needed by the original Logitech F710 gamepad program.

### Warp compatibility for MuJoCo/MJX 3.10.0

If the installed versions are MuJoCo/MJX 3.10.0, keep Warp on 1.12.1:

```bash
python -m pip install "warp-lang==1.12.1"
```

This avoids the following incompatibility caused by newer Warp releases removing a private API expected by MuJoCo/MJX 3.10.0:

```text
AttributeError: type object 'int' has no attribute 'WARP'
```

Confirm the important versions:

```bash
python -m pip show jax jaxlib mujoco mujoco-mjx warp-lang playground
```

## 6. Verify the Go1 environment

```bash
export XLA_PYTHON_CLIENT_PREALLOCATE=false

python - <<'PY'
import jax
from mujoco_playground import registry

env = registry.load("Go1JoystickFlatTerrain")

print("Backend:", jax.default_backend())
print("Environment:", type(env).__name__)
print("Action size:", env.action_size)
print("Control timestep:", env.dt)
PY
```

The first run downloads the pinned MuJoCo Menagerie assets. Important expected values are:

```text
Backend: gpu
Action size: 12
Control timestep: 0.02
```

## 7. Checkpoint formats

MuJoCo Playground uses two different policy formats in this workflow:

| Format                    | Location                                                        | Purpose                                                       | Can resume PPO training? |
| ------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------ |
| Bundled ONNX policy       | `mujoco_playground/experimental/sim2sim/onnx/go1_policy.onnx` | Ready-to-run Go1 inference in native MuJoCo                   | No                       |
| Brax checkpoint directory | Created under a training run's`checkpoints/<step>/` directory | JAX/Brax policy restoration, playback, and continued training | Yes                      |

Do not pass `go1_policy.onnx` to `--load_checkpoint_path`. The training program expects a native Brax checkpoint directory, not an ONNX file.

## 8. Run the pretrained Go1 keyboard controller

The custom keyboard runner is:

```text
mujoco_playground/experimental/sim2sim/play_go1_keyboard.py
```

It loads the bundled pretrained policy:

```text
mujoco_playground/experimental/sim2sim/onnx/go1_policy.onnx
```

Run it from the repository root:

```bash
conda activate go1-playground
cd /home/sriramk/go1_playground/mujoco_playground
python mujoco_playground/experimental/sim2sim/play_go1_keyboard.py
```

Click inside the MuJoCo window to give it keyboard focus.

### Keyboard controls

| Key         | Action                                |
| ----------- | ------------------------------------- |
| Up arrow    | Increase forward velocity by 0.25 m/s |
| Down arrow  | Decrease forward velocity by 0.25 m/s |
| Left arrow  | Increase left-yaw command             |
| Right arrow | Increase right-yaw command            |
| Enter       | Set all velocity commands to zero     |
| Backspace   | Stop and reset the simulation         |

Commands persist after a key press. Press the same arrow repeatedly to increase its command, and press Enter to stop. The controller clamps commands to the ranges used during training.

This runner uses ONNX Runtime's CPU execution provider for policy inference and native MuJoCo for simulation. It demonstrates the supplied policy but does not test PPO training or checkpoint creation.

## 9. Validate the bundled ONNX checkpoint without the viewer

This test verifies that the policy file loads and produces 12 Go1 joint actions:

```bash
cd /home/sriramk/go1_playground/mujoco_playground

python - <<'PY'
from pathlib import Path

import numpy as np
import onnxruntime as ort

policy_path = Path(
    "mujoco_playground/experimental/sim2sim/onnx/go1_policy.onnx"
)
session = ort.InferenceSession(
    policy_path.as_posix(),
    providers=["CPUExecutionProvider"],
)

observation = np.zeros((1, 48), dtype=np.float32)
action = session.run(
    ["continuous_actions"],
    {"obs": observation},
)[0]

print("Input:", [(x.name, x.shape) for x in session.get_inputs()])
print("Output:", [(x.name, x.shape) for x in session.get_outputs()])
print("Action shape:", action.shape)
assert action.shape == (1, 12)
print("Bundled Go1 ONNX policy: OK")
PY
```

# Training the Go1 controller

Training uses `learning/train_jax_ppo.py`. It automatically:

- loads the environment and tuned Go1 PPO configuration;
- trains and evaluates the policy;
- creates timestamped log and checkpoint directories;
- restores compatible Brax checkpoints when requested;
- renders an MP4 rollout after training.

The official Go1 configuration targets substantially larger GPUs. Start with memory-safe values on an 8 GB RTX 2070.

## 10. PPO smoke test

The smoke test confirms JAX compilation, Warp simulation, PPO updates, evaluation, checkpoint saving, and video rendering. It is too short to learn a polished walking policy.

```bash
conda activate go1-playground
cd /home/sriramk/go1_playground/mujoco_playground

python learning/train_jax_ppo.py \
  --env_name=Go1JoystickFlatTerrain \
  --impl=warp \
  --num_timesteps=100000 \
  --num_evals=2 \
  --num_envs=256 \
  --num_eval_envs=1 \
  --batch_size=256 \
  --num_minibatches=1 \
  --num_videos=1 \
  --suffix=rtx2070-smoke \
  --logdir=/home/sriramk/go1_playground/runs
```

In a second terminal, monitor GPU utilization and memory:

```bash
watch -n 1 nvidia-smi
```

The first JAX/Warp compilation can take considerably longer than later iterations.

## 11. Training output

Each execution creates a timestamped experiment directory similar to:

```text
/home/sriramk/go1_playground/runs/
└── Go1JoystickFlatTerrain-YYYYMMDD-HHMMSS-rtx2070-smoke/
    ├── checkpoints/
    │   ├── config.json
    │   └── <training-step>/
    └── rollout0.mp4
```

Keep the entire checkpoint directory. The parameters, observation normalizer, value network, and network configuration must remain compatible when restoring.

## 12. Longer training run

After the smoke test succeeds, start with 10 million environment steps and domain randomization:

```bash
python learning/train_jax_ppo.py \
  --env_name=Go1JoystickFlatTerrain \
  --impl=warp \
  --num_timesteps=10000000 \
  --num_evals=10 \
  --num_envs=256 \
  --num_eval_envs=1 \
  --batch_size=256 \
  --num_minibatches=1 \
  --domain_randomization \
  --num_videos=1 \
  --suffix=rtx2070-baseline \
  --logdir=/home/sriramk/go1_playground/runs
```

Ten million steps is a practical first learning run, not the full official Go1 baseline. The tuned source configuration uses 200 million steps and 8192 parallel environments, which is intended for much larger GPUs.

If 256 environments are stable, test 512 environments while preserving the PPO divisibility requirement:

```text
num_envs = 512
batch_size = 256
num_minibatches = 2
```

The command-line flags are:

```bash
--num_envs=512 --batch_size=256 --num_minibatches=2
```

`batch_size * num_minibatches` must be divisible by `num_envs`.

## 13. Resume training from a Brax checkpoint

Set `CHECKPOINTS` to the absolute `checkpoints` directory from the previous run. The trainer automatically selects its latest numeric step directory.

Example:

```bash
python learning/train_jax_ppo.py \
  --env_name=Go1JoystickFlatTerrain \
  --impl=warp \
  --load_checkpoint_path=/home/sriramk/go1_playground/runs/EXPERIMENT/checkpoints \
  --num_timesteps=10000000 \
  --num_evals=10 \
  --num_envs=256 \
  --num_eval_envs=1 \
  --batch_size=256 \
  --num_minibatches=1 \
  --domain_randomization \
  --num_videos=1 \
  --suffix=rtx2070-resumed \
  --logdir=/home/sriramk/go1_playground/runs
```

Replace `EXPERIMENT` with the actual timestamped directory name. Keep the environment name, observation keys, and policy/value network architecture consistent with the checkpoint.

## 14. Render a trained Brax checkpoint without additional training

```bash
python learning/train_jax_ppo.py \
  --env_name=Go1JoystickFlatTerrain \
  --impl=warp \
  --play_only \
  --load_checkpoint_path=/home/sriramk/go1_playground/runs/EXPERIMENT/checkpoints \
  --num_envs=1 \
  --num_eval_envs=1 \
  --batch_size=1 \
  --num_minibatches=1 \
  --num_videos=1 \
  --suffix=playback \
  --logdir=/home/sriramk/go1_playground/playback
```

The rendered video is saved in a timestamped directory under `/home/sriramk/go1_playground/playback`.

## 15. RTX 2070 memory guidance

If training runs out of memory:

1. Stop the failed Python process.
2. Confirm memory was released with `nvidia-smi`.
3. Use 128 training environments:

```bash
--num_envs=128 --batch_size=128 --num_minibatches=1 --num_eval_envs=1
```

4. Avoid running Jupyter, another model, or another GPU simulation concurrently.
5. Keep `XLA_PYTHON_CLIENT_PREALLOCATE=false`.

The training script sets `XLA_PYTHON_CLIENT_PREALLOCATE=false` and `MUJOCO_GL=egl` internally.

## 16. Troubleshooting

### JAX reports a CPU backend

```bash
unset LD_LIBRARY_PATH
python -c "import jax; print(jax.default_backend()); print(jax.devices())"
nvidia-smi
python -m pip show jax jaxlib jax-cuda12-plugin jax-cuda12-pjrt
```

Reinstall the CUDA 12 build if necessary:

```bash
python -m pip install --upgrade --force-reinstall "jax[cuda12]"
```

### `GraphMode.WARP` or `type object 'int' has no attribute 'WARP'`

```bash
python -m pip install "warp-lang==1.12.1"
```

Then start a new Python process before retesting.

### `ModuleNotFoundError: No module named 'hid'`

The original `play_go1_joystick.py` imports the gamepad reader. Run the keyboard program instead:

```bash
python mujoco_playground/experimental/sim2sim/play_go1_keyboard.py
```

If the physical gamepad program is desired, install its dependency separately:

```bash
python -m pip install hidapi
```

### Viewer does not open

The interactive keyboard program requires a desktop display. Check:

```bash
echo "$DISPLAY"
```

Run it from the Ubuntu desktop session rather than a headless SSH terminal. Training can run with EGL without displaying a window.

### Menagerie asset download fails

Confirm internet access and retry:

```bash
python -c "from mujoco_playground import registry; registry.load('Go1JoystickFlatTerrain'); print('Go1 loaded')"
```

## 17. Daily startup

For pretrained keyboard control:

```bash
conda activate go1-playground
cd /home/sriramk/go1_playground/mujoco_playground
python mujoco_playground/experimental/sim2sim/play_go1_keyboard.py
```

For training:

```bash
conda activate go1-playground
cd /home/sriramk/go1_playground/mujoco_playground
export XLA_PYTHON_CLIENT_PREALLOCATE=false
```

Then run the smoke, baseline, resume, or playback command from the relevant section above.

# Windows 11: ONNX keyboard controller only

The bundled ONNX policy and native MuJoCo viewer can also run directly on Windows 11. This section is for inference and keyboard control only; it does not configure JAX GPU training.

MuJoCo publishes Windows Python wheels containing the native library and interactive viewer. The regular `onnxruntime` package provides CPU inference. The Go1 policy is small, so an NVIDIA GPU, CUDA Toolkit, and ONNX Runtime GPU package are unnecessary for this workflow.

## 18. Windows prerequisites

Install:

- Git for Windows: <https://git-scm.com/download/win>
- Miniconda: <https://docs.conda.io/projects/miniconda/en/latest/>

Open **Miniconda Prompt** or a PowerShell terminal in which Conda has been initialized.

Do not run the Ubuntu `apt` commands on Windows. Do not set `MUJOCO_GL=egl`, which is part of the Linux/headless configuration.

## 19. Clone the repository on Windows

In PowerShell:

```powershell
$Go1Root = Join-Path $env:USERPROFILE "go1_playground"
New-Item -ItemType Directory -Force -Path $Go1Root
Set-Location $Go1Root

git clone https://github.com/google-deepmind/mujoco_playground.git
Set-Location (Join-Path $Go1Root "mujoco_playground")
```

If the repository is already present, skip `git clone` and change into its existing directory.

Copy the custom keyboard runner into:

```text
mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

The official repository already supplies the pretrained policy at:

```text
mujoco_playground\experimental\sim2sim\onnx\go1_policy.onnx
```

## 20. Create the Windows Conda environment

```powershell
conda create -n go1-onnx python=3.12 -y
conda activate go1-onnx
python -m pip install --upgrade pip setuptools wheel
```

## 21. Install Playground and ONNX Runtime on Windows

From the repository root:

```powershell
python -m pip install -e .
python -m pip install onnxruntime
```

The editable Playground installation may install CPU JAX because Playground modules import JAX utilities. The keyboard controller itself uses ONNX Runtime for policy inference and does not need CUDA-enabled JAX.

For this ONNX-only workflow, do not install or configure:

- `jax[cuda12]`;
- the NVIDIA CUDA Toolkit;
- Linux EGL/OpenGL packages;
- the Warp pin used by the Linux GPU-training setup;
- `hidapi`, unless the original physical-gamepad program will also be used.

## 22. Download the pinned Menagerie assets on Windows

The keyboard runner accesses the Go1 model files directly, so explicitly download the pinned MuJoCo Menagerie checkout on a fresh installation:

```powershell
python -c "from mujoco_playground._src import mjx_env; mjx_env.ensure_menagerie_exists()"
```

Confirm that this directory now exists:

```text
mujoco_playground\external_deps\mujoco_menagerie\unitree_go1
```

## 23. Validate the bundled Go1 ONNX checkpoint on Windows

Check that the model exists:

```powershell
Test-Path .\mujoco_playground\experimental\sim2sim\onnx\go1_policy.onnx
```

Expected output:

```text
True
```

Run one inference call and confirm that the policy produces 12 joint actions:

```powershell
python -c "import numpy as np, onnxruntime as ort; s=ort.InferenceSession(r'.\mujoco_playground\experimental\sim2sim\onnx\go1_policy.onnx', providers=['CPUExecutionProvider']); y=s.run(['continuous_actions'], {'obs':np.zeros((1,48), dtype=np.float32)})[0]; print('Action shape:', y.shape); assert y.shape == (1,12)"
```

Expected output:

```text
Action shape: (1, 12)
```

## 24. Run the keyboard controller on Windows

```powershell
python .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

Click inside the MuJoCo viewer to give it keyboard focus.

| Key | Action |
|---|---|
| Up arrow | Increase forward velocity |
| Down arrow | Increase backward velocity |
| Left arrow | Turn left |
| Right arrow | Turn right |
| Enter | Stop |
| Backspace | Stop and reset the simulation |

The Windows runner uses the same `go1_policy.onnx` checkpoint as Ubuntu. It does not load a Brax checkpoint and cannot resume PPO training from the ONNX file.

## 25. Windows troubleshooting

### `play_go1_keyboard.py` is missing

The keyboard runner is a custom file and is not part of the original upstream checkout. Copy it into the expected `sim2sim` directory. The official upstream runner is gamepad-only.

### `ModuleNotFoundError: No module named 'onnxruntime'`

```powershell
conda activate go1-onnx
python -m pip install onnxruntime
```

### Menagerie mesh or XML file is missing

```powershell
python -c "from mujoco_playground._src import mjx_env; mjx_env.ensure_menagerie_exists()"
```

### Viewer window does not appear
