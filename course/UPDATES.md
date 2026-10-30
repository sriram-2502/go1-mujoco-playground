# Receive instructor code updates on your team branch

Instructor code is published on `main`; student reports live on `team-alpha` or
`team-bravo`. Pulling `main` while on `main` does not update a different branch.
Before running a new lab, refresh your assigned team branch with the instructor.
This imports the approved baseline; it does not authorize uploading code experiments.

1. Run `git status`. Save your work. Commit only the intended README report and
   permitted small evidence files; keep experimental source changes local and
   preserve them separately before merging. Do not continue with a dirty tree.
2. Switch to your existing assigned branch and fetch. For Team Alpha:

```powershell
git switch team-alpha
git pull --ff-only origin team-alpha
git fetch origin
git merge --no-edit origin/main
git status
```

Team Bravo substitutes `team-bravo` in both commands. For an initial clone,
create the tracking checkout using the Week 1 instructions first. Do not create
a personal branch, reset your team branch, or force-push.

3. If Git reports a conflict, a divergent team pull, or would overwrite local
   work, stop and ask the instructor to reconcile it. Preserve existing student
   folders; do not resolve a conflict by deleting another student's report.
4. After the instructor checks the result, run the lab checkout and push the
   approved baseline merge plus your intended README report to the same team
   branch. Check staged files; do not add unrelated experimental code.

The instructor may instead refresh the shared team branches before class, in
which case the team pull already brings in the baseline. Check `git log --oneline -5`
and record the version used in your report.

The physical Go2 application is a separate checkout. Follow its own
[update instructions](https://github.com/sriram-2502/go2-webrtc-gesture-nav#get-instructor-updates);
do not merge hardware application files into the playground.
