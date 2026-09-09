# Week 1 Summary

## Team and contributors

- Team: `team-alpha` or `team-bravo`
- Names Camden Norris
- Date:9/9/26

## Week 1 goal

What were we trying to accomplish?

## GitHub setup

- GitHub account verified: Yes
- Repository cloned: Yes
- Team branch: Alpha
- Commit containing this summary: Add after committing

## What we did

Describe the main activities you completed.

- Cloned and inspected the GitHub repository
- Learned the difference between the main branch and our team branches
- Set up the environment and run the simulation
- Test basic controls in the simulation

## MuJoCo and Go1 baseline

What did you observe when running the existing keyboard controller?

- Forward command: The up arrow sends a forward velocity command to the robot.
- Backward command:The down arrow sends a backward velocity command.
- Turning command:The left and right arrows command the robot to turn.
- Stop behavior:Pressing Enter sends a zero command and stops the robot.
- Reset behavior: Backspace stops and resets the simulation.

## Evidence

Add links or filenames for screenshots, recordings, terminal output, or other
evidence. Do not commit private videos or sensitive information.

robot video.mp4

## Systems understanding

In your own words, describe how this pipeline works:

```text
input → velocity command → locomotion policy → joint actions → simulated motion
```

The keyboard provides the movement input. This is converted into a velocity command and sent to the locomotion policy. The policy determines the joint actions for the Go1 robot, and MuJoCo simulates the resulting movement.

What are the three high-level command dimensions?

forward/backward velocity, lateral velocity, and turning or angular velocity.

## Open-ended design question

The current keyboard command can persist after a key press. Propose one way to
make input safer, such as a joystick/gamepad interface or a stale-command
timeout.

- Proposed idea: A controller with a stale-command timeout
- How would it detect missing input? It would record the time of the most recent input and if there
were no new input, then the command would zero.
- What should cause the command to become zero? If there was no new input in .25 seconds then the velocity would zero
- What tradeoff would your design create?
If the time was too short, then commands may be cut off, but it would improve responsiveness and safety
## What worked

- The GitHub branch workflow and basic Go1 control structure became clearer after working through the setup and running the existing controller.

## Problem and resolution

What problem did you encounter, and how did you address it?

- One problem was installing all of the required Python dependencies on Windows. Some packages created file paths that exceeded the Windows path-length limitation. I addressed this by enabling long Windows paths and using a shorter Conda environment path.

## What I learned

- I learned how Git branches work and can be edited separately to later be incorporated into a larger bed of code, 
allowing for it to be reviewed and corrected.

## Next week

What would you like to understand or try next?

- I would like to get better at commands and commit more to memory for easier use

