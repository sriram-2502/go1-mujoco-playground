# Week 8: Safety behavior and automated tests

## Milestone

Turn safety expectations into executable tests that run without a webcam,
simulator window, or physical robot.

## Learning objectives

- Translate a safety statement into a testable requirement.
- Write normal, boundary, and failure-case tests.
- Use injected timestamps to test timeout behavior repeatably.
- Produce evidence that stop behavior overrides motion.

## Prerequisites

- Week 6 mapper and Week 7 simulated integration complete
- Command limits and timeouts stored in configuration
- Team has a non-actuating mock command sink

## Task 1: Write requirements

Give each requirement an identifier. At minimum include:

| ID | Requirement |
|---|---|
| SAF-01 | `STOP` always produces zero command. |
| SAF-02 | `UNKNOWN` and no-hand input produce zero command. |
| SAF-03 | A stale input produces zero command within the timeout. |
| SAF-04 | Every command component remains within its configured bound. |
| SAF-05 | Stop overrides a pending or previous motion request. |
| SAF-06 | Motion does not resume without new validated intent. |

Make each statement specific enough that a test can pass or fail it.

## Task 2: Build a test table

For each requirement, include:

- initial state;
- input sequence and timestamps;
- expected output;
- actual output; and
- pass/fail result.

Include values just below, exactly at, and just above every threshold or limit.

## Task 3: Automate pure command tests

Write tests around the validator and mapper without opening a camera or MuJoCo.
Pass a controlled time value into timeout logic instead of making tests sleep.
This keeps tests fast and repeatable.

Run tests using the framework selected by the instructor and save the complete
terminal result.

## Task 4: Run integration fault injection

With the Go1 only in simulation, intentionally create:

1. missing hand input;
2. low-confidence input;
3. delayed input;
4. rapidly alternating labels;
5. out-of-range command requests; and
6. source shutdown during motion.

Measure time to zero command for each applicable case.

## Task 5: Review defaults

Inspect configuration while the system starts, reloads, or encounters a missing
value. Safe defaults must not enable motion. A missing configuration must fail
closed with a clear error or zero command.

## Task 6: Conduct a peer safety review

Another team reviews the requirements, tests, and one fault-injection run. The
reviewing team should try to find an untested path to persistent motion. Record
the issue, response, and retest result.

## Completion checklist

- [ ] Safety requirements have identifiers and measurable outcomes.
- [ ] Boundary cases exist for every threshold and command limit.
- [ ] Automated command tests pass.
- [ ] Six integration faults tested in simulation.
- [ ] Safe-default behavior verified.
- [ ] Peer review completed and findings addressed.
- [ ] Hardware output remains disabled.

## Deliverables

- Safety requirements and traceability table
- Automated test source and terminal results
- Fault-injection measurements
- Peer-review record

## Next week

Continue to [Week 9: Integrated system
evaluation](../week-09-system-evaluation/README.md).
