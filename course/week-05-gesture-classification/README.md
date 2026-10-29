# Week 5: Gesture Validation and Command Supervision

## Transfer the supervision ideas to Go2

Keep the simulation limits in the reference table below. Later, Go2 uses a
different speed profile and supports sideways motion. Compare units, stop
priority, fresh-input requirements, and explicit enabling using the hardware
guide. Explain why a zero request or a transmitted packet alone does not prove
a physical robot has stopped; no physical motion is required this week.

See [Go2 hardware onboarding](../GO2_HARDWARE.md) for the later hardware path.

## Milestone

Turn raw timestamped labels into bounded, interruptible velocity commands. Verify command behavior independently before Week 6 live navigation.

## Reference code

`safety.py` contains pure-Python `Prediction`, `Limits` and `Supervisor` types. A prediction carries a raw label and its monotonic frame-acquisition timestamp. `Supervisor.approve()` returns an approved `(vx, vy, yaw_rate)` tuple and a status reason.

| Rule | Reference behavior |
|---|---|
| Forward bound | 0.25 m/s |
| Lateral velocity | Always zero |
| Turning bound | +/-0.50 rad/s |
| Motion hold | 0.30 s of consistent fresh predictions |
| Frame / dashboard timeout | 0.40 s |
| STOP, UNKNOWN, no hand, multiple hands | Immediate zero request, without motion hold |
| Camera error | No-hand input and zero request |
| Stop button | Latched disarm until explicit Enable motion |

The simulation worker checks input age even if the camera worker stops publishing. Reusing one frame does not satisfy hold time. Invalid, expired or out-of-order input resets the motion candidate. After a stop, a fresh motion sequence must satisfy the hold again.

The reference uses geometric classification without a calibrated confidence value. If adding a confidence-based classifier, document the score and evaluate thresholds separately from MediaPipe detection/tracking thresholds.

## Activities

1. Read `Supervisor.approve()` and draw its state transitions.
2. Run the scripted tests without a webcam.
3. Explain each input and the reason for a zero command.
4. Measure gesture accuracy and rejection behavior across people and lighting. Record expected label, raw label, approved command and timestamp.
5. Compare transition delay and false motion before/after hold filtering.
6. Use the dashboard with motion disabled to inspect labels. Then use `--input mock --scene arena` for an instructor-reviewed command-path check.

## Verification

```powershell
python -m unittest discover -s course/week-05-gesture-classification -v
```

Tests cover hold, repeated frames, stop priority, invalid labels, expiry, dashboard heartbeat, rearming, timestamp anomalies and limits. Live failure-case timing is checked again in Week 6.

## Deliverables

Mapping and bounds table, confusion counts, hold/latency measurements, scripted test output and explanations of stale-input and stop behavior.

Next: [Week 6 integrated navigation dashboard](../week-06-mock-command-mapping/README.md).

## Weekly submission

Submit your individual `week-05/README.md` in your student folder on the
assigned team branch. Put worksheet answers, results, and evidence summaries there.
Any code, CSVs, recordings, or ZIPs named in this lab are local working artifacts,
not additional weekly Git submissions. Optional small media and the final report
follow [the submission and data policy](../SUBMISSIONS.md).
