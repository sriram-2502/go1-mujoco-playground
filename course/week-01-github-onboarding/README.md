# Week 1: GitHub onboarding and Go1 baseline

## Milestone

Join the course workflow, access the assigned team branch, and run the existing
Go1 keyboard controller from the instructor-provided `main` code.

This is a two-hour onboarding session. Do not modify the robot controller yet.

## Week 1 in one pass

Complete the work in this order:

1. **Prerequisite:** finish the [Windows 11 setup](windows-setup.md), including
   Git, VS Code, Miniconda, and the course dependencies.
2. **Study:** read the [Control Pipeline](https://dyco-ai.github.io/go1_gesture_tracking/control-pipeline/)
   and [MuJoCo Orientation](https://dyco-ai.github.io/go1_gesture_tracking/mujoco-orientation/).
3. **Run:** fetch the repository, enter `team-alpha` or `team-bravo`, and run
   the existing Go1 MuJoCo Playground keyboard controller.
4. **Question:** propose one safer input idea, such as joystick, voice,
   gestures, or a stale-command timeout.
5. **Submit:** complete your individual Markdown summary and push it to your
   team branch.

The expected Week 1 code change is documentation only. Ask the instructor
before pushing any controller or simulation code change.

## The standard weekly workflow

Most weeks follow this pattern:

1. Fetch the latest instructor materials.
2. Read the week's activity page and the relevant code.
3. Complete the worksheet or experiment requested for the week.
4. Push the worksheet and documentation to your team branch.
5. Make code changes only when the activity requires them or after discussing
   the proposed change with the instructor.

Documentation is the default deliverable. If you are confident that a code
change is useful, ask for instructor consent before pushing it. After approval,
make the change on your team branch, explain it in your weekly summary, and
include evidence that the baseline still works.

## Learning objectives

By the end of this week, you should be able to:

- access GitHub and the public course repository;
- explain the difference between `main` and a team branch;
- clone the repository and switch to the assigned team branch;
- run the existing Go1 simulation; and
- record reproducible evidence in a one-page weekly summary.

## Team branches

The instructor maintains stable code in `main`. Students work on their assigned
branch:

```text
team-alpha
team-bravo
```

Students may push to their team branch. Do not push directly to `main`.

## Two-hour schedule

| Time | Activity | Evidence |
|---:|---|---|
| 0:00–0:15 | Read the control-pipeline and MuJoCo orientation pages | One systems question |
| 0:15–0:35 | Create or verify a GitHub account and review repository rules | Repository access |
| 0:35–0:55 | Clone the repository and enter the team branch | Current branch |
| 0:55–1:25 | Run the existing Go1 keyboard simulation | Screenshot or recording |
| 1:25–1:45 | Make a documentation-only commit | Commit hash |
| 1:45–2:00 | Complete the individual summary and design question | Your named Markdown file |

## Task 1: GitHub access

Use the companion [Week 1 Git Worksheet](git-worksheet.md) for the commands
used during this session.

Before coding, read the [Control Pipeline overview](https://dyco-ai.github.io/go1_gesture_tracking/control-pipeline/)
and [MuJoCo Orientation](https://dyco-ai.github.io/go1_gesture_tracking/mujoco-orientation/).

If you do not already have a GitHub account, create one at
[github.com](https://github.com/). Use an account name you are comfortable using
for course work. Enable two-factor authentication if possible.

Open the public course repository:

<https://github.com/sriram-2502/go1-mujoco-playground>

Do not upload passwords, API keys, robot network credentials, private videos, or
other sensitive data.

## Task 2: Clone the repository

If Git and Miniconda are not installed, first follow the
[Windows 11 setup sheet](windows-setup.md). It covers the clean installation
of Git for Windows, Miniconda, the course environment, and MuJoCo dependencies.

Use **Git Bash** or **Miniconda Prompt**:

```powershell
cd $HOME\Downloads
git clone https://github.com/sriram-2502/go1-mujoco-playground.git
cd .\go1-mujoco-playground
git remote -v
git status
```

The repository should be clean after cloning.

## Task 3: Inspect `main` and enter your team branch

```powershell
git fetch origin
git branch -a
git switch main
git pull --ff-only origin main
git log --oneline -5
```

Switch to the branch assigned by the instructor:

```powershell
git switch team-alpha
```

Team Bravo should use:

```powershell
git switch team-bravo
```

Confirm the active branch:

```powershell
git branch --show-current
git status
```

Expected branch names are `team-alpha` or `team-bravo`. If the branch does not
exist, stop and ask the instructor rather than creating a different branch.

## Task 4: Run the existing Go1 code

The instructor has already prepared the baseline code. From the repository root:

```powershell
python .\mujoco_playground\experimental\sim2sim\play_go1_keyboard.py
```

Click inside the MuJoCo viewer so it receives keyboard input.

| Key | Action |
|---|---|
| Up arrow | Forward |
| Down arrow | Backward |
| Left arrow | Turn left |
| Right arrow | Turn right |
| Enter | Stop |
| Backspace | Stop and reset |

For this first session, do not change controller parameters or simulation code.

## Open-ended systems question

The baseline keyboard controller stores the last command, so an arrow-key press
can continue producing motion after the key is released. Enter explicitly sends
a zero command. Think about how you would improve this behavior without changing
the locomotion policy:

- Would a joystick or gamepad be a better input device?
- How would you detect that the input source stopped updating?
- What timeout should cause the command to return to zero?
- How would you keep the stop command higher priority than motion?

For your weekly summary, sketch one possible design and explain the tradeoff
between responsiveness and accidental stopping. Do not connect a physical
joystick or robot yet.

## Task 5: Make a documentation-only commit

Copy [the Week 1 summary template](weekly-summary-template.md) into your team
branch as `weekly-summaries/week-01-firstname-lastname.md`. Each student submits
an individual summary. Fill it out with your own findings, then commit and push
it:

```powershell
git add weekly-summaries/week-01-firstname-lastname.md
git commit -m "Add week 01 onboarding summary"
git push -u origin team-alpha
```

Team Bravo should replace the final branch name with `team-bravo`.

## Completion checklist

- [ ] GitHub account verified or created.
- [ ] Course repository cloned.
- [ ] `main` inspected but not modified.
- [ ] Assigned team branch checked out.
- [ ] Existing Go1 keyboard controller launched.
- [ ] Forward, turning, stop, and reset behavior observed.
- [ ] Week 1 summary committed and pushed to the team branch.

## Deliverables

- Team branch containing each student's `weekly-summaries/week-01-firstname-lastname.md`.
- Screenshot or short recording of the existing simulation.
- One sentence explaining the difference between `main` and the team branch.

## Next week

Continue to the instructor-provided MuJoCo setup and baseline exercise.

