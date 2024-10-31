# Experimental Analysis

## Introduction 
The purpose of this report is to verify the requirements and constraints set for each subsystem and explain the prodecures and experiments used to validate them. The constraints for each subsystem were set and finialzed during the detail design phase of our senior design project. 

## Experimentation
Each subsystem will be divided into it's own section to make it easy to follow.

### Power

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





