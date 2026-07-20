"""Run the bundled Go1 ONNX policy using keyboard commands."""

import time

from etils import epath
import glfw
import mujoco
import mujoco.viewer
import numpy as np
import onnxruntime as rt

from mujoco_playground._src.locomotion.go1 import go1_constants
from mujoco_playground._src.locomotion.go1.base import get_assets


_HERE = epath.Path(__file__).parent
_POLICY_PATH = _HERE / "onnx" / "go1_policy.onnx"


class KeyboardController:
  def __init__(self, default_angles, n_substeps):
    self.command = np.zeros(3, dtype=np.float32)
    self.default_angles = default_angles
    self.last_action = np.zeros(12, dtype=np.float32)
    self.action_scale = 0.5
    self.n_substeps = n_substeps
    self.counter = 0

    self.session = rt.InferenceSession(
        _POLICY_PATH.as_posix(),
        providers=["CPUExecutionProvider"],
    )

  def change_command(self, dvx=0.0, dvy=0.0, dwz=0.0):
    self.command += np.array([dvx, dvy, dwz], dtype=np.float32)
    self.command[0] = np.clip(self.command[0], -1.5, 1.5)
    self.command[1] = np.clip(self.command[1], -0.8, 0.8)
    self.command[2] = np.clip(self.command[2], -2 * np.pi, 2 * np.pi)
    print(
        f"Command: forward={self.command[0]:+.2f}, "
        f"lateral={self.command[1]:+.2f}, "
        f"yaw={self.command[2]:+.2f}"
    )

  def stop(self):
    self.command[:] = 0.0
    print("Command: STOP")

  def get_observation(self, model, data):
    linvel = data.sensor("local_linvel").data
    gyro = data.sensor("gyro").data
    imu_xmat = data.site_xmat[model.site("imu").id].reshape(3, 3)
    gravity = imu_xmat.T @ np.array([0.0, 0.0, -1.0])
    joint_angles = data.qpos[7:] - self.default_angles
    joint_velocities = data.qvel[6:]

    observation = np.hstack([
        linvel,
        gyro,
        gravity,
        joint_angles,
        joint_velocities,
        self.last_action,
        self.command,
    ])
    return observation.astype(np.float32)

  def control(self, model, data):
    self.counter += 1
    if self.counter % self.n_substeps:
      return

    observation = self.get_observation(model, data)
    self.last_action = self.session.run(
        ["continuous_actions"],
        {"obs": observation.reshape(1, -1)},
    )[0][0]

    data.ctrl[:] = (
        self.last_action * self.action_scale + self.default_angles
    )


def main():
  model = mujoco.MjModel.from_xml_path(
      go1_constants.FEET_ONLY_ROUGH_TERRAIN_XML.as_posix(),
      assets=get_assets(),
  )
  data = mujoco.MjData(model)
  mujoco.mj_resetDataKeyframe(model, data, 0)

  model.opt.timestep = 0.004
  controller = KeyboardController(
      default_angles=np.array(model.keyframe("home").qpos[7:]),
      n_substeps=5,  # 0.02 control dt / 0.004 simulation dt
  )

  # Brighter camera-mounted headlight.
  model.vis.headlight.ambient[:] = [0.30, 0.30, 0.30]
  model.vis.headlight.diffuse[:] = [0.75, 0.75, 0.75]
  model.vis.headlight.specular[:] = [0.30, 0.30, 0.30]

  # Add ambient contribution to the model's directional light.
  if model.nlight:
    model.light_ambient[:] = [0.15, 0.15, 0.15]

  def key_callback(keycode):
    if keycode == glfw.KEY_UP:
      controller.change_command(dvx=0.25)
    elif keycode == glfw.KEY_DOWN:
      controller.change_command(dvx=-0.25)
    elif keycode == glfw.KEY_LEFT:
      controller.change_command(dwz=0.50)
    elif keycode == glfw.KEY_RIGHT:
      controller.change_command(dwz=-0.50)
    elif keycode in (glfw.KEY_ENTER, glfw.KEY_KP_ENTER):
      controller.stop()
    elif keycode == glfw.KEY_BACKSPACE:
      controller.stop()
      mujoco.mj_resetDataKeyframe(model, data, 0)
      mujoco.mj_forward(model, data)
      print("Simulation reset")

  print("""
Keyboard controls
-----------------
Up/Down    increase/decrease forward velocity
Left/Right turn left/right
Enter      stop
Backspace  reset robot
""")

  mujoco.set_mjcb_control(controller.control)

  try:
    with mujoco.viewer.launch_passive(
        model,
        data,
        key_callback=key_callback,
    ) as viewer:
      while viewer.is_running():
        start = time.monotonic()
        mujoco.mj_step(model, data)
        viewer.sync()

        remaining = model.opt.timestep - (time.monotonic() - start)
        if remaining > 0:
          time.sleep(remaining)
  finally:
    mujoco.set_mjcb_control(None)


if __name__ == "__main__":
  main()