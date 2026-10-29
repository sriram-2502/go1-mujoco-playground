"""GUI checkout without a physical webcam; needs Qt and working OpenGL."""

import argparse
from importlib import import_module
import threading
import time
import unittest
from unittest.mock import patch

from PySide6.QtCore import QEventLoop, Qt, QTimer
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from course import safety

dashboard = import_module("course.week-06-mock-command-mapping.dashboard")


class CameraPlaceholder:
  def __init__(self, index):
    self.quit = threading.Event()

  def start(self):
    pass

  def join(self, timeout=None):
    pass

  def snapshot(self):
    return None, safety.Prediction(), "No webcam required for GUI checkout", 0


class DashboardTests(unittest.TestCase):
  def wait_for(self, predicate, window, seconds=30):
    deadline = time.monotonic() + seconds
    if predicate():
      return
    # Use a real Qt event loop, as the application does, so worker threads can
    # initialize while the GUI continues handling frame and heartbeat timers.
    loop = QEventLoop()
    timer = QTimer()
    def poll():
      if predicate() or window.runtime.snapshot()[3] or time.monotonic() >= deadline:
        loop.quit()
    timer.timeout.connect(poll)
    timer.start(20)
    loop.exec()
    timer.stop()
    self.assertFalse(window.runtime.snapshot()[3])
    self.assertTrue(predicate(), "Dashboard stage timed out")

  def test_quality_primary_fullscreen_motion_and_stop(self):
    app = QApplication.instance() or QApplication([])
    app.setStyleSheet(dashboard.STYLE)
    args = argparse.Namespace(camera=0, scene="arena", input="keyboard",
                              quality="balanced", screenshot=None, quit_after=None)
    with patch.object(dashboard.vision, "Webcam", CameraPlaceholder):
      window = dashboard.Dashboard(args)
      window.resize(1280, 720)
      window.show()
      try:
        self.wait_for(lambda: window.runtime.snapshot()[1] is not None, window)
        self.assertEqual(window.runtime.snapshot()[1].shape, (540, 960, 3))
        self.assertGreater(window.overview.width(), window.width() * .6)
        self.assertGreater(window.overview.height(), window.height() * .7)
        self.assertLess(window.camera_panel.width() / window.camera_panel.height(), 1.6)
        self.assertFalse(window.quality.isVisible(), "Setup controls belong in Settings")
        self.assertFalse(window.details.isVisible(), "Diagnostics must not crowd the video")
        self.assertIn("[vx cmd", window.velocity_readout.text())
        self.assertIn("sim", window.velocity_readout.text())
        worker = window.runtime
        window.primary.setCurrentIndex(1)
        self.assertIs(window.runtime, worker, "Changing view must preserve the trial")
        self.assertIs(window.view_grid.itemAtPosition(0, 0).widget(), window.fpv_panel)
        window.toggle_fullscreen()
        self.assertTrue(window.isFullScreen())
        window.toggle_fullscreen()
        self.assertFalse(window.isFullScreen())
        window.quality.setCurrentIndex(2)
        self.assertTrue(worker.quit.is_set())
        self.wait_for(lambda: window.runtime.snapshot()[1] is not None, window)
        self.assertEqual(window.runtime.snapshot()[1].shape, (720, 1280, 3))
        self.assertFalse(window.runtime.snapshot()[0].get("enabled"))
        window.arm()
        QTest.keyPress(window, Qt.Key.Key_Up)
        self.wait_for(lambda: window.runtime.snapshot()[0].get("command") == (.25, 0, 0), window, 5)
        self.wait_for(lambda: "vx cmd +0.25" in window.velocity_readout.text(), window, 5)
        QTest.keyRelease(window, Qt.Key.Key_Up)
        window.stop()
        self.wait_for(lambda: window.runtime.snapshot()[0].get("command") == (0, 0, 0), window, 5)
        self.assertFalse(window.runtime.snapshot()[0].get("enabled"))
      finally:
        window.close()
    self.assertTrue(all(not worker.is_alive() for worker in window.workers))
