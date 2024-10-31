# Experimental Analysis

## Introduction 
The purpose of this report is to verify the requirements and constraints set for each subsystem and explain the prodecures and experiments used to validate them. The constraints for each subsystem were set and finialzed during the detail design phase of our senior design project. 

## Experimentation
Each subsystem will be divided into it's own section to make it easy to follow.

### Device Power

#### Constraints
| NO. | Constraint                                                          |
|-----|---------------------------------------------------------------------|
| 1   | The power system shall be controlled by an emergency stop which will de-energize the mechanical system. This will shut off the motors which will not allow any projectiles to be fired. This will only be used if the system threatens peoples safety 
| 2   | The system shall convert wall outlet AC voltage to up to 24 volts at up to 20 amps for the mechanical system. This includes two DC motor controllers which requires 9-48 volts at 5 amps and the DC motor which will receieve anywhere from 12-24 volts at 10 amps |
| 3   | The system shall convert wall outlet AC voltage to up to 5 volts at up to 5 amps for the proccesor system, which requires 5 volts at 4 amps, relay coil which requires 5 volts as a high impendence input and the extra subsystem which requires 5 volts at 0.8 amps. |
| 4   | The system shall be controlled by a power switch                 |

#### Results

#### 1 - Emergency Stop:

The system must have an emergency stop button that will completly de-energize the mechanical system. This means the processor and lights will remain on, while the motors and solenoid that make up the mechanical system will be completely off. There are two types of mechanical componets in this system that each require a differnt test to measure the efectiveness of the emergency stop.
The firing motors that control the wheels which create the speed of the projectile were tested by measuring the output voltage with the emergency stop being on and off. The solenoid 





### Extra

#### Constraints
| NO. | Constraint                                                          |
|-----|---------------------------------------------------------------------|
| 1. |  The interceptor shall have a switch that sets the system into a pause state that will keep the interceptor from firing. |
| 2. | The voltage switched by the pause switch shall be 5V. |
| 3. | The interceptor must have lights that are bright enough to be seen by the judges approximately six and a half feet away, which is the longest length of the gameboard. Therefore the lights must have a candela rating greater than that of a fire alarm which is 15 cd. These lights must also emit a light that falls within the visual light spectrum of 380 to 720 nanometers. |
| 4. | The interceptor must make sounds before firing. The sounds will need to fall within the range of frequency humans can hear which is 20 to 20,000Hz. The volume, or loudness, must be 10db above the average of the room, which usually falls at 60 dB, in order for the judges to hear the sound. The sound must also not exceed 85dB for more than eight hours or it may cause hearing damage. |

#### Results

#### 1 

#### 2 
The voltage switched by the pause switch was measured over the course of five trials. All trial results are shown below. As can be seen the voltage switched by the pause switch is approximately 5V.

| NO. | Result |
|-----|---------------------------------------------------------------------|
| 1. | 5.05V |
| 2. | 5.05V |
| 3. | 5.05V |
| 4. | 5.05V |
| 5. | 5.05V |

#### 3
The following images show that both the green and red lights can be seen from 6.5' away. 

#### Figure 1: Green LED's
![Alt Text](Video_Photos/Green_lights.jpeg)

#### Figure 2: Red LED's
![Alt Text](Video_Photos/Red_Lights.jpeg)

#### 4
The interceptor does make sounds before firing. The sound is a frequency that humans can hear and it can be heard above the noise of the room and interceptor itself. 

### Image Processing
#### Constraints
| NO. | Constraint                                                          |
|-----|---------------------------------------------------------------------|
| 1| Must be able to distinguish the golf ball from surroundings based on golf ball's shape and color |
| 2| Must be able to extract the x,y coordinates of the golf ball with an inch of accuracy to distinguish between the wires and variable height|
| 3| Must be able to receive the data and perform calculations in 500 ms to allow the interceptor time to aim and shoot based on the calculations|

#### Results






### Interceptor Controller

#### Constraints

| NO. | Constraint                                                          |
|-----|---------------------------------------------------------------------|
|1|The Interceptor Controller shall move firing mechanism to 1 of 30 pre set locations |
|2|Must communicate with processor|
|3|Shall receive 5V power supply from processor|
|4|Must change direction of the motors in the Mechanical's section |
|5|Must maintain safe firing speed and distance|
|6|Must change position before incoming object enters the "kill zone"|

#### Results


### Main Processor

#### Constraints

| NO. | Constraint                                                          |
|-----|---------------------------------------------------------------------|
| 1	| Time Constraints - Real-time data processing for trajectory prediction for the golf ball can not take longer than the total time for each image. The main processor needs to calculate the ball data before the ball reaches the end which varies from 1.9 seconds to 7.4 seconds |
| 2	| Processing Speed - The main processor scripts and programs have to be optimized for efficient calculations. The scripts get the speed, wire, and variable height from input data. These calculations should not take longer than their required time per calculation iteration |
| 3	| Resource Utilization - Since the board has 1.43GHz with quad-cores and 4GB RAM, the main processor needs to be utilized properly to prevent an overload of system resources. The system needs to use all cores and not overload the RAM for speed efficiency but not sacrifice stability |
| 4 | Pausing Processes: The system needs a pause state to stop other scripts from activating firing mechanisms. |

#### Results



### Sensor Subsystem

#### Constraints

| NO. | Constraint                                                          |
|-----|---------------------------------------------------------------------|
| 1   | The sensor shall be supplied 5 V via USB from the Jetson Nano processor   |
| 2   | The sensor shall be able to retrieve at least 2 data points within 0.0667s in order to calculate speed which allows for maximum time for calculations given the constraints of the image processing system  |
| 3   | The sensor shall have a resolution no larger than 1920 X 1080 due to constraints from the image processing system                                                                                           |
| 4   | The sensor shall be able to gather depth data from at most 6' and at least 1' away which is the length of the gameboard                                                                                     |
| 5   | The sensor shall have a FOV that is wider than 56" from 6' away which is the width of anchor 2 and the length of the gameboard                                                                              |

#### Results


