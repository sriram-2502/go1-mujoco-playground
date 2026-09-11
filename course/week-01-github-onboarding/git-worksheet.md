# Week 1 Git Worksheet

Use this short worksheet during onboarding. Replace values in angle brackets.

## 1. Configure Git

```powershell
git config --global user.name "<Your Name>"
git config --global user.email "<your-github-email>"
git config --global init.defaultBranch main
```

Check the settings:

```powershell
git config --global user.name
git config --global user.email
```

## 2. Clone the course repository

```powershell
cd $HOME\Downloads
git clone https://github.com/sriram-2502/go1-mujoco-playground.git
cd .\go1-mujoco-playground
git remote -v
git status
```

## 3. Inspect `main`

```powershell
git fetch origin
git branch -a
git switch main
git log --oneline -5
```

`main` is the instructor's stable code. Do not push directly to it.

## 4. Enter your team branch

Use the branch assigned by your instructor:

```powershell
git switch --track origin/team-alpha
```

or:

```powershell
git switch --track origin/team-bravo
```

Confirm your branch:

```powershell
git branch --show-current
git status
```

## 5. Commit and push your weekly summary

Copy `weekly-summary-template.md` to
`weekly-summaries/week-01-firstname-lastname.md`, fill out your individual
summary, then run:

```powershell
git add weekly-summaries/week-01-firstname-lastname.md
git status
git commit -m "Add week 01 summary"
git log --oneline -1
git push
```

Refresh your team branch on GitHub and confirm that the file is visible.

## Useful commands

```powershell
git status                 # What changed?
git diff                   # What changed but is not staged?
git log --oneline -5       # Recent commits
git branch -vv             # Current branch and tracking branch
git remote -v              # Connected GitHub repository
```

## Remember

- Work on `team-alpha` or `team-bravo`, not `main`.
- Read `git status` before committing.
- Make small commits with clear messages.
- Never commit passwords, tokens, robot credentials, private videos, or large
  generated files.

