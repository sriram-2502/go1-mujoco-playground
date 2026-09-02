# Starter Code and Repository Structure

## Overview

This document describes the software infrastructure that will be provided to students for the Gesture-Guided Quadruped Navigation course.

The objective of the starter code is to give students a reliable robotics platform without requiring them to build low-level locomotion, network communication, camera transport, or hardware drivers from scratch.

Students will work within the provided architecture to develop gesture recognition, command logic, safety behaviors, testing procedures, and system improvements.

---

# Design Principles

The starter code should follow these principles:

1. Simulation and hardware should use the same high-level command format.
2. Low-level locomotion and robot communication should be hidden behind simple interfaces.
3. Every major subsystem should be testable independently.
4. Keyboard input should be available before gesture input.
5. Mock gesture input should be available for automated testing.
6. Safety logic should be separated from command-generation logic.
7. Hardware operation should require explicit enable and qualification steps.
8. Configuration values should be stored outside the main Python code.
9. Logging should be enabled for both simulation and hardware trials.
10. Student TODO sections should be clearly identified.

---

# Recommended Repository Structure

```text
go1-mujoco-playground/
|
├── COURSE_PLAN.md
├── STARTER_CODE.md
├── README.md
|
├── ci_course/
│   ├── __init__.py
│   ├── README.md
│   ├── requirements-course.txt
│   │
│   ├── configs/
│   │   ├── default.yaml
│   │   ├── simulation.yaml
│   │   ├── hardware.yaml
│   │   └── safe_limits.yaml
│   │
│   ├── mission_control/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── command_types.py
│   │   ├── gesture_classifier.py
│   │   ├── gesture_filter.py
│   │   ├── command_manager.py
│   │   ├── safety_supervisor.py
│   │   ├── dashboard.py
│   │   └── logger.py
│   │
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── go1_sim_interface.py
│   │   ├── go1_hardware_interface.py
│   │   ├── keyboard_source.py
│   │   ├── mock_gesture_source.py
│   │   ├── webcam_source.py
│   │   └── robot_camera.py
│   │
│   ├── environments/
│   │   ├── flat_world.xml
│   │   ├── mini_course.xml
│   │   └── maze_world.xml
│   │
│   ├── labs/
│   │   ├── week_01_setup/
│   │   ├── week_02_simulation/
│   │   ├── week_03_velocity_control/
│   │   ├── week_04_hand_tracking/
│   │   ├── week_05_gesture_filtering/
│   │   ├── week_06_gesture_control/
│   │   ├── week_07_safety/
│   │   ├── week_08_hardware/
│   │   ├── week_09_qualification/
│   │   ├── week_10_maze/
│   │   └── week_11_testing/
│   │
│   ├── scripts/
│   │   ├── check_install.py
│   │   ├── run_keyboard_demo.py
│   │   ├── run_mock_gesture_demo.py
│   │   ├── run_gesture_demo.py
│   │   ├── run_hardware_check.py
│   │   ├── run_camera_viewer.py
│   │   └── run_maze_trial.py
│   │
│   └── tests/
│       ├── test_gesture_classifier.py
│       ├── test_gesture_filter.py
│       ├── test_command_manager.py
│       ├── test_safety_supervisor.py
│       └── test_command_timeout.py
│
└── existing MuJoCo Playground files
```

---

# 1. Course Launcher

Provide a single entry point for launching the full system.

```bash
python -m ci_course.mission_control.main
```

The launcher should support command-line arguments such as:

```bash
python -m ci_course.mission_control.main \
    --robot simulation \
    --input keyboard \
    --config ci_course/configs/simulation.yaml
```

Example modes:

```text
--robot simulation
--robot hardware

--input keyboard
--input mock
--input gesture
```

The launcher should:

- Load the selected configuration
- Create the input source
- Create the robot interface
- Create the safety supervisor
- Create the dashboard
- Start the logging system
- Run the control loop
- Stop the robot safely when the program exits

---

# 2. Common Command Types

Provide common data structures that are shared by all subsystems.

```python
from dataclasses import dataclass
from enum import Enum
import time


class GestureLabel(Enum):
    UNKNOWN = "unknown"
    STOP = "stop"
    FORWARD = "forward"
    BACKWARD = "backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    SLOW = "slow"


class CommandMode(Enum):
    STOP = "stop"
    VELOCITY = "velocity"


@dataclass
class GesturePrediction:
    label: GestureLabel
    confidence: float
    timestamp: float

    @classmethod
    def unknown(cls) -> "GesturePrediction":
        return cls(
            label=GestureLabel.UNKNOWN,
            confidence=0.0,
            timestamp=time.monotonic(),
        )


@dataclass
class RobotCommand:
    mode: CommandMode
    vx: float = 0.0
    vy: float = 0.0
    yaw_rate: float = 0.0
    timestamp: float = 0.0
    source: str = "unknown"
    confidence: float = 1.0

    @classmethod
    def stop(cls, source: str = "system") -> "RobotCommand":
        return cls(
            mode=CommandMode.STOP,
            vx=0.0,
            vy=0.0,
            yaw_rate=0.0,
            timestamp=time.monotonic(),
            source=source,
            confidence=1.0,
        )


@dataclass
class RobotState:
    timestamp: float
    position_x: float = 0.0
    position_y: float = 0.0
    yaw: float = 0.0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    yaw_rate: float = 0.0
    connected: bool = False
    enabled: bool = False
```

Students should use these shared types rather than passing unstructured lists between modules.

---

# 3. Go1 Simulation Interface

Provide a complete simulation adapter that hides the MuJoCo environment and locomotion-policy internals.

```python
class Go1SimInterface:
    def __init__(self, config):
        self.config = config
        self.connected = False
        self.enabled = False

    def connect(self) -> None:
        """Initialize the MuJoCo environment and load the policy."""
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the robot and simulation environment."""
        raise NotImplementedError

    def enable(self) -> None:
        """Enable command processing."""
        self.enabled = True

    def send_velocity_command(
        self,
        vx: float,
        vy: float,
        yaw_rate: float,
    ) -> None:
        """Send a high-level velocity command to the locomotion controller."""
        raise NotImplementedError

    def get_robot_state(self):
        """Return the latest simulated robot state."""
        raise NotImplementedError

    def render(self) -> None:
        """Update the simulation visualization."""
        raise NotImplementedError

    def stop(self) -> None:
        """Send a zero-velocity command."""
        self.send_velocity_command(0.0, 0.0, 0.0)

    def disconnect(self) -> None:
        """Close the simulation safely."""
        self.stop()
        self.connected = False
        self.enabled = False
```

The instructional team should provide the implementation of this interface.

Students should not modify the low-level locomotion policy during the main course project.

---

# 4. Go1 Hardware Interface

Provide a tested hardware adapter with an interface similar to the simulation adapter.

```python
class Go1HardwareInterface:
    def __init__(self, config):
        self.config = config
        self.connected = False
        self.enabled = False

    def connect(self) -> None:
        """Connect to the physical Go1."""
        raise NotImplementedError

    def enable(self) -> None:
        """Enable robot motion after safety checks."""
        raise NotImplementedError

    def send_velocity_command(
        self,
        vx: float,
        vy: float,
        yaw_rate: float,
    ) -> None:
        """Send a high-level velocity command to the physical robot."""
        raise NotImplementedError

    def get_robot_state(self):
        """Return the latest physical robot state."""
        raise NotImplementedError

    def stop(self) -> None:
        """Send a safe stop command."""
        raise NotImplementedError

    def disconnect(self) -> None:
        """Stop and disconnect from the robot."""
        self.stop()
        self.connected = False
        self.enabled = False
```

The instructional team should provide:

- Unitree communication code
- Network configuration
- Connection monitoring
- Command heartbeat
- Hardware-level velocity limits
- Emergency-stop support
- Robot-state decoding
- Safe disconnect behavior

Students should interact only with the high-level interface.

---

# 5. Keyboard Command Source

Provide a complete keyboard controller for early simulation development.

Recommended controls:

```text
W       Move forward
S       Move backward
A       Turn left
D       Turn right
Space   Stop
Escape  Emergency stop
R       Reset simulation
```

Example interface:

```python
class KeyboardCommandSource:
    def __init__(self, config):
        self.config = config

    def update(self):
        """Read keyboard input and return a RobotCommand."""
        raise NotImplementedError

    def close(self) -> None:
        """Release keyboard or window resources."""
        pass
```

This module should be fully implemented by the instructional team.

It allows students to test:

- The simulation interface
- Velocity commands
- Command saturation
- Emergency stopping
- Logging
- Dashboard output

before integrating gesture recognition.

---

# 6. Mock Gesture Source

Provide a mock gesture source for testing without a webcam.

```python
class MockGestureSource:
    def __init__(self, sequence):
        self.sequence = sequence
        self.index = 0

    def update(self):
        """Return the next predefined GesturePrediction."""
        raise NotImplementedError
```

Example test sequence:

```python
sequence = [
    ("stop", 2.0),
    ("forward", 3.0),
    ("turn_left", 1.5),
    ("forward", 2.0),
    ("stop", 2.0),
]
```

This source should support:

- Scripted demonstrations
- Automated tests
- Safety testing
- Command-manager testing
- Dashboard testing

---

# 7. Webcam Source

Provide a working webcam interface.

```python
class WebcamSource:
    def __init__(self, camera_id: int = 0):
        self.camera_id = camera_id

    def open(self) -> None:
        """Open the webcam."""
        raise NotImplementedError

    def get_frame(self):
        """Return the latest camera frame."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Return whether valid frames are being received."""
        raise NotImplementedError

    def close(self) -> None:
        """Release the webcam."""
        raise NotImplementedError
```

The webcam source should:

- Open the selected camera
- Return valid frames
- Report camera failure
- Track frame timestamps
- Release resources safely

Students should not need to implement low-level webcam access.

---

# 8. Hand-Landmark Detection

Provide a working hand-tracking module using MediaPipe or an equivalent library.

```python
class HandTracker:
    def process_frame(self, frame):
        """
        Detect a hand and return normalized landmarks.

        Returns:
            landmarks:
                Hand landmark data or None.
            annotated_frame:
                Frame with visualization overlays.
        """
        raise NotImplementedError
```

The starter implementation should:

- Detect at least one hand
- Return normalized landmark coordinates
- Draw landmarks
- Report whether a hand is visible
- Measure processing latency
- Return an annotated image

Students should build gesture logic on top of the landmark output.

---

# 9. Gesture Classifier Skeleton

Provide a partially completed gesture classifier.

```python
class GestureClassifier:
    def __init__(self, config):
        self.config = config

    def classify(self, landmarks):
        """
        Convert hand landmarks into a GesturePrediction.

        Student TODO:
        - Define gesture rules
        - Compute confidence
        - Handle unknown gestures
        """
        raise NotImplementedError
```

Students may implement rule-based gesture classification using:

- Finger extension states
- Landmark distances
- Landmark angles
- Hand orientation
- Relative finger positions

The output should be:

```python
GesturePrediction(
    label=GestureLabel.FORWARD,
    confidence=0.92,
    timestamp=time.monotonic(),
)
```

The classifier should always return `UNKNOWN` when a gesture cannot be identified reliably.

---

# 10. Gesture Filter and State Machine

Provide a partially completed temporal-filtering module.

```python
class GestureFilter:
    def __init__(self, config):
        self.config = config
        self.current_candidate = None
        self.candidate_start_time = None
        self.active_gesture = None

    def update(self, prediction):
        """
        Convert noisy predictions into stable gesture states.

        Student TODO:
        - Apply confidence threshold
        - Apply hold-time requirement
        - Implement gesture transitions
        - Give STOP the highest priority
        """
        raise NotImplementedError
```

Students should implement or tune:

- Minimum confidence
- Required gesture hold time
- Debounce logic
- Unknown-gesture behavior
- Gesture transition logic
- Stop-command priority
- Gesture release behavior

---

# 11. Command Manager

Provide a common command manager with partially completed gesture mappings.

```python
class CommandManager:
    def __init__(self, config):
        self.config = config

    def gesture_to_command(self, gesture_prediction):
        """
        Convert a filtered gesture into a RobotCommand.

        Student TODO:
        - Map gestures to velocity commands
        - Select speed values
        - Handle slow mode
        - Handle unknown gestures
        """
        raise NotImplementedError
```

Example command mappings:

```text
STOP        -> vx = 0.0, yaw_rate = 0.0
FORWARD     -> vx = 0.3, yaw_rate = 0.0
BACKWARD    -> vx = -0.15, yaw_rate = 0.0
TURN_LEFT   -> vx = 0.0, yaw_rate = 0.4
TURN_RIGHT  -> vx = 0.0, yaw_rate = -0.4
```

Students should be able to modify these values through the configuration files.

---

# 12. Safety Supervisor Skeleton

Provide a partially completed safety layer.

```python
class SafetySupervisor:
    def __init__(self, config):
        self.config = config
        self.emergency_stop_active = False
        self.previous_command = None

    def evaluate(
        self,
        requested_command,
        robot_state,
        current_time,
        perception_available=True,
    ):
        """
        Approve, modify, or reject a requested command.

        Student TODO:
        - Apply command timeout
        - Reject low-confidence commands
        - Apply velocity limits
        - Apply acceleration limits
        - Stop on perception loss
        - Stop on communication loss
        """
        raise NotImplementedError
```

The safety supervisor should return:

```python
SafeCommandResult(
    requested_command=requested_command,
    approved_command=approved_command,
    safety_state="safe",
    stop_reason=None,
)
```

Required stop reasons may include:

```text
emergency_stop
stale_command
low_confidence
perception_lost
communication_lost
robot_not_enabled
invalid_command
```

The physical hardware interface must also contain independent instructor-provided safety limits.

---

# 13. Robot Camera Viewer

Provide a working robot-camera streaming client.

```python
class RobotCameraViewer:
    def __init__(self, config):
        self.config = config

    def connect(self) -> None:
        """Connect to the robot-mounted camera stream."""
        raise NotImplementedError

    def get_frame(self):
        """Return the latest robot-camera frame."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Return whether the camera stream is active."""
        raise NotImplementedError

    def disconnect(self) -> None:
        """Close the camera connection."""
        raise NotImplementedError
```

The instructional team should provide the transport layer.

Students may modify:

- Image layout
- Overlays
- Latency display
- Connection status display
- Navigation aids

---

# 14. Mission-Control Dashboard

Provide a basic dashboard that displays:

- Laptop webcam image
- Robot-camera image
- Detected gesture
- Gesture confidence
- Filtered gesture
- Requested velocity command
- Approved velocity command
- Robot state
- Safety state
- Stop reason
- Connection status
- Camera status
- Emergency-stop state
- Trial time

Suggested layout:

```text
+-------------------------+-------------------------+
| Laptop Webcam           | Robot Camera            |
|                         |                         |
| Gesture: FORWARD        |                         |
| Confidence: 92%         |                         |
+-------------------------+-------------------------+
| Requested command: vx=0.30, yaw=0.00              |
| Approved command:  vx=0.22, yaw=0.00              |
| Safety state: SAFE                                  |
| Connection: ACTIVE                                  |
| Last valid gesture: 0.10 seconds ago                |
+-----------------------------------------------------+
```

Students may redesign or extend the dashboard.

---

# 15. Maze Environments

Provide at least three simulation environments.

## Flat World

Used for:

- Basic motion tests
- Keyboard control
- Stopping tests
- Turning tests

## Mini Course

Used for:

- Hardware qualification preparation
- One straight corridor
- One left turn
- One right turn

## Full Maze

Used for:

- Integrated simulation trials
- Final competition preparation
- Performance evaluation

The maze should include:

- Start region
- Goal region
- Collision geometry
- Wide corridors
- At least two turns
- Robot reset location
- Clearly defined boundaries

---

# 16. Configuration Files

Store important parameters in YAML files.

Example `safe_limits.yaml`:

```yaml
velocity_limits:
  vx_min: -0.15
  vx_max: 0.40
  vy_min: 0.00
  vy_max: 0.00
  yaw_rate_min: -0.50
  yaw_rate_max: 0.50

acceleration_limits:
  linear: 0.40
  angular: 0.80

gesture:
  confidence_min: 0.80
  hold_time_seconds: 0.35

safety:
  command_timeout_seconds: 0.50
  stop_on_perception_loss: true
  stop_on_communication_loss: true

hardware:
  require_enable: true
  require_heartbeat: true
```

Example `simulation.yaml`:

```yaml
robot:
  mode: simulation
  environment: flat_world

input:
  mode: keyboard

display:
  show_dashboard: true
  show_simulation: true

logging:
  enabled: true
  directory: logs
```

Example `hardware.yaml`:

```yaml
robot:
  mode: hardware
  address: REPLACE_WITH_ROBOT_ADDRESS

input:
  mode: gesture

display:
  show_dashboard: true
  show_robot_camera: true

logging:
  enabled: true
  directory: logs

safety:
  require_hardware_qualification: true
```

Hardware addresses and credentials should not be committed to the public repository.

---

# 17. Logging Utilities

Provide structured CSV logging.

Each control-loop update should record:

```text
timestamp
trial_id
gesture_raw
gesture_filtered
gesture_confidence
requested_vx
requested_vy
requested_yaw_rate
approved_vx
approved_vy
approved_yaw_rate
measured_vx
measured_vy
measured_yaw_rate
safety_state
stop_reason
robot_connected
camera_available
emergency_stop
```

Example log location:

```text
logs/team_01/trial_03.csv
```

Students should use these logs to calculate:

- Trial duration
- Gesture-command accuracy
- Number of false commands
- Number of safety stops
- Number of manual resets
- Average command latency
- Maze completion rate

---

# 18. Installation Verification Script

Provide a script such as:

```bash
python ci_course/scripts/check_install.py
```

The script should verify:

- Supported Python version
- MuJoCo installation
- Required Python packages
- Webcam availability
- Simulation environment loading
- Locomotion-policy loading
- Keyboard input
- Dashboard imports
- Configuration-file loading

Example output:

```text
[PASS] Python version
[PASS] MuJoCo import
[PASS] Course package import
[PASS] Simulation environment
[PASS] Go1 policy
[PASS] Webcam detected
[PASS] Configuration files
[PASS] Logging directory

Course environment is ready.
```

Hardware connectivity should be checked by a separate instructor-supervised script.

---

# 19. Hardware Qualification Script

Provide a guided script:

```bash
python ci_course/scripts/run_hardware_check.py
```

The script should guide teams through:

1. Robot connection
2. Camera connection
3. Emergency-stop verification
4. Stationary heartbeat test
5. Low-speed forward test
6. Stop test
7. Left-turn test
8. Right-turn test
9. Perception-loss test
10. Communication-loss test

Each step should require instructor approval before continuing.

---

# 20. Automated Tests

Provide example unit tests and require students to add tests.

Required starter tests:

```python
def test_unknown_gesture_produces_stop():
    pass


def test_low_confidence_gesture_produces_stop():
    pass


def test_stale_command_produces_stop():
    pass


def test_velocity_is_saturated():
    pass


def test_acceleration_is_limited():
    pass


def test_emergency_stop_overrides_command():
    pass


def test_perception_loss_produces_stop():
    pass


def test_communication_loss_produces_stop():
    pass
```

Tests should not require:

- A physical robot
- A webcam
- A graphical display

Mock inputs should be used whenever possible.

---

# 21. Student TODO Markers

Student assignments should use consistent TODO markers.

Example:

```python
def classify(self, landmarks):
    # TODO(student): Determine which fingers are extended.
    # TODO(student): Identify the gesture label.
    # TODO(student): Compute a confidence value.
    raise NotImplementedError
```

Recommended labels:

```text
TODO(student)
TODO(extension)
TODO(instructor)
```

This makes assignment scope clear.

---

# 22. Code Provided as Complete Infrastructure

The following components should be fully implemented before the course begins:

- MuJoCo installation and loading
- Go1 simulation environment
- Pretrained locomotion-policy loading
- Simulation rendering
- Physical Go1 networking
- Physical Go1 command transport
- Robot-state communication
- Robot-camera transport
- Webcam capture
- Hand-landmark detection
- Keyboard input
- Emergency-stop mechanism
- Basic dashboard
- Configuration loading
- CSV logging
- Installation checker
- Hardware qualification tool

---

# 23. Code Students Should Complete

Students should complete or modify:

- Gesture rules
- Gesture confidence logic
- Gesture filtering
- Gesture state transitions
- Gesture-command mapping
- Command smoothing
- Velocity saturation
- Acceleration limiting
- Command timeout
- Perception-loss behavior
- Communication-loss behavior
- Dashboard extensions
- Testing procedures
- Performance analysis
- Team-selected extension

---

# 24. Recommended Development Order

The instructional team should develop the starter code in this order.

## Phase 1 — Simulation Foundation

1. Create the course package.
2. Create the common command types.
3. Wrap the existing Go1 locomotion environment.
4. Create the simulation interface.
5. Create keyboard control.
6. Add reset and emergency stop.
7. Add logging.
8. Add the flat-world environment.

## Phase 2 — Command Architecture

9. Create the command manager.
10. Create the safety-supervisor skeleton.
11. Add command limits.
12. Add mock gesture input.
13. Add automated tests.
14. Add the mini-course environment.

## Phase 3 — Vision

15. Add webcam capture.
16. Add hand-landmark detection.
17. Create the gesture-classifier skeleton.
18. Create the gesture-filter skeleton.
19. Connect gesture input to simulation.
20. Add webcam visualization.

## Phase 4 — Hardware

21. Create the Go1 hardware interface.
22. Add command heartbeat.
23. Add hardware enable and disable logic.
24. Add the robot-camera client.
25. Add the hardware qualification script.
26. Test safe disconnect behavior.

## Phase 5 — Course Packaging

27. Create weekly lab folders.
28. Add student TODO sections.
29. Add instructor solution versions.
30. Add setup documentation.
31. Add troubleshooting documentation.
32. Add the full maze.
33. Record a reference demonstration.
34. Run a complete instructor test of the 12-week workflow.

---

# 25. Initial Instructor Development Milestone

The first major milestone should be:

> A student can launch the simulation with one command and safely drive the Go1 using keyboard controls without interacting with the locomotion-policy internals.

Example:

```bash
python ci_course/scripts/run_keyboard_demo.py
```

The second milestone should be:

> A scripted mock gesture sequence can control the simulated Go1 through the same command and safety pipeline.

Example:

```bash
python ci_course/scripts/run_mock_gesture_demo.py
```

The third milestone should be:

> Webcam gestures can control the simulated Go1 while the safety supervisor handles invalid and stale input.

Example:

```bash
python ci_course/scripts/run_gesture_demo.py
```

Only after these simulation milestones are reliable should the course stack be connected to the physical Go1.

---

# 26. Hardware Safety Boundary

Student code should never directly send unrestricted commands to the physical robot.

The hardware command path should always be:

```text
Student Gesture Logic
        |
        v
Student Command Manager
        |
        v
Student Safety Supervisor
        |
        v
Instructor Hardware Safety Layer
        |
        v
Physical Go1
```

The instructor hardware layer should independently enforce:

- Maximum velocity
- Maximum turning rate
- Command heartbeat
- Enable state
- Emergency stop
- Communication timeout
- Safe zero-command behavior
- Safe disconnect behavior

This boundary allows students to learn robotics and control design while keeping physical robot operation supervised and constrained.
