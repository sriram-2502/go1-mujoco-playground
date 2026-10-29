"""Stage 1: measure the real dashboard before changing its presentation path.

Run from the repository root:
  python -m course.week-06-mock-command-mapping.benchmark

Each resolution gets a fresh simulation, a warm-up and a measured interval.
Motion remains disabled. Output is local JSON under ignored logs/.
"""

import argparse
from collections import Counter
from datetime import datetime
from importlib import import_module
import json
from pathlib import Path
import statistics
import threading
import time
from unittest.mock import patch

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from course import simulation

dashboard = import_module("course.week-06-mock-command-mapping.dashboard")
runtime = import_module("course.week-06-mock-command-mapping.runtime")
SIZES = runtime.RENDER_PRESETS


def summary(values):
  if not values:
    return None
  ordered = sorted(values)
  return {"median": round(statistics.median(values), 3),
          "p95": round(ordered[min(len(ordered) - 1, int(len(ordered) * .95))], 3)}


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--seconds", type=float, default=8)
  parser.add_argument("--warmup", type=float, default=3)
  parser.add_argument("--camera", type=int, default=0)
  parser.add_argument("--preset", choices=tuple(SIZES), action="append",
                      help="Repeat to select presets; default tests all three")
  args = parser.parse_args()
  if args.seconds < 2 or args.warmup < 0:
    parser.error("Use at least 2 measured seconds and a nonnegative warm-up")
  presets = iter(args.preset or SIZES)
  current = {"preset": next(presets)}
  metadata = {}
  metadata_lock = threading.Lock()
  original_render = simulation.Simulation.render
  original_show = dashboard.Video.show_frame
  original_refresh = dashboard.Dashboard.refresh
  results = []
  samples = {}
  phase = "startup"
  phase_started = time.monotonic()
  baseline = None
  failure = None

  def create_runtime(*a, **kw):
    kw["render_size"] = SIZES[current["preset"]]
    return runtime.Runtime(*a, **kw)

  def measured_render(sim, renderer, data=None):
    start = time.perf_counter()
    frames = original_render(sim, renderer, data)
    end = time.perf_counter()
    with metadata_lock:
      for frame in frames:
        metadata[id(frame)] = (end, (end - start) * 1000,
                               (sim.data if data is None else data).time)
      # Keep only a few recent frames; no unbounded array/metadata retention.
      while len(metadata) > 100:
        del metadata[next(iter(metadata))]
    return frames

  def measured_show(video, frame):
    changed = frame is not None and frame is not video.frame
    start = time.perf_counter()
    original_show(video, frame)
    end = time.perf_counter()
    if phase != "measure" or not changed:
      return
    if video is window.overview:
      samples["displayed_frames"] += 1
      samples["ui_copy_scale_ms"].append((end - start) * 1000)
      with metadata_lock:
        info = metadata.get(id(frame))
      if info:
        completed, duration, sim_time = info
        samples["render_ms"].append(duration)
        samples["delivery_age_ms"].append((end - completed) * 1000)
        state = window.runtime.snapshot()[0]
        samples["snapshot_lag_sim_ms"].append(max(0, state.get("sim_time", sim_time) - sim_time) * 1000)

  def measured_refresh(window):
    start = time.perf_counter()
    window.runtime.controls(enabled=False)
    original_refresh(window)
    for control in (window.enable, window.trial_button, window.scene, window.input, window.quality):
      control.setEnabled(False)
    if phase == "measure":
      samples["ui_refresh_ms"].append((time.perf_counter() - start) * 1000)

  def tick():
    nonlocal phase, phase_started, samples, baseline, failure
    now = time.monotonic()
    state, overview, _, error = window.runtime.snapshot()
    if error or now - phase_started > 45:
      failure = error or "Stage timed out"
      print(f"BENCHMARK ERROR: {failure}", flush=True)
      window.close()
      return
    if phase == "startup" and overview is not None:
      phase, phase_started = "warmup", now
      print(f"Warm-up: {current['preset']} {SIZES[current['preset']]}", flush=True)
    elif phase == "warmup" and now - phase_started >= args.warmup:
      samples = {name: [] for name in ("render_ms", "delivery_age_ms", "snapshot_lag_sim_ms",
                                      "ui_copy_scale_ms", "ui_refresh_ms", "input_age_ms", "camera_fps")}
      samples["displayed_frames"] = 0
      samples["gestures"] = Counter()
      baseline = (now, state["sim_time"], time.process_time())
      phase, phase_started = "measure", now
    elif phase == "measure":
      _, prediction, camera_error, fps = window.webcam.snapshot()
      samples["input_age_ms"].append((now - prediction.timestamp) * 1000)
      samples["camera_fps"].append(fps)
      samples["gestures"][prediction.label] += 1
      if now - baseline[0] >= args.seconds:
        elapsed = now - baseline[0]
        result = {"preset": current["preset"], "size": SIZES[current["preset"]],
                  "seconds": round(elapsed, 2),
                  "simulation_speed": round((state["sim_time"] - baseline[1]) / elapsed, 3),
                  "displayed_fps": round(samples["displayed_frames"] / elapsed, 2),
                  "process_cpu_one_core_percent": round((time.process_time() - baseline[2]) / elapsed * 100, 1),
                  "camera_error": camera_error, "gestures": dict(samples["gestures"])}
        result.update({k: summary(v) for k, v in samples.items() if isinstance(v, list)})
        results.append(result)
        print(json.dumps(result, indent=2), flush=True)
        try:
          current["preset"] = next(presets)
        except StopIteration:
          phase = "finished"
          window.close()
          return
        phase, phase_started = "startup", now
        window.quality.blockSignals(True)
        window.quality.setCurrentIndex(list(SIZES).index(current["preset"]))
        window.quality.blockSignals(False)
        window.args.quality = current["preset"]
        window.change_scene("maze")

  app = QApplication([])
  app.setStyleSheet(dashboard.STYLE)
  with patch.object(dashboard, "Runtime", create_runtime), \
       patch.object(simulation.Simulation, "render", measured_render), \
       patch.object(dashboard.Video, "show_frame", measured_show), \
       patch.object(dashboard.Dashboard, "refresh", measured_refresh):
    window = dashboard.Dashboard(argparse.Namespace(camera=args.camera, scene="maze", input="gesture",
                                                    quality=current["preset"], screenshot=None, quit_after=None))
    window.show()
    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(50)
    app.exec()
    timer.stop()
  destination = Path("logs") / f"dashboard-benchmark-{datetime.now():%Y%m%d-%H%M%S}.json"
  destination.parent.mkdir(exist_ok=True)
  destination.write_text(json.dumps({"results": results, "error": failure,
      "notes": ["Motion disabled; perception timing is frame age, not gesture-to-motion latency.",
                "Displayed FPS counts new frames submitted to Qt, not measured monitor scanout.",
                "delivery_age_ms measures render completion to UI submission.",
                "CPU 100% means one fully utilized core; GPU utilization is not sampled."]}, indent=2), encoding="utf-8")
  print(f"Saved {destination}", flush=True)
  if failure:
    raise SystemExit(1)


if __name__ == "__main__":
  main()
