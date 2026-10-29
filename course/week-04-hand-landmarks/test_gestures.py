"""Synthetic geometry checks; real operator recognition still needs evaluation."""

from types import SimpleNamespace
import unittest

from course import gestures


class GestureTests(unittest.TestCase):
  def pose(self, extended):
    points = [SimpleNamespace(x=0, y=0, z=0) for _ in range(21)]
    for up, tip, pip in zip(extended, (8, 12, 16, 20), (6, 10, 14, 18)):
      points[pip].y = .5
      points[tip].y = 1 if up else .2
    return points

  def test_reference_vocabulary_and_unknown(self):
    for pose, label in (((1, 1, 1, 1), "STOP"), ((0, 0, 0, 0), "STOP"),
                        ((1, 0, 0, 0), "FORWARD"), ((1, 1, 0, 0), "LEFT"),
                        ((1, 1, 1, 0), "RIGHT"), ((0, 1, 0, 1), "UNKNOWN")):
      self.assertEqual(gestures.classify(self.pose(pose)), label)

  def test_rotation_translation_and_scale(self):
    points = self.pose((1, 1, 0, 0))
    for p in points:
      p.x, p.y = 3 - p.y * .2, 5 + p.x * .2
    self.assertEqual(gestures.classify(points), "LEFT")

  def test_incomplete_landmarks(self):
    self.assertEqual(gestures.classify([]), "UNKNOWN")
