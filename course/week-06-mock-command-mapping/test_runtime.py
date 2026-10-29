"""Exercise the actual worker with timestamped synthetic webcam predictions."""

from importlib import import_module
import time
import unittest
from unittest.mock import patch

from course import safety

Runtime = import_module("course.week-06-mock-command-mapping.runtime").Runtime


class SyntheticCamera:
  prediction = safety.Prediction()

  def snapshot(self):
    return None, self.prediction, "", 30


class RuntimeTests(unittest.TestCase):
  def test_slow_camera_rendering_does_not_slow_physics_or_stop(self):
    import threading
    import numpy as np
    from course import simulation

    drawing = threading.Event()

    def slow_render(sim, renderer, data=None):
      drawing.set()
      time.sleep(.20)  # Reproduce the original graphics stall.
      return (np.zeros((180, 320, 3), dtype=np.uint8),) * 2

    camera = SyntheticCamera()
    worker = Runtime(camera, "arena", render=True)
    with patch.object(simulation.Simulation, "render", slow_render):
      worker.start()
      try:
        deadline = time.monotonic() + 30
        while not drawing.is_set():
          worker.controls()
          self.assertFalse(worker.snapshot()[3])
          self.assertLess(time.monotonic(), deadline)
          time.sleep(.02)
        worker.controls(enabled=True)
        start = time.monotonic()
        initial_sim_time = worker.snapshot()[0].get("sim_time", 0)
        while time.monotonic() - start < 2:
          camera.prediction = safety.Prediction("FORWARD", time.monotonic())
          worker.controls()
          time.sleep(.02)
        state = worker.snapshot()[0]
        self.assertEqual(state["command"], (.25, 0, 0))
        ratio = (state["sim_time"] - initial_sim_time) / (time.monotonic() - start)
        self.assertGreater(ratio, .75, "Rendering must not throttle physics")
        worker.controls(enabled=False)
        time.sleep(.15)
        self.assertEqual(worker.snapshot()[0]["command"], (0, 0, 0))
      finally:
        worker.quit.set()
        worker.join(5)
    self.assertFalse(worker.is_alive())
    self.assertFalse(worker.snapshot()[3])

  def test_live_input_timeout_stop_reset_and_shutdown(self):
    camera = SyntheticCamera()
    worker = Runtime(camera, "arena", render=False)
    worker.start()
    try:
      deadline = time.monotonic() + 30
      while "command" not in worker.snapshot()[0]:
        self.assertFalse(worker.snapshot()[3])
        self.assertLess(time.monotonic(), deadline, "Simulation startup timed out")
        worker.controls()
        time.sleep(.03)
      worker.controls(enabled=True)
      deadline = time.monotonic() + .8
      while time.monotonic() < deadline:
        camera.prediction = safety.Prediction("FORWARD", time.monotonic())
        worker.controls()
        time.sleep(.02)
      self.assertEqual(worker.snapshot()[0]["command"], (.25, 0, 0))
      # Keep UI alive but freeze perception.
      deadline = time.monotonic() + .65
      while time.monotonic() < deadline:
        worker.controls()
        time.sleep(.02)
      self.assertEqual(worker.snapshot()[0]["command"], (0, 0, 0))
      self.assertEqual(worker.snapshot()[0]["status"], "STALE INPUT")
      worker.controls(enabled=False)
      worker.reset_requested.set()
      deadline = time.monotonic() + .5
      while time.monotonic() < deadline:
        worker.controls()
        time.sleep(.02)
      self.assertFalse(worker.snapshot()[0]["enabled"])
      self.assertEqual(worker.snapshot()[0]["resets"], 1)
    finally:
      worker.quit.set()
      worker.join(5)
    self.assertFalse(worker.is_alive())
    self.assertFalse(worker.snapshot()[3])
