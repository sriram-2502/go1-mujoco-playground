# Gesture-Guided Quadruped Navigation  
## 12-Week Creative Inquiry Course Plan

## Course Overview

This course introduces undergraduate students to robotics, control design, computer vision, human–robot interaction, and systems integration through a hands-on quadruped robotics project.

Students will develop a gesture-guided control system for a Unitree Go1 robot. The project begins in MuJoCo simulation and progresses toward supervised deployment on the physical robot. During the final challenge, student teams will use hand gestures and a robot-mounted camera feed to guide the Go1 through a modular maze.

The instructional team will provide the core infrastructure required to operate the simulation and physical robot. This includes the pretrained locomotion controller, MuJoCo environment, hardware communication interface, robot-camera stream, webcam pipeline, safety framework, and deployment tools.

Students will focus on the higher-level robotics problems of:

- Perception and gesture recognition
- Command generation
- Coordinate frames and velocity control
- Filtering and state machines
- Safety supervision
- Simulation-to-hardware deployment
- Systems integration
- Experimental testing
- Team-based engineering design

The course emphasizes safe and structured robotics development rather than low-level motor control or locomotion-policy training.

---

# Course Architecture

The course project follows the system architecture:

```text
Laptop Webcam
      |
      v
Hand Landmark Detection
      |
      v
Gesture Classification
      |
      v
Gesture Filtering and State Machine
      |
      v
Velocity Command Generation
      |
      v
Safety Supervisor
      |
      +----------------------+
      |                      |
      v                      v
MuJoCo Go1 Interface   Physical Go1 Interface
```

The simulation and hardware systems use the same high-level command representation:

```python
VelocityCommand(
    vx=0.3,
    vy=0.0,
    yaw_rate=0.0,
)
```

Only the final robot interface changes between simulation and hardware.

---

# Weekly Plan

## Week 1 — Introduction to Robotics Systems

### Topics

- Overview of the Unitree Go1 platform
- Components of a robotic system
- Sensing, computation, control, and actuation
- Course software architecture
- Git and collaborative development
- Laboratory and hardware safety

### Student Activities

- Install the course software environment
- Clone the course repository
- Run the installation verification script
- Explore the starter-code structure
- Run a basic MuJoCo example
- Review the course safety procedures

### Milestone

Students can launch the course environment and explain the major components of the gesture-guided robot system.

---

## Week 2 — Go1 Simulation and Locomotion

### Topics

- Introduction to MuJoCo
- Robot models, joints, actuators, and sensors
- High-level and low-level robot control
- Pretrained locomotion controllers
- Simulation as a robotics development tool

### Student Activities

- Launch the simulated Go1
- Run the provided locomotion controller
- Inspect the robot state
- Observe the response to velocity commands
- Reset the simulation
- Compare commanded and measured motion

### Milestone

Students can run the pretrained Go1 locomotion controller and explain how high-level velocity commands produce robot movement.

---

## Week 3 — Velocity Commands and Coordinate Frames

### Topics

- Robot body frame
- World frame
- Linear velocity
- Angular velocity
- Forward, backward, and turning commands
- Command saturation
- Emergency stopping

### Student Activities

- Use the provided keyboard controller
- Drive the simulated Go1
- Modify safe velocity limits
- Visualize commanded and measured velocities
- Complete a command-saturation function
- Test the emergency-stop behavior

### Milestone

Students can safely control the simulated Go1 using keyboard commands.

---

## Week 4 — Webcam Input and Hand Tracking

### Topics

- Camera image acquisition
- Image coordinates
- Frame rate and latency
- Hand landmarks
- Real-time perception pipelines
- Perception noise and failure cases

### Student Activities

- Capture video from a laptop webcam
- Run the provided hand-landmark detector
- Display detected landmarks
- Measure the camera frame rate
- Investigate the effects of lighting and occlusion
- Save sample gesture images for testing

### Milestone

Students can reliably detect and visualize a hand using a laptop webcam.

---

## Week 5 — Gesture Recognition and Temporal Filtering

### Topics

- Gesture classification
- Discrete command vocabularies
- Confidence scores
- Temporal filtering
- Debouncing
- Gesture hold time
- Finite-state machines

### Student Activities

- Complete gesture-classification logic
- Test the starter gesture set
- Add confidence thresholds
- Implement gesture hold-time logic
- Handle unknown gestures
- Evaluate false detections

### Suggested Starter Gestures

- Stop
- Forward
- Turn left
- Turn right
- Slow mode

### Milestone

Students can produce stable symbolic gesture commands from live webcam input.

---

## Week 6 — Gesture-to-Motion Control

### Topics

- Mapping discrete gestures to continuous commands
- Motion primitives
- Command persistence
- Command smoothing
- Velocity scaling
- Human–robot interaction

### Student Activities

- Map gestures to Go1 velocity commands
- Connect gesture output to the simulated robot
- Tune forward speed
- Tune turning speed
- Add smooth command transitions
- Test movement and stopping behavior

### Milestone

Students can control the simulated Go1 using hand gestures.

---

## Week 7 — Safety Supervisor and Fault Handling

### Topics

- Safety layers in robotic systems
- Fail-safe behavior
- Stale-command detection
- Perception-loss handling
- Communication-loss handling
- Velocity and acceleration limits
- Software emergency stops

### Student Activities

- Complete the safety-supervisor functions
- Add a command timeout
- Add low-confidence rejection
- Add acceleration limiting
- Add turn-rate limiting
- Test emergency-stop behavior
- Verify that perception loss produces a stop command

### Required Safety Tests

Students must demonstrate that the robot stops when:

- No valid gesture has been received recently
- Gesture confidence is below the threshold
- The webcam is unavailable
- Communication is interrupted
- The emergency-stop command is activated
- The requested command exceeds the safe operating limits

### Milestone

Students demonstrate that the simulated robot safely handles the required fault conditions.

---

## Week 8 — Physical Go1 and Camera Integration

### Topics

- Simulation-to-hardware transition
- Go1 communication architecture
- Network configuration
- Robot health monitoring
- Robot-mounted camera streaming
- Hardware operating procedures

### Student Activities

- Connect to the physical Go1 under instructor supervision
- Display the robot-mounted camera feed
- Run a stationary communication test
- Verify the command heartbeat
- Test the physical emergency stop
- Compare the simulation and hardware interfaces

### Milestone

Students can connect to the Go1, view the robot camera, and verify safe communication without moving the robot.

---

## Week 9 — Hardware Qualification

### Topics

- Structured hardware testing
- Incremental validation
- Safe operating envelopes
- Simulation-to-real differences
- Experimental checklists
- Data collection

### Student Activities

- Perform a low-speed forward-motion test
- Perform a controlled stop test
- Perform left- and right-turn tests
- Test stale-command stopping
- Test perception-loss stopping
- Record commanded and measured behavior
- Complete the hardware qualification checklist

### Qualification Sequence

Each team must pass:

1. Stationary communication test
2. Emergency-stop test
3. Forward-motion test
4. Controlled-stop test
5. Left-turn test
6. Right-turn test
7. Perception-loss test
8. Communication-loss test

### Milestone

Each team passes the required Go1 hardware qualification.

---

## Week 10 — Mission-Control Integration and Maze Construction

### Topics

- Full-system integration
- Operator feedback
- Robot-camera navigation
- Maze geometry
- Robot clearances
- Logging and performance metrics
- Human–robot teaming

### Student Activities

- Integrate the webcam pipeline
- Integrate gesture detection
- Integrate command generation
- Integrate safety supervision
- Display the robot-mounted camera feed
- Build a modular maze
- Test corridor widths and turn clearances
- Navigate a partial maze

### Milestone

Students complete a partial maze using the integrated gesture-guided Go1 system.

---

## Week 11 — Reliability Testing and Team Extension

### Topics

- Repeatability
- Failure-mode analysis
- Performance evaluation
- Parameter tuning
- Engineering iteration
- Experimental validation

### Student Activities

- Run repeated maze trials
- Record completion time
- Record false gesture commands
- Record safety stops
- Record collisions and manual resets
- Identify common failure modes
- Tune gesture thresholds
- Tune velocity limits
- Complete one team-selected extension

### Possible Team Extensions

- Add an additional gesture
- Add slow and normal driving modes
- Improve the mission-control dashboard
- Add obstacle-based stopping
- Add adaptive speed scaling
- Improve gesture filtering
- Add trial replay tools
- Add automatic performance summaries
- Add sound or visual operator feedback

### Milestone

Each team demonstrates repeatable performance and documents at least one design improvement.

---

## Week 12 — Physical Maze Competition and Technical Review

### Activities

- Pre-run hardware inspection
- Final safety qualification
- Supervised maze competition
- Technical presentation
- Team reflection
- System performance review

### Competition Objective

Teams must guide the physical Go1 through a modular maze using:

- Hand gestures
- The laptop webcam
- The mission-control interface
- The robot-mounted camera feed
- The student-developed command and safety logic

Students should operate from a designated mission-control location and should not rely on direct line-of-sight navigation.

### Competition Evaluation

Teams may be evaluated using:

- Successful maze completion
- Safe robot behavior
- Gesture-recognition reliability
- Number of collisions
- Number of manual resets
- Number of safety violations
- Navigation efficiency
- Quality of technical explanation
- Quality of experimental documentation
- Teamwork

### Milestone

Students demonstrate an integrated robotic system combining perception, command generation, control, safety, simulation, hardware deployment, and experimental validation.

---

# Project Scope

## Instructor-Provided Infrastructure

The instructional team will provide:

- Pretrained Go1 locomotion controller
- MuJoCo Go1 model
- Simulation environment
- Simulation command interface
- Physical Go1 communication interface
- Robot-camera streaming interface
- Webcam capture pipeline
- Hand-landmark detection
- Basic mission-control dashboard
- Emergency-stop infrastructure
- Hardware deployment scripts
- Logging utilities
- Example unit tests
- Modular maze materials
- Tested reference implementation

## Student-Developed Components

Students will develop, complete, or tune:

- Gesture definitions
- Gesture-classification logic
- Confidence thresholds
- Temporal filtering
- Gesture state machine
- Gesture-to-command mappings
- Velocity limits
- Acceleration limits
- Command smoothing
- Safety-supervisor behavior
- Dashboard improvements
- Test procedures
- Performance analysis
- Team-selected extension
- Final system integration

---

# Required Course Deliverables

Each team will submit:

1. Completed weekly lab exercises
2. Working gesture-recognition module
3. Working gesture-to-command module
4. Working safety-supervisor module
5. Simulation demonstration
6. Hardware qualification checklist
7. Integrated maze-navigation demonstration
8. Source code repository
9. Trial logs and performance analysis
10. Final technical presentation
11. Short final report or design summary

---

# Expected Learning Outcomes

By the end of the course, students should be able to:

1. Explain how sensing, perception, control, and actuation interact in a robotic system.
2. Describe the difference between high-level motion commands and low-level actuator control.
3. Use simulation to test robot-control software before hardware deployment.
4. Interpret robot position, orientation, and velocity data.
5. Apply body-frame and world-frame coordinate concepts.
6. Translate human gestures into high-level robot commands.
7. Apply velocity saturation and acceleration limiting.
8. Implement simple filters and finite-state machines.
9. Design fail-safe behaviors for uncertain or missing sensor information.
10. Design fail-safe behaviors for stale commands and communication faults.
11. Integrate perception, command, simulation, and hardware subsystems.
12. Conduct structured robotics experiments.
13. Interpret logged data and identify system failure modes.
14. Improve system reliability through engineering iteration.
15. Safely deploy a high-level controller on a physical quadruped robot.
16. Work effectively in a small engineering team.
17. Communicate technical design decisions through demonstrations and documentation.

---

# Completion Levels

To account for hardware availability and unexpected equipment issues, the course includes three completion levels.

## Level 1 — Required

Complete gesture-guided Go1 navigation in simulation.

## Level 2 — Expected

Deploy the system to the physical Go1 and pass the hardware qualification tests.

## Level 3 — Final Challenge

Complete the physical maze using gestures and the robot-mounted camera feed.

Simulation completion remains the required baseline for all teams.
