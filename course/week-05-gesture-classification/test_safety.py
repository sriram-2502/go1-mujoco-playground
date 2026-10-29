"""Run: python -m unittest discover -s course/week-05-gesture-classification."""

import unittest

from course import safety


class SupervisorTests(unittest.TestCase):
  def setUp(self):
    self.supervisor = safety.Supervisor()

  def approve(self, label, stamp, now=None, enabled=True, heartbeat=None):
    now = stamp if now is None else now
    return self.supervisor.approve(safety.Prediction(label, stamp), now, enabled,
                                   now if heartbeat is None else heartbeat)

  def moving(self):
    self.approve("FORWARD", 10)
    return self.approve("FORWARD", 10.31)

  def test_hold_and_bounds(self):
    self.assertEqual(self.approve("FORWARD", 10)[0], (0, 0, 0))
    self.assertEqual(self.approve("FORWARD", 10.31)[0], (.25, 0, 0))
    self.assertEqual(self.approve("LEFT", 10.32)[0], (0, 0, 0))
    self.assertEqual(self.approve("LEFT", 10.63)[0], (0, 0, .5))

  def test_same_frame_does_not_satisfy_hold(self):
    self.approve("FORWARD", 10)
    self.assertEqual(self.approve("FORWARD", 10, now=10.35)[0], (0, 0, 0))

  def test_stop_and_invalid_input_bypass_hold(self):
    for label in ("STOP", "NO_HAND", "UNKNOWN", "bad label"):
      self.moving()
      self.assertEqual(self.approve(label, 10.32)[0], (0, 0, 0))
      self.assertEqual(self.approve("FORWARD", 10.33)[0], (0, 0, 0))

  def test_stale_input_and_ui_watchdog(self):
    self.moving()
    self.assertEqual(self.approve("FORWARD", 10.31, now=10.8)[0], (0, 0, 0))
    self.moving()
    self.assertEqual(self.approve("FORWARD", 10.32, heartbeat=9)[0], (0, 0, 0))

  def test_disarm_clears_candidate(self):
    self.moving()
    self.assertEqual(self.approve("FORWARD", 10.32, enabled=False)[0], (0, 0, 0))
    self.assertEqual(self.approve("FORWARD", 10.33)[0], (0, 0, 0))

  def test_invalid_timestamps(self):
    for stamp in (float("nan"), float("inf"), 11):
      self.assertEqual(self.approve("FORWARD", stamp, now=10)[0], (0, 0, 0))
    self.moving()
    self.assertEqual(self.approve("FORWARD", 10.2, now=10.32)[0], (0, 0, 0))

  def test_gap_does_not_count_as_hold(self):
    self.approve("FORWARD", 10)
    self.assertEqual(self.approve("FORWARD", 11)[0], (0, 0, 0))

  def test_limits_reject_unbounded_values(self):
    with self.assertRaises(ValueError):
      safety.Supervisor(safety.Limits(forward=float("nan")))
    with self.assertRaises(ValueError):
      safety.Supervisor(safety.Limits(yaw=10))


if __name__ == "__main__":
  unittest.main()
