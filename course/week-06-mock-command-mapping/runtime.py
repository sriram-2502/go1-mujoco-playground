"""Week 6 integration: independent simulation watchdog and latest-value mailboxes."""

import csv
from datetime import datetime
from pathlib import Path
import threading
import time

from course import safety

RENDER_PRESETS = {"performance": (640, 360), "balanced": (960, 540),
                  "quality": (1280, 720)}


class ViewRenderer(threading.Thread):
  """Own the OpenGL context and render the latest private physics snapshot.

  Only mjData copies hold the mailbox lock. GPU rendering never does, and there
  is a single pending snapshot rather than a queue of increasingly stale frames.
  """

  def __init__(self, sim, render_size=(640, 360)):
    import mujoco
    super().__init__(daemon=True, name="go1-cameras")
    self.sim = sim
    self.width, self.height = render_size
    # Configure before creating the renderer; these sizes remain fixed while it runs.
    sim.model.vis.global_.offwidth = max(sim.model.vis.global_.offwidth, self.width)
    sim.model.vis.global_.offheight = max(sim.model.vis.global_.offheight, self.height)
    self.pending = mujoco.MjData(sim.model)
    self.lock = threading.Lock()
    self.ready = threading.Event()
    self.quit = threading.Event()
    self.images = (None, None)
    self.error = ""
    self.fps = self.render_ms = 0.0

  def submit(self):
    import mujoco
    with self.lock:
      mujoco.mj_copyData(self.pending, self.sim.model, self.sim.data)
      self.ready.set()

  def snapshot(self):
    with self.lock:
      return self.images, self.error, self.fps, self.render_ms

  def run(self):
    import mujoco
    renderer = None
    try:
      data = mujoco.MjData(self.sim.model)
      renderer = mujoco.Renderer(self.sim.model, height=self.height, width=self.width)
      previous = time.monotonic()
      while not self.quit.is_set():
        if not self.ready.wait(.05):
          continue
        if self.quit.is_set():
          break
        with self.lock:
          mujoco.mj_copyData(data, self.sim.model, self.pending)
          self.ready.clear()
        start = time.monotonic()
        images = self.sim.render(renderer, data=data)
        end = time.monotonic()
        with self.lock:
          self.images = images
          self.fps = 1 / max(end - previous, .001)
          self.render_ms = (end - start) * 1000
        previous = end
    except Exception as exc:
      with self.lock:
        self.error = f"{type(exc).__name__}: {exc}"
    finally:
      if renderer is not None:
        renderer.close()


class Runtime(threading.Thread):
  def __init__(self, webcam, scene="maze", source="gesture", render=True,
               render_size=(640, 360)):
    super().__init__(daemon=True, name="go1-simulation")
    self.webcam = webcam
    self.scene = scene
    self.source = source
    self.render_enabled = render
    self.render_size = render_size
    self.lock = threading.Lock()
    self.quit = threading.Event()
    self.reset_requested = threading.Event()
    self.enabled = False
    self.heartbeat = time.monotonic()
    self.keyboard_label = "STOP"
    self.trial = False
    self.state = {"status": "Loading Go1 and ONNX policy..."}
    self.overview = self.fpv = None
    self.views = None
    self.error = ""
    self.log_path = ""

  def controls(self, *, enabled=None, label=None, trial=None):
    with self.lock:
      self.heartbeat = time.monotonic()
      if enabled is not None:
        self.enabled = enabled
      if label is not None:
        self.keyboard_label = label
      if trial is not None:
        self.trial = trial

  def snapshot(self):
    with self.lock:
      state, overview, fpv, error, views = (
          dict(self.state), self.overview, self.fpv, self.error, self.views)
    # Read the newest completed images directly. Telemetry publication must not
    # throttle video or add another frame of delay between rendering and Qt.
    if views is not None:
      (overview, fpv), render_error, fps, render_ms = views.snapshot()
      state.update(render_fps=fps, render_ms=render_ms)
      error = error or render_error
    return state, overview, fpv, error

  def run(self):
    renderer = None
    log = None
    try:
      import numpy as np
      from course import simulation

      sim = simulation.Simulation(self.scene)
      supervisor = safety.Supervisor()
      if self.render_enabled:
        renderer = ViewRenderer(sim, self.render_size)
        renderer.submit()
        with self.lock:
          self.views = renderer
        renderer.start()
      folder = Path(__file__).parents[2] / "logs"
      folder.mkdir(exist_ok=True)
      self.log_path = str(folder / f"sim-{datetime.now():%Y%m%d-%H%M%S-%f}.csv")
      log = open(self.log_path, "w", newline="", encoding="utf-8")
      writer = csv.writer(log)
      writer.writerow(("monotonic_s", "sim_s", "trial_id", "raw_gesture", "input_age_s",
                       "requested_vx", "requested_vy", "requested_yaw",
                       "approved_vx", "approved_vy", "approved_yaw", "status",
                       "x", "y", "measured_vx", "measured_yaw", "wall_contacts", "resets", "goal",
                       "real_time_factor", "render_fps", "render_ms"))
      next_render = next_log = next_state = next_flush = time.monotonic()
      previous = time.monotonic()
      sample_wall, sample_sim = previous, sim.data.time
      real_time_factor = 1.0
      render_fps = render_ms = 0.0
      trial_started = None
      trial_id = resets = 0
      was_trial = False
      completed = False
      fallen = False
      elapsed = 0.0
      budget = 0.0
      while not self.quit.is_set():
        now = time.monotonic()
        with self.lock:
          enabled, heartbeat, label, trial = (
              self.enabled, self.heartbeat, self.keyboard_label, self.trial)
        if self.reset_requested.is_set():
          sim.reset()
          resets += 1
          supervisor.reset()
          self.reset_requested.clear()
          with self.lock:
            self.enabled = self.trial = False
          enabled = trial = False
          completed = False
          fallen = False
          elapsed = 0.0
          budget = 0.0
          sample_wall, sample_sim = now, sim.data.time
        if trial and not was_trial:
          trial_id += 1
          trial_started = now
          completed = False
        if trial and trial_started is not None:
          elapsed = now - trial_started
        was_trial = trial
        if self.source == "gesture":
          _, prediction, camera_error, _ = self.webcam.snapshot()
          if camera_error:
            prediction = safety.Prediction("NO_HAND", now)
        elif self.source == "keyboard":
          prediction = safety.Prediction(label, heartbeat)
        else:
          # Scripted, bounded input to check the command interface, not solve a maze.
          sequence = ("STOP", "FORWARD", "STOP", "LEFT", "STOP", "RIGHT", "STOP")
          prediction = safety.Prediction(sequence[int(sim.data.time / 2) % len(sequence)], now)
        command, status = supervisor.approve(prediction, now, enabled, heartbeat)
        if completed or fallen:
          command, status = (0.0, 0.0, 0.0), "GOAL REACHED - RESET TO RESTART"
          if fallen:
            status = "ROBOT FELL - RESET REQUIRED"
        # Bound catch-up work after an OS stall; rendering runs independently.
        budget = min(budget + max(0, now - previous), 0.04)
        previous = now
        while budget >= sim.model.opt.timestep:
          sim.step(command)
          budget -= sim.model.opt.timestep
        if not np.isfinite(sim.data.qpos).all():
          raise RuntimeError("Non-finite robot state; stop and reset the simulation")
        if sim.data.qpos[2] < 0.12:
          fallen = True
          with self.lock:
            self.enabled = False
          command, status = (0.0, 0.0, 0.0), "ROBOT FELL - RESET REQUIRED"
        if sim.goal_reached:
          completed = True
          with self.lock:
            self.enabled = self.trial = False
          command, status = (0.0, 0.0, 0.0), "GOAL REACHED - RESET TO RESTART"
        if now - sample_wall >= 1.0:
          real_time_factor = (sim.data.time - sample_sim) / (now - sample_wall)
          sample_wall, sample_sim = now, sim.data.time
        if now >= next_render and renderer is not None:
          renderer.submit()
          # Absolute deadlines avoid Windows timer granularity reducing 30 Hz
          # to ~21 Hz when each relative 33 ms wait rounds up to ~47 ms.
          next_render = max(next_render + 1 / 30, now)
        if now >= next_state:
          images = (None, None)
          if renderer is not None:
            images, render_error, render_fps, render_ms = renderer.snapshot()
            if render_error:
              raise RuntimeError(f"Camera rendering failed: {render_error}")
          with self.lock:
            self.overview, self.fpv = images
            self.state = dict(status=status, label=prediction.label, command=command,
                              measured_velocity=(float(sim.data.sensor("local_linvel").data[0]),
                                                 float(sim.data.sensor("local_linvel").data[1]),
                                                 float(sim.data.sensor("gyro").data[2])),
                              age=max(0, now - prediction.timestamp), sim_time=sim.data.time,
                              x=sim.data.qpos[0], y=sim.data.qpos[1],
                              contacts=sim.contacts, resets=resets, goal=completed, fallen=fallen,
                              elapsed=elapsed, trial_id=trial_id, enabled=self.enabled,
                              rtf=real_time_factor, render_fps=render_fps, render_ms=render_ms)
          next_state = max(next_state + .05, now)
        if now >= next_log:
          requested = supervisor.requested(prediction.label)
          writer.writerow((now, sim.data.time, trial_id if trial or completed else 0, prediction.label,
                           now - prediction.timestamp, *requested, *command, status,
                           *sim.data.qpos[:2], sim.data.sensor("local_linvel").data[0],
                           sim.data.sensor("gyro").data[2], sim.contacts, resets, completed,
                           real_time_factor, render_fps, render_ms))
          # Buffer rows, flushing once per second rather than on every update.
          if now >= next_flush:
            log.flush()
            next_flush = now + 1
          next_log = now + 0.1
        self.quit.wait(0.001)
    except Exception as exc:
      with self.lock:
        self.enabled = False
        self.error = f"{type(exc).__name__}: {exc}"
    finally:
      if renderer is not None:
        renderer.quit.set()
        renderer.ready.set()
        renderer.join(timeout=3)
      if log is not None:
        log.close()
