"""Week 6 mission control. Run ``python run_gesture_navigation.py`` at repo root."""

import argparse
from importlib import import_module
from pathlib import Path
import sys
import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QFormLayout, QFrame, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget,
)

from course import vision

Runtime = import_module("course.week-06-mock-command-mapping.runtime").Runtime
RENDER_PRESETS = import_module("course.week-06-mock-command-mapping.runtime").RENDER_PRESETS

STYLE = """
QMainWindow, QWidget { background: #0c1421; color: #e7effb; font-family: 'Segoe UI'; font-size: 16px; }
QFrame#panel { background: #142032; border: 1px solid #25374e; border-radius: 14px; }
QLabel { background: transparent; border: none; }
QLabel#muted { color: #91a6c2; }
QPushButton { background: #24374f; border: 1px solid #38516d; border-radius: 8px; padding: 10px 14px; font-weight: 600; }
QPushButton:hover { background: #324c69; }
QPushButton#enable { background: #146657; border-color: #259982; }
QPushButton#stop { background: #932f46; border-color: #e06478; }
QPushButton:disabled { color: #64748b; background: #172234; }
QComboBox { background: #24374f; border: 1px solid #38516d; border-radius: 7px; padding: 8px; }
QComboBox QAbstractItemView { background: #24374f; color: white; }
"""


class Video(QLabel):
  def __init__(self, placeholder):
    super().__init__(placeholder)
    self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.setMinimumSize(160, 120)
    self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
    self.setStyleSheet("background: #080f1b; color: #8da5c0; border-radius: 8px;")
    self.frame = None
    self.last_size = None
    self.display_fps = 0.0
    self.display_count = 0
    self.display_since = time.monotonic()

  def show_frame(self, frame):
    if frame is self.frame and self.last_size == self.size():
      return
    if frame is not None:
      self.frame = frame
    if self.frame is None:
      return
    self.display_count += 1
    now = time.monotonic()
    if now - self.display_since >= 1:
      self.display_fps = self.display_count / (now - self.display_since)
      self.display_count = 0
      self.display_since = now
    self.last_size = self.size()
    height, width, _ = self.frame.shape
    picture = QImage(self.frame.data, width, height, self.frame.strides[0],
                     QImage.Format.Format_RGB888).copy()
    self.setPixmap(QPixmap.fromImage(picture).scaled(
        self.size(), Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation))


def panel(title, widget, accessory=None, readout=None):
  frame = QFrame()
  frame.setObjectName("panel")
  layout = QVBoxLayout(frame)
  layout.setContentsMargins(10, 8, 10, 10)
  layout.setSpacing(6)
  header = QHBoxLayout()
  heading = QLabel(title)
  heading.setStyleSheet("font-size: 18px; font-weight: 600;")
  header.addWidget(heading)
  header.addStretch()
  if accessory is not None:
    header.addWidget(accessory)
  layout.addLayout(header)
  if readout is not None:
    layout.addWidget(readout)
  layout.addWidget(widget, 1)
  return frame


class Dashboard(QMainWindow):
  def __init__(self, args):
    super().__init__()
    self.args = args
    self.args.quality = getattr(args, "quality", "quality")
    self.setWindowTitle("Go1 Mission Control | Week 06")
    screen = QApplication.primaryScreen().availableGeometry()
    self.resize(min(1280, screen.width() - 24), min(800, screen.height() - 24))
    self.webcam = vision.Webcam(args.camera)
    self.runtime = Runtime(self.webcam, args.scene, args.input,
                           render_size=RENDER_PRESETS[self.args.quality])
    self.workers = []
    self.key_down = None
    self.recording = False
    root = QWidget()
    self.setCentralWidget(root)
    layout = QVBoxLayout(root)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)

    # Setup and diagnostics live off the driving surface, in a scrollable dialog.
    self.settings_dialog = QDialog(self)
    self.settings_dialog.setWindowTitle("Navigation settings")
    self.settings_dialog.resize(560, 540)
    settings_layout = QVBoxLayout(self.settings_dialog)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    settings_body = QWidget()
    form = QFormLayout(settings_body)
    form.setSpacing(12)
    self.quality = QComboBox()
    for name, (width, height) in RENDER_PRESETS.items():
      self.quality.addItem(f"{name.title()} - {width}x{height}", name)
    self.quality.setCurrentIndex(list(RENDER_PRESETS).index(self.args.quality))
    self.quality.currentIndexChanged.connect(self.change_quality)
    form.addRow("Video quality", self.quality)
    self.primary = QComboBox()
    self.primary.addItems(["Simulation", "Robot FPV"])
    self.primary.currentIndexChanged.connect(self.change_primary)
    form.addRow("Large view", self.primary)
    self.input = QComboBox()
    self.input.addItems(["gesture", "keyboard", "mock"])
    self.input.setCurrentText(args.input)
    self.input.currentTextChanged.connect(self.change_input)
    form.addRow("Input", self.input)
    self.scene = QComboBox()
    self.scene.addItems(["maze", "corridor", "arena"])
    self.scene.setCurrentText(args.scene)
    self.scene.currentTextChanged.connect(self.change_scene)
    form.addRow("Course", self.scene)
    help_text = QLabel("One hand: index = forward, two fingers = left, three = right. "
                       "Palm or fist = stop. Hold motion gestures for 0.30 s. "
                       "Space / Escape stops; F11 toggles fullscreen. "
                       "Changing quality, input or course resets the simulation.")
    help_text.setWordWrap(True)
    form.addRow(help_text)
    self.metrics = {}
    for name, initial in (("Gesture", "NO HAND"), ("Command (m/s, rad/s)", "0 / 0 / 0"),
                          ("Trial time", "0.0 s"), ("Wall contacts", "0")):
      value = QLabel(initial)
      self.metrics[name] = value
      form.addRow(name, value)
    self.details = QLabel("Initializing...")
    self.details.setWordWrap(True)
    form.addRow(self.details)
    self.log_label = QLabel("Logs will be written to logs/")
    self.log_label.setWordWrap(True)
    self.log_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    form.addRow(self.log_label)
    scroll.setWidget(settings_body)
    settings_layout.addWidget(scroll)
    close_settings = QPushButton("Done")
    close_settings.clicked.connect(self.settings_dialog.accept)
    settings_layout.addWidget(close_settings)

    self.view_grid = QGridLayout()
    self.view_grid.setSpacing(8)
    self.overview = Video("Loading simulation...")
    self.camera = Video("Opening webcam...")
    self.fpv = Video("Loading robot camera...")
    self.gesture_badge = QLabel("NO HAND")
    self.gesture_badge.setStyleSheet("font-size: 19px; font-weight: 700; color: #55dfbf;")
    self.velocity_readout = QLabel("[vx cmd -- | sim -- m/s]\n[yaw cmd -- | sim -- rad/s]")
    self.velocity_readout.setStyleSheet("font-family: Consolas; font-size: 14px; color: #b8cce3;")
    self.velocity_readout.setToolTip("Approved command versus measured body-frame simulator velocity. "
                                     "vx is forward speed; yaw is turning rate. Zero command requests standing.")
    self.overview_enlarge = QPushButton("Enlarge")
    self.fpv_enlarge = QPushButton("Enlarge")
    for button in (self.overview_enlarge, self.fpv_enlarge):
      button.setStyleSheet("font-size: 14px; padding: 4px 9px;")
    self.overview_enlarge.clicked.connect(lambda: self.primary.setCurrentIndex(0))
    self.fpv_enlarge.clicked.connect(lambda: self.primary.setCurrentIndex(1))
    self.overview_panel = panel("Simulation", self.overview, self.overview_enlarge)
    self.camera_panel = panel("Webcam", self.camera, self.gesture_badge, self.velocity_readout)
    self.fpv_panel = panel("Robot FPV", self.fpv, self.fpv_enlarge)
    self.change_primary(0)
    self.view_grid.setColumnStretch(0, 7)
    self.view_grid.setColumnStretch(1, 3)
    self.view_grid.setRowStretch(0, 1)
    self.view_grid.setRowStretch(1, 1)
    layout.addLayout(self.view_grid, 1)

    # Errors stay visible even when settings are closed. Routine diagnostics do not.
    self.notice = QLabel()
    self.notice.setWordWrap(True)
    self.notice.setStyleSheet("color: #ffce78; font-weight: 600; padding: 4px;")
    self.notice.hide()
    layout.addWidget(self.notice)
    bar = QHBoxLayout()
    bar.setSpacing(8)
    self.enable = QPushButton("Enable motion")
    self.enable.setObjectName("enable")
    self.enable.clicked.connect(self.arm)
    bar.addWidget(self.enable)
    stop = QPushButton("STOP [Space]")
    stop.setObjectName("stop")
    stop.setMinimumWidth(150)
    stop.clicked.connect(self.stop)
    bar.addWidget(stop)
    reset = QPushButton("Reset")
    reset.clicked.connect(self.reset)
    bar.addWidget(reset)
    self.trial_button = QPushButton("Start trial")
    self.trial_button.clicked.connect(self.toggle_trial)
    bar.addWidget(self.trial_button)
    self.status = QLabel("Loading...")
    self.status.setStyleSheet("color: #ffce78; font-weight: 600;")
    bar.addStretch()
    bar.addWidget(self.status)
    bar.addStretch()
    settings_button = QPushButton("Settings")
    settings_button.clicked.connect(self.open_settings)
    bar.addWidget(settings_button)
    for button in (self.enable, stop, reset, self.trial_button, settings_button):
      button.setMinimumHeight(46)
    layout.addLayout(bar)
    self.stop_shortcut = QShortcut(QKeySequence("Space"), self)
    self.stop_shortcut.activated.connect(self.stop)
    self.escape_shortcut = QShortcut(QKeySequence("Escape"), self)
    self.escape_shortcut.activated.connect(self.stop)
    self.fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
    self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
    self.webcam.start()
    self.runtime.start()
    self.workers.append(self.runtime)
    self.timer = QTimer(self)
    self.timer.setTimerType(Qt.TimerType.PreciseTimer)
    self.timer.timeout.connect(self.refresh)
    # Sample the render mailbox at twice its rate to avoid missing a new frame
    # when two independent ~30 Hz timers drift out of phase. Video caches repeats.
    self.timer.start(16)
    if args.screenshot:
      QTimer.singleShot(15000, self.screenshot)
    if args.quit_after:
      QTimer.singleShot(int(args.quit_after * 1000), self.close)

  def arm(self):
    self.runtime.controls(enabled=True, label="STOP")

  def stop(self):
    self.key_down = None
    self.runtime.controls(enabled=False, label="STOP")

  def reset(self):
    self.stop()
    self.recording = False
    self.runtime.controls(trial=False)
    self.runtime.reset_requested.set()
    self.trial_button.setText("Start trial")

  def toggle_trial(self):
    self.recording = not self.recording
    self.runtime.controls(trial=self.recording)
    self.trial_button.setText("End trial" if self.recording else "Start trial")

  def change_scene(self, scene):
    self.stop()
    self.runtime.quit.set()
    self.recording = False
    self.trial_button.setText("Start trial")
    self.runtime = Runtime(self.webcam, scene, self.args.input,
                           render_size=RENDER_PRESETS[self.args.quality])
    self.workers.append(self.runtime)
    self.runtime.start()

  def keyPressEvent(self, event):
    labels = {Qt.Key.Key_Up: "FORWARD", Qt.Key.Key_Left: "LEFT", Qt.Key.Key_Right: "RIGHT"}
    if event.key() in labels and self.args.input == "keyboard":
      if not event.isAutoRepeat():
        self.key_down = event.key()
        self.runtime.controls(label=labels[event.key()])
      return
    super().keyPressEvent(event)

  def keyReleaseEvent(self, event):
    if event.key() == self.key_down and not event.isAutoRepeat():
      self.key_down = None
      self.runtime.controls(label="STOP")
    super().keyReleaseEvent(event)

  def changeEvent(self, event):
    # A held arrow must not persist when the dashboard loses keyboard focus.
    from PySide6.QtCore import QEvent
    if event.type() == QEvent.Type.ActivationChange and not self.isActiveWindow():
      if hasattr(self, "runtime"):
        self.stop()
    super().changeEvent(event)

  def change_input(self, source):
    self.args.input = source
    self.change_scene(self.scene.currentText())

  def change_quality(self, index):
    self.args.quality = self.quality.itemData(index)
    self.change_scene(self.scene.currentText())

  def change_primary(self, index):
    for item in (self.overview_panel, self.camera_panel, self.fpv_panel):
      self.view_grid.removeWidget(item)
    main, secondary = ((self.overview_panel, self.fpv_panel) if index == 0
                       else (self.fpv_panel, self.overview_panel))
    self.view_grid.addWidget(main, 0, 0, 2, 1)
    self.view_grid.addWidget(self.camera_panel, 0, 1)
    self.view_grid.addWidget(secondary, 1, 1)
    self.overview_enlarge.setVisible(index != 0)
    self.fpv_enlarge.setVisible(index != 1)

  def open_settings(self):
    self.stop()
    self.settings_dialog.exec()

  def toggle_fullscreen(self):
    self.showNormal() if self.isFullScreen() else self.showFullScreen()

  def refresh(self):
    self.runtime.controls()
    frame, prediction, error, fps = self.webcam.snapshot()
    state, overview, fpv, sim_error = self.runtime.snapshot()
    self.camera.show_frame(frame)
    if error and frame is None:
      self.camera.setText(error)
      self.camera.setWordWrap(True)
    self.overview.show_frame(overview)
    self.fpv.show_frame(fpv)
    status = state.get("status", "STARTING")
    if status == "DISARMED / STOP LATCHED":
      self.status.setText("Motion disabled")
    else:
      short_status = {"HOLD GESTURE": "Hold gesture...", "FORWARD": "Forward",
                      "LEFT": "Turning left", "RIGHT": "Turning right",
                      "NO_HAND": "No hand", "UNKNOWN": "Unknown gesture", "STOP": "Stopped",
                      "STALE INPUT": "Input expired", "DASHBOARD TIMEOUT": "Input expired",
                      "GOAL REACHED - RESET TO RESTART": "Goal reached",
                      "ROBOT FELL - RESET REQUIRED": "Reset required"}
      self.status.setText(short_status.get(status, "Starting..."))
    self.status.setToolTip(status)
    self.enable.setText("Motion enabled" if state.get("enabled") else "Enable motion")
    self.gesture_badge.setText(state.get("label", prediction.label).replace("_", " "))
    self.notice.setText(sim_error or error)
    self.notice.setVisible(bool(sim_error or error))
    self.enable.setEnabled(not sim_error and overview is not None
                           and not state.get("goal") and not state.get("fallen"))
    self.trial_button.setEnabled(self.enable.isEnabled())
    self.metrics["Gesture"].setText(state.get("label", prediction.label))
    command = state.get("command", (0, 0, 0))
    measured = state.get("measured_velocity")
    if measured is not None:
      self.velocity_readout.setText(
          f"[vx cmd {command[0]:+.2f} | sim {measured[0]:+.2f} m/s]\n"
          f"[yaw cmd {command[2]:+.2f} | sim {measured[2]:+.2f} rad/s]")
    self.metrics["Command (m/s, rad/s)"].setText(" / ".join(f"{v:+.2f}" for v in command))
    self.metrics["Trial time"].setText(f"{state.get('elapsed', 0):.1f} s")
    self.metrics["Wall contacts"].setText(str(state.get("contacts", 0)))
    if state.get("goal"):
      self.recording = False
      self.trial_button.setText("Goal reached")
    if sim_error:
      self.stop()
      self.status.setText("Simulation error")
    self.details.setText(sim_error or error or (
        f"Input: {self.args.input.upper()}   •   Camera: {fps:.0f} fps   •   "
        f"Input age: {state.get('age', 0):.2f} s   •   "
        f"Sim: {state.get('rtf', 0):.2f}× real time   •   "
        f"Display: {self.overview.display_fps:.0f} fps / render: {state.get('render_fps', 0):.0f} fps   •   "
        f"Position: ({state.get('x', 0):.2f}, {state.get('y', 0):.2f}) m   •   "
        "Rule-based gestures; no classifier confidence score"))
    self.log_label.setText(f"CSV log: {self.runtime.log_path or 'starting…'}")

  def screenshot(self):
    self.grab().save(str(Path(self.args.screenshot).resolve()))

  def closeEvent(self, event):
    self.timer.stop()
    self.stop()
    self.webcam.quit.set()
    for worker in self.workers:
      worker.quit.set()
    for worker in self.workers:
      worker.join(timeout=3)
    self.webcam.join(timeout=2)
    event.accept()


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--camera", type=int, default=0)
  parser.add_argument("--scene", choices=("maze", "corridor", "arena"), default="maze")
  parser.add_argument("--input", choices=("gesture", "keyboard", "mock"), default="gesture")
  parser.add_argument("--quality", choices=tuple(RENDER_PRESETS), default="quality")
  parser.add_argument("--screenshot", help="Save a dashboard PNG after 15 seconds (QA)")
  parser.add_argument("--quit-after", type=float, help="Automatically close after N seconds (QA)")
  args = parser.parse_args()
  app = QApplication(sys.argv[:1])
  app.setStyleSheet(STYLE)
  window = Dashboard(args)
  window.showMaximized()
  sys.exit(app.exec())


if __name__ == "__main__":
  main()
