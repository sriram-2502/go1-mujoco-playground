"""Shared weekly lab modules, resolved without modifying sys.path.

Existing lab directory names contain hyphens. import_module supports those names;
this facade gives students ordinary imports such as ``from course import safety``.
"""

from importlib import import_module

_MODULES = {
    "simulation": "week-02-go1-controller.simulation",
    "vision": "week-03-webcam-basics.vision",
    "gestures": "week-04-hand-landmarks.gestures",
    "safety": "week-05-gesture-classification.safety",
}


def __getattr__(name):
  if name not in _MODULES:
    raise AttributeError(name)
  module = import_module(f"{__name__}.{_MODULES[name]}")
  globals()[name] = module
  return module
