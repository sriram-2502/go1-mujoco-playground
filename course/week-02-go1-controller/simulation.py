"""Week 2: native MuJoCo adapter for the existing 48-input Go1 ONNX policy."""

from pathlib import Path
import xml.etree.ElementTree as ET

import mujoco
import numpy as np

from mujoco_playground._src.locomotion.go1.base import get_assets
from mujoco_playground.experimental.sim2sim.play_go1_keyboard import KeyboardController

SCENES = Path(__file__).parents[1] / "week-06-mock-command-mapping" / "scenes"


class Simulation:
  def __init__(self, scene="maze"):
    if scene not in ("arena", "corridor", "maze"):
      raise ValueError(f"Unknown scene: {scene}")
    assets = get_assets()
    assets.update({p.name: p.read_bytes() for p in SCENES.glob("*.xml")})
    robot = ET.fromstring(assets["go1_mjx_feetonly.xml"])
    # VFS assets use basenames. Preserve the original robot and its joint order.
    robot.find("compiler").set("meshdir", ".")
    for mesh in robot.findall(".//mesh"):
      if "file" in mesh.attrib:
        mesh.set("file", Path(mesh.get("file")).name)
    trunk = robot.find(".//body[@name='trunk']")
    ET.SubElement(trunk, "camera", name="robot_fpv", pos="0.28 0 0.10",
                  xyaxes="0 -1 0 0 0 1", fovy="85")
    assets["course_robot.xml"] = ET.tostring(robot)
    self.model = mujoco.MjModel.from_xml_string(
        (SCENES / f"{scene}.xml").read_text(), assets=assets)
    # Bit 1: original feet-floor contacts. Bit 2: all collision geoms vs walls.
    # This adds no robot self-collisions or new body-floor contacts.
    physical = self.model.geom_group == 3
    self.model.geom_conaffinity[physical] |= 2
    self.data = mujoco.MjData(self.model)
    self.controller = KeyboardController(
        np.array(self.model.keyframe("home").qpos[7:]), n_substeps=5)
    self.walls = {i for i in range(self.model.ngeom)
                  if (self.model.geom(i).name or "").startswith("wall_")}
    self.goal = self.model.site("goal").pos[:2].copy()
    self.goal_radius = self.model.site("goal").size[0]
    self.contacts = 0
    self.touching = False
    self.goal_reached = False
    self.overview_camera = mujoco.MjvCamera()
    self.overview_camera.lookat[:] = (2.4, 1.1, 0)
    self.overview_camera.distance = 8.8
    self.overview_camera.azimuth = 90
    self.overview_camera.elevation = -62
    self.reset()

  def reset(self):
    mujoco.mj_resetDataKeyframe(self.model, self.data, 0)
    self.controller.stop()
    self.controller.last_action[:] = 0
    self.controller.counter = 0
    self.contacts = 0
    self.touching = False
    self.goal_reached = False
    mujoco.mj_forward(self.model, self.data)

  def step(self, command):
    self.controller.command[:] = command
    self.controller.control(self.model, self.data)
    mujoco.mj_step(self.model, self.data)
    touching = any(
        int(c.geom1) in self.walls or int(c.geom2) in self.walls
        for c in self.data.contact)
    if touching and not self.touching:
      self.contacts += 1
    self.touching = touching
    self.goal_reached = bool(
        np.linalg.norm(self.data.qpos[:2] - self.goal) < self.goal_radius)

  def render(self, renderer, data=None):
    """Render an optional private snapshot, so graphics never holds up stepping."""
    data = self.data if data is None else data
    images = []
    for camera in (self.overview_camera, "robot_fpv"):
      renderer.update_scene(data, camera=camera)
      # Shadows/reflections are expensive on integrated/software OpenGL drivers.
      renderer.scene.flags[mujoco.mjtRndFlag.mjRND_SHADOW] = False
      renderer.scene.flags[mujoco.mjtRndFlag.mjRND_REFLECTION] = False
      images.append(renderer.render().copy())
    return tuple(images)
