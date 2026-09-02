# Week 1: GitHub onboarding and Go1 baseline

## Milestone

Join the course workflow, access the assigned team branch, and run the existing
Go1 keyboard controller from the instructor-provided `main` code.

This is a two-hour onboarding session. Do not modify the robot controller yet.

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
| 0:00–0:20 | Create or verify a GitHub account and review repository rules | Repository access |
| 0:20–0:45 | Clone the repository and inspect branches | Terminal output |
| 0:45–1:05 | Switch to the assigned team branch | Current branch |
| 1:05–1:40 | Run the existing Go1 keyboard simulation | Screenshot or recording |
| 1:40–1:55 | Make a documentation-only commit | Commit hash |
| 1:55–2:00 | Complete the weekly summary | `week-01.md` |

## Task 1: GitHub access

If you do not already have a GitHub account, create one at
[github.com](https://github.com/). Use an account name you are comfortable using
for course work. Enable two-factor authentication if possible.

Open the public course repository:

<https://github.com/sriram-2502/go1-mujoco-playground>

Do not upload passwords, API keys, robot network credentials, private videos, or
other sensitive data.

## Task 2: Clone the repository

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

## Task 5: Make a documentation-only commit

Create `weekly-summaries/week-01.md` in your team branch using the template
below. Then commit and push it:

```powershell
git add weekly-summaries/week-01.md
git commit -m "Add week 01 onboarding summary"
git push -u origin team-alpha
```

Team Bravo should replace the final branch name with `team-bravo`.

## Weekly summary template

```markdown
# Week 01 Summary

## Team
Names:

## Goal
What were we trying to accomplish?

## What we did
-
-

## Evidence
Commit:
Simulation result:

## What worked
-

## Problem and resolution
-

## What I learned
-

## Next week
-
```

## Completion checklist

- [ ] GitHub account verified or created.
- [ ] Course repository cloned.
- [ ] `main` inspected but not modified.
- [ ] Assigned team branch checked out.
- [ ] Existing Go1 keyboard controller launched.
- [ ] Forward, turning, stop, and reset behavior observed.
- [ ] Week 1 summary committed and pushed to the team branch.

## Deliverables

- Team branch containing `weekly-summaries/week-01.md`.
- Screenshot or short recording of the existing simulation.
- One sentence explaining the difference between `main` and the team branch.

## Next week

Continue to the instructor-provided MuJoCo setup and baseline exercise.

