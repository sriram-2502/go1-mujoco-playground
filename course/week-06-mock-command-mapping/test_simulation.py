"""Physics/policy checks: python -m unittest discover -s course/week-06-mock-command-mapping."""

import unittest

import mujoco
import numpy as np

from course import safety, simulation


class SimulationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.sim = simulation.Simulation("maze")

  def setUp(self):
    self.sim.reset()

  def test_policy_moves_forward_and_stops(self):
    sim = self.sim
    for _ in range(500):
      sim.step((0, 0, 0))
    start = sim.data.qpos[0]
    for _ in range(1000):
      sim.step((.25, 0, 0))
    # This bundled policy tracks conservative requests imperfectly on flat ground.
    self.assertGreater(sim.data.qpos[0] - start, .3)
    for _ in range(500):
      sim.step((0, 0, 0))
    self.assertGreater(sim.data.qpos[2], .2)
    self.assertLess(abs(sim.data.sensor("local_linvel").data[0]), .15)

  def test_positive_yaw_turns_left(self):
    for _ in range(500):
      self.sim.step((0, 0, 0))
    for _ in range(1000):
      self.sim.step((0, 0, .5))
    quat = self.sim.data.qpos[3:7]
    yaw = np.arctan2(2 * (quat[0] * quat[3] + quat[1] * quat[2]),
                     1 - 2 * (quat[2] ** 2 + quat[3] ** 2))
    self.assertGreater(yaw, .2)

  def test_maze_route_with_bounded_symbolic_commands(self):
    # Test-only waypoint pilot supplies the same symbolic labels as gestures.
    # This verifies traversability, not webcam recognition or operator skill.
    sim = self.sim
    gate = safety.Supervisor()
    points = ((2.15, 0), (2.15, 2.15), (5.2, 2.15))
    target = 0
    turning = False
    for tick in range(75000):
      delta = np.array(points[target]) - sim.data.qpos[:2]
      if np.linalg.norm(delta) < .25 and target < len(points) - 1:
        target += 1
        delta = np.array(points[target]) - sim.data.qpos[:2]
        turning = True
      q = sim.data.qpos[3:7]
      yaw = np.arctan2(2 * (q[0] * q[3] + q[1] * q[2]),
                       1 - 2 * (q[2] ** 2 + q[3] ** 2))
      error = (np.arctan2(delta[1], delta[0]) - yaw + np.pi) % (2 * np.pi) - np.pi
      # Generous hysteresis accommodates imperfect low-speed policy tracking.
      if abs(error) > .4:
        turning = True
      elif abs(error) < .2:
        turning = False
      label = ("LEFT" if error > 0 else "RIGHT") if turning else "FORWARD"
      now = 1 + tick * sim.model.opt.timestep
      command, _ = gate.approve(safety.Prediction(label, now), now, True, now)
      sim.step(command)
      if sim.goal_reached:
        break
    self.assertTrue(sim.goal_reached, "Bounded reference commands must reach the goal")
    self.assertEqual(sim.contacts, 0)

  def test_body_and_leg_wall_collision_masks(self):
    sim = self.sim
    physical = np.flatnonzero(sim.model.geom_group == 3)
    self.assertGreater(len(physical), 4)
    self.assertTrue(np.all(sim.model.geom_conaffinity[physical] & 2))
    sim.data.qpos[1] = -.9
    mujoco.mj_forward(sim.model, sim.data)
    contacts = [c for c in sim.data.contact
                if c.geom1 in sim.walls or c.geom2 in sim.walls]
    self.assertTrue(contacts, "Robot body must contact the south wall")

  def test_reset_clears_policy_history(self):
    self.sim.controller.last_action[:] = 1
    self.sim.contacts = 5
    self.sim.reset()
    np.testing.assert_array_equal(self.sim.controller.last_action, np.zeros(12))
    self.assertEqual(self.sim.contacts, 0)

  def test_all_scenes_and_two_camera_views(self):
    for scene in ("arena", "corridor", "maze"):
      sim = simulation.Simulation(scene)
      with mujoco.Renderer(sim.model, height=180, width=320) as renderer:
        overview, fpv = sim.render(renderer)
      self.assertEqual(overview.shape, (180, 320, 3))
      self.assertGreater(float(fpv.std()), 1)
      self.assertFalse(np.array_equal(overview, fpv))


if __name__ == "__main__":
  unittest.main()
