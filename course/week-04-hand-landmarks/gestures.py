"""Week 4: orientation-independent finger rules for the reference vocabulary.

These are geometric rules, not a trained gesture confidence estimator. Students
can replace classify() while preserving the label contract.
"""

from math import sqrt


def _distance(a, b):
  return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def classify(landmarks):
  """Open palm/fist: STOP; index: forward; V: left; three fingers: right."""
  if len(landmarks) != 21:
    return "UNKNOWN"
  # Compare tip and middle-joint distances from the wrist, ignoring the thumb.
  fingers = tuple(
      _distance(landmarks[tip], landmarks[0])
      > 1.18 * _distance(landmarks[pip], landmarks[0])
      for tip, pip in ((8, 6), (12, 10), (16, 14), (20, 18))
  )
  return {
      (True, True, True, True): "STOP",
      (False, False, False, False): "STOP",
      (True, False, False, False): "FORWARD",
      (True, True, False, False): "LEFT",
      (True, True, True, False): "RIGHT",
  }.get(fingers, "UNKNOWN")
