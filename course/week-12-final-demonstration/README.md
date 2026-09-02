# Week 12: Final demonstration and communication

## Milestone

Present a repeatable final demonstration and explain the engineering evidence,
safety decisions, limitations, and future work behind it.

## Learning objectives

- Plan a demonstration with measurable success and abort criteria.
- Communicate a multidisciplinary system to technical and general audiences.
- Support design claims with recorded tests rather than anecdotes.
- Identify limitations and propose responsible next steps.

## Prerequisites

- Weeks 1–10 complete
- Week 11 hardware checkout complete if the final uses the physical Go1
- Instructor approves the final demonstration mode and test area
- A simulation-only final remains acceptable when hardware approval is absent

## Task 1: Freeze the final system

Record:

- Git commit and branch;
- Conda/package environment;
- model and configuration versions;
- command limits and timeout values;
- hardware/software architecture; and
- known limitations.

After the freeze, only instructor-approved critical fixes are allowed. Retest any
changed component.

## Task 2: Define success

Create a demonstration scorecard. Example criteria include:

- all approved gestures recognized;
- no false motion during unknown input;
- stop succeeds within the approved time;
- command limits are never exceeded;
- required course or maze sequence is completed; and
- system remains recoverable after a rejected gesture.

Define abort criteria and a fallback simulation demonstration.

## Task 3: Rehearse roles

Assign a presenter, operator, safety observer, data observer, and backup. Rehearse
normal operation, a rejected gesture, a stop, and an abort. Every team member
should be able to explain the full architecture and their contribution.

## Task 4: Prepare the technical story

Your poster or presentation should include:

1. motivation and user need;
2. system architecture;
3. gesture vocabulary and command mapping;
4. simulation and hardware progression;
5. safety requirements and evidence;
6. accuracy and latency results;
7. one failure and how the team addressed it;
8. limitations; and
9. future work.

Use plots with labeled axes, units, sample counts, and readable captions.

## Task 5: Run the final demonstration

Follow the approved checklist exactly. If using hardware, the instructor must be
present and Week 11 safety rules remain active. A safe abort is a successful use
of the safety system, not a reason to hide the result.

## Task 6: Archive and reflect

Save final code, configuration, test data, plots, documentation, and a short demo
video in instructor-approved locations. Do not commit Conda environments, private
videos, credentials, or large unapproved artifacts.

Each student writes a short reflection:

- What did I contribute?
- What technical idea can I now explain?
- What evidence most changed our design?
- What would I do next with more time?

## Completion checklist

- [ ] Final version and configuration frozen.
- [ ] Success and abort criteria documented.
- [ ] Team roles rehearsed.
- [ ] Presentation includes evidence, safety, and limitations.
- [ ] Approved demonstration completed or safely aborted.
- [ ] Code, results, and documentation archived.
- [ ] Individual reflections completed.

## Deliverables

- Final demonstration or simulation fallback
- Poster or technical presentation
- Final test scorecard and selected raw evidence
- Demonstration video
- Team archive and individual reflections

## Course closeout

Return to the [course overview](../../README.md) and review the course outcomes.
For each outcome, identify one artifact that demonstrates your progress.
