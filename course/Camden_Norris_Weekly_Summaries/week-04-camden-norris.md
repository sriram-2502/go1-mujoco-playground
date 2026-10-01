| Intent | Gesture | Why it is distinct | Possible confusion |

| --- | --- | --- | --- |

| STOP | Open palm | Large, obvious hand shape | Could resemble another open-hand gesture |

| FORWARD | Point forward / index finger | Single extended finger is easy to identify | Could be confused when the hand is rotated |

| BACKWARD | Closed fist | Very different from pointing or an open palm | Could be confused with a partially closed hand |

| LEFT | Point left | Direction is visually clear | Camera angle may make the direction unclear |

| RIGHT | Point right | Direction is visually clear | Camera angle may make the direction unclear |



\### Why are landmarks more useful than raw pixels for a simple gesture model?



Landmarks provide the positions of key hand joints and fingertips, making it easier to identify hand shapes and finger positions without analyzing every pixel.



\### What is the difference between “no hand” and “unknown gesture”?



“No hand” means the camera does not detect a hand at all. “Unknown gesture” means a hand is detected, but its shape does not match one of the recognized gestures.



\### Why should STOP not depend on a subtle finger position?



STOP should use a clear and obvious gesture so it can be recognized quickly and reliably. A subtle finger position could be missed or misclassified by the software.



\### Which gesture pair is most likely to be confused, and why?



LEFT and RIGHT are most likely to be confused because they may use similar pointing gestures. Hand rotation, camera angle, or mirrored video could make the direction harder to distinguish.

