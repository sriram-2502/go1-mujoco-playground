\# Week 5: Gesture Classification and Validation



\## Validation Settings



Minimum confidence threshold: `0.80`  

Required hold time: `0.30 seconds`



Any gesture below the confidence threshold, an unknown gesture, or no detected hand is treated as `UNKNOWN`.



\## Test Protocol



The following gestures were tested:



\- STOP

\- FORWARD

\- BACKWARD

\- LEFT

\- RIGHT

\- UNKNOWN



Trials per gesture: 10  

Total trials: 60



Testing included different lighting conditions, hand distances, orientations, and transitions between gestures.



\## Confusion Table



| Expected | STOP | FORWARD | BACKWARD | LEFT | RIGHT | UNKNOWN |

| --- | ---: | ---: | ---: | ---: | ---: | ---: |

| STOP | 10 | 0 | 0 | 0 | 0 | 0 |

| FORWARD | 0 | 9 | 0 | 0 | 0 | 1 |

| BACKWARD | 1 | 0 | 9 | 0 | 0 | 0 |

| LEFT | 0 | 0 | 0 | 8 | 0 | 2 |

| RIGHT | 0 | 0 | 0 | 0 | 8 | 2 |

| UNKNOWN | 0 | 0 | 0 | 0 | 0 | 10 |



\## Accuracy Results



Overall accuracy: `90%`



STOP accuracy: `100%`



FORWARD accuracy: `90%`



BACKWARD accuracy: `90%`



LEFT accuracy: `80%`



RIGHT accuracy: `80%`



UNKNOWN accuracy: `100%`



A total of 54 out of 60 trials were classified correctly.



LEFT and RIGHT were the least accurate gestures. Most of their missed trials were classified as UNKNOWN instead of being incorrectly accepted as another movement command.



\## Confidence Threshold Results



Minimum confidence threshold: `0.80`



With the current confidence-proxy setup, recognized gestures use a confidence value of `0.95`, while UNKNOWN or rejected gestures use `0.00`.



Samples below the 0.80 threshold: `15 / 60`



The rejected samples included the 10 intentional UNKNOWN trials and five motion trials that were classified as UNKNOWN.



Using the confidence threshold helps prevent weak or uncertain gesture predictions from becoming valid commands. Low-confidence predictions are changed to `UNKNOWN` instead.



\## Temporal Validation



Required hold time: `0.30 seconds`



Average validation delay: approximately `0.30 seconds`



During testing, some gestures briefly switched between labels when the gesture was first presented. After a fraction of a second, the predictions became stable.



False validated transitions observed after the hold period: `0`



Requiring the same gesture to remain consistent for 0.30 seconds prevented the brief unstable predictions from becoming validated commands.



The tradeoff is a small delay before the gesture is accepted, but the added delay improves reliability and reduces accidental commands.



\## Input Handling



\### What happens when no hand is detected?



When no hand is detected, `hand\_detected` is false and the validated intent becomes `UNKNOWN`. This prevents movement from being commanded when the camera cannot see a valid hand.



\### What is an unknown gesture?



An UNKNOWN gesture means a hand may be visible, but the gesture does not match one of the approved commands or does not meet the required confidence level.



\### What happens when confidence is below 0.80?



The prediction is rejected and converted to `UNKNOWN`.



The allowed validated intents are:



`STOP`, `FORWARD`, `BACKWARD`, `LEFT`, `RIGHT`, and `UNKNOWN`.



\## Gesture Mapping



| Gesture | Validated Intent |

| --- | --- |

| Open palm | STOP |

| Point forward | FORWARD |

| Closed fist | BACKWARD |

| Point left | LEFT |

| Point right | RIGHT |

| No hand / uncertain gesture | UNKNOWN |



STOP remains the safest command and should have priority over movement commands.



\## Week 6 Recommendation



For Week 6, I recommend keeping the confidence threshold at `0.80` and the gesture hold time at `0.30 seconds`.



Testing produced an overall classification accuracy of `90%`. STOP and UNKNOWN performed best at 100%, while LEFT and RIGHT were the least accurate at 80%.



Some gestures briefly switched between predictions before stabilizing. The 0.30-second hold prevented those short transitions from immediately becoming commands.



Future improvements should focus on making LEFT and RIGHT easier to distinguish and replacing the temporary fixed confidence value with a measured classifier confidence.



These settings provide a good balance between responsiveness and reliability before validated gestures are connected to robot motion.



\## Conclusion



Week 5 showed how confidence filtering and temporal validation can improve gesture recognition reliability.



The system does not immediately accept every camera prediction. Instead, it checks the prediction confidence and requires a gesture to remain stable for 0.30 seconds before it becomes a validated intent.



Out of 60 trials, 54 were classified correctly for an overall accuracy of 90%. The validation system also prevented brief unstable predictions from becoming commands.

