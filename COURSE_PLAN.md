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

## Week 2 — Go1 Controller Behavior, Control, and Reinforcement Learning

### Topics

- Introduction to MuJoCo
- Robot models, joints, actuators, and sensors
- High-level and low-level robot control
- Pretrained locomotion controllers
- Basic feedback-control concepts
- Reinforcement-learning policy concepts
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

## Week 3 — Webcam Input and Hand Tracking

### Topics

- Webcam image acquisition
- Image coordinates, frame rate, and latency
- Hand landmarks and real-time perception
- Lighting, occlusion, and perception failure cases

### Student Activities

- Capture video from a laptop webcam
- Run the provided hand-landmark detector
- Display landmarks and measure frame rate
- Test lighting, distance, and occlusion
- Save representative examples and document failure cases

### Milestone

Students can acquire webcam frames and visualize a hand reliably enough for the next perception activity.

---

## Week 4 — Gesture Recognition and Temporal Filtering

### Topics

- Gesture features and discrete command vocabularies
- Confidence scores and unknown detections
- Temporal filtering, debouncing, and hold time
- Finite-state machines

### Student Activities

- Run the starter gesture classifier
- Test stop, forward, left, right, and slow-mode gestures
- Add confidence and hold-time checks
- Handle unknown gestures
- Measure false detections and stable recognition time

### Milestone

Students can produce stable symbolic gesture commands from live webcam input.

---

## Week 5 — Gesture-to-Command Control in MuJoCo

### Topics

- Mapping discrete gestures to continuous commands
- Body-frame velocity commands: vx, vy, and yaw
- Command persistence, smoothing, and scaling
- Simulation testing and reproducible experiments

### Student Activities

- Connect validated gesture intent to the existing Go1 command interface
- Run the gesture controller in MuJoCo
- Tune forward and turning speeds
- Add smooth command transitions
- Test stop behavior and input loss in simulation

### Suggested Starter Gestures

- Stop
- Forward
- Turn left
- Turn right
- Slow mode

### Milestone

Students can guide the simulated Go1 with validated gestures by the end of Week 5.

---

## Week 6 — Hardware Interface and Safety Checkout

### Topics

- Simulation-to-hardware interface
- Go1 communication architecture
- Robot health and command heartbeat
- Emergency stop and default-stop behavior
- Hardware operating procedures

### Student Activities

- Compare the simulation and physical command interfaces
- Connect to the physical Go1 under instructor supervision
- Run stationary communication and heartbeat tests
- Verify health monitoring and emergency stop
- Do not enable locomotion until the instructor approves

### Milestone

Students can verify the hardware interface safely without commanding physical motion.

---

## Week 7 — Supervised Hardware Integration

### Topics

- Incremental hardware testing
- Safe operating envelopes
- Simulation-to-real differences
- Stale-command and perception-loss handling
- Structured qualification checklists

### Student Activities

- Test gesture commands at zero or very low speed
- Verify timeout, low-confidence, communication-loss, and emergency-stop behavior
- Compare commanded and measured motion
- Complete the instructor-approved hardware qualification checklist

### Required Safety Tests

Students must demonstrate that the robot stops when:

- No valid gesture has been received recently
- Gesture confidence is below the threshold
- The webcam is unavailable
- Communication is interrupted
- The emergency-stop command is activated
- The requested command exceeds the safe operating limits

### Milestone

Students demonstrate a supervised, bounded gesture-control loop on the physical Go1.

---

## Week 8 — Final Project Definition and Architecture

### Topics

- Final project requirements and team roles
- System architecture and interface contracts
- Mission-control design
- Testable success criteria and safety constraints
- Modular maze and robot-clearance requirements

### Student Activities

- Select a team extension or mission objective
- Draw the complete perception-to-motion architecture
- Define interfaces between gesture, command, safety, camera, and robot modules
- Create a project backlog and test plan

### Milestone

Each team has an approved final-project design, interfaces, backlog, and safety/test plan.

---

## Week 9 — Final Project Implementation

### Topics

- Full-system implementation in simulation
- Mission-control and robot-camera integration
- Logging and operator feedback
- Team-selected design extension

### Student Activities

- Integrate gesture recognition, command generation, safety supervision, and Go1 simulation
- Add the approved team extension
- Run repeatable simulation trials
- Record failures and update the implementation plan

### Milestone

Each team demonstrates its complete project in simulation and has a working test log.

---

## Week 10 — Reliability Testing and Maze Preparation

### Topics

- Repeatability and failure-mode analysis
- Performance metrics and trial logs
- Maze geometry, clearances, and operator procedures

### Student Activities

- Run repeated end-to-end trials
- Measure completion time, latency, false gestures, stops, and resets
- Build and inspect the modular maze
- Test partial navigation in simulation or under instructor direction

### Milestone

Each team has a documented, repeatable system and an instructor-approved demonstration plan.

---

## Week 11 — Supervised Final Demonstration Rehearsal

### Topics

- Final safety review
- Supervised hardware rehearsal
- Technical communication and troubleshooting

### Student Activities

- Pass the hardware and emergency-stop checklist
- Rehearse the complete mission under supervision
- Fix only approved high-priority failures
- Prepare the final demonstration and technical explanation

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

Each team completes a supervised rehearsal and is ready for final evaluation.

---

## Week 12 — Final Project Demonstration and Technical Review

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
