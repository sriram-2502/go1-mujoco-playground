# Student submissions and local experiment data

Use your assigned `team-alpha` or `team-bravo` branch. Each student has a unique
`first-last` folder on that shared branch. Weekly submissions are README reports;
code experiments remain local unless the instructor explicitly requests a code contribution.
There is no automatic switch to code submissions in Week 5 or Week 6.
An instructor-reviewed [baseline update](UPDATES.md) imports approved course code
into the team branch; it is separate from student code experiments.

```text
course/student-work/<team>/<first-last>/
  week-01/README.md
  week-02/README.md
  ...
  week-12/README.md
  week-XX/media/demo.mp4       optional compressed evidence
  final-report/README.md
```

Use the same student folder throughout the course. Previously submitted
`weekly-summaries/week-XX.md` files can stay in place; new work uses the layout
above. Do not move or overwrite another student's work.

## What to write each week

Copy [the weekly report template](WEEKLY_REPORT_TEMPLATE.md) into that week's
`README.md`. Record the goal, activities, results, a small results table, problems,
what you learned, and next steps. Put answers to the weekly worksheet and links
to evidence in this report. Source files named in a lab are working artifacts,
not additional Git submissions. For hardware weeks, distinguish requested and
measured velocities and simulated, stationary, and supervised physical evidence.

An honest incomplete result and explanation are useful evidence. Weekly reports
do not need a polished video, and the same report format applies to hardware labs.

## Optional small media

README-only is sufficient. If useful, add a short compressed MP4 or GIF under
that week's `media/` folder and link it with a relative path. Use a normal Markdown
link for MP4 and an image link for GIF. Default budget: **5 MB per file and 10 MB
total optional media per student per week**. Check actual file size before staging;
shorter clips, lower resolution, and lower frame rate help. GIF can exceed MP4 size.
Use only consented, sanitized footage; a skeleton/dashboard crop usually suffices.

The ignore rules allow MP4/GIF only in this designated weekly media directory.
Git cannot enforce this size budget through `.gitignore`; inspect `git diff --cached --stat`
and `git status` before committing. Do not use `git add .` or force-add raw data.

## Store full runs locally

Save recording ZIPs, full-resolution videos, CSV/JSONL telemetry, voxel data,
and intermediate exports outside the repositories, for example:

```text
C:/Users/<you>/go2-course-data/<team>/<first-last>/<date>/<run-id>/
```

Keep a local backup on instructor-approved storage. A browser download alone is
not a backup. Raw experiment data is not a weekly Git deliverable. Ignored
`data/`, `recordings/`, and `runs/` folders are a fallback, not permission to
publish private data. Ignore rules do not remove files already tracked by Git.

In the weekly README, list run IDs, software/firmware version, settings, avoidance
state, conditions, results, and interventions. Copy only compact summary tables
or small sanitized figures into the report. A local filename records provenance;
it is not a link classmates can open. Use the instructor's approved channel if
full data needs to be shared. Do not add a public download link by default.

## End-of-course report

Write `final-report/README.md` in your student folder, bringing together the
question, methods, architecture, experiment conditions, aggregate results,
limitations, and lessons learned. Reference weekly reports and local run IDs.
Keep the full data local; arrange instructor access separately if requested.

## Hardware access and networking

Ask the instructor for the assigned Go2's AES key and Wi-Fi credentials. Never
put keys, passwords, tokens, credential screenshots, or secret-bearing logs in
README files, media, code, or Git history. Do not use sample keys from another robot.

Install dependencies using an internet connection first. For the robot session,
join the **assigned Go2 Wi-Fi hotspot**, then use **192.168.12.1** as the default
WebRTC endpoint. Do not use Clemson campus Wi-Fi as the robot connection path:
campus firewall/client-isolation policies can interfere, and the robot's private
hotspot endpoint is reached through its own network. If this fails, ask the
instructor; do not disable campus or Windows security controls. The browser UI
itself runs locally. The robot hotspot may have no internet access.

See [Go2 hardware onboarding](GO2_HARDWARE.md) for complete setup and checks.
