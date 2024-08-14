# Interceptor Controller Subsystem

## **Function:**
![Elaboration Photo](../Images/Controllers/InterceptorController.png)

Figure 1: Interceptor Controller Subsystem

The goal of this subsystem is to activate the position motors and firing mechanism within the mechanical system, maintain safe firing speed, as well as alleviate some of the coding within the processor. 

## **Constraints:**

|No.|Constraint|Origin|
|--|------|-------|
|1|The Interceptor Controller shall move firing mechanism to 1 of 30 pre set locations |Conceptual Design|
|2|Must communicate with processor| Conceptual Design |
|3|Shall receive 5V power supply from processor| Conceptual Design|
|4|Must change direction of the motors in the Mechanical's section |Conceptual Design|
|5|Must maintain safe firing speed and distance|Conceptual Design/Rule Book|
|6|Must change position before incoming object enters the "kill zone"| Conceptual Design|
|7|Must fire at incoming object before it can make contact will the device| Conceptual Design/Rule Book|



1.	Using the sensor data analyzed by the processor the arduino activates the 2 position motors to move to 1 of 30 set positions.
2.	After completing the movement to the desired position, and the projectile is within set "kill zone", the firing mechanism is engaged firing only one shot.
3.	Using the 5V pin on the processor to power the adruino.
4.  To be able to move to the correct coordinates the motors need to move in either direction along the x and y axis.
5.  Per Devcom rule books the projectile must be fired at a safe speed and stay within a distance of 6ft *this speed will be found by the ME team*
6. 

## **Buildable Schematics:**

![Elaboration Photo](../Images/Controllers/Schematic3.png)

Figure 2: Buildable Schematic

## **Analysis:**
Arduino Analysis:

Due to the Arduinos variety of uses and applications it was the best choice to convert the analog data being provided from processor to digital logic that the mechanical system can understand. Shown in Figure 3 below we can see the JDIGITAL pins are the outputs of the Arduino but are the inputs for the mechanical system satisfying the first constraint. As for sending the signal back to the processer the analog side is used since that is the language the processer uses satisfying the third constraint. To ensure that the Arduino does not have any current going into the I/O pins a Stepper Motor is there to increase the current going into the motor to make it run as well as keep the current from going in reverse bias and frying the Arduino. Using these two devices speed, rotation, and direction can be changed. The speed is dictated my the power given to each motor *This measurement will be supplied by the ME team based on constraints and parameters of the competition*.

Stepper Motor Integration:

The Arduino UNO R3 seamlessly integrates with the TB6600 Stepper Motor Driver to control the interceptor's aiming mechanism [7]. Through GPIO communication, the Arduino UNO R3 commands the stepper motor driver to adjust the interceptor's position, aligning it with the golf ball's predicted path. Real-time trajectory data calculated by the processor guides precise motor movements, ensuring accurate interception. The compatibility between theArduino UNO R3 and TB6600 Stepper Motor Driver facilitates seamless communication and system integration. The stepper motor will be put into a zero position. While it is in its zero position, the processor can count how many steps the motor takes to determine the correct aiming position. This can apply for the X-Axis and Y-Axis of the system to be able to reset the interceptor back to the zero position after each time it aims and fires at the incoming golf ball [6].

![Elaboration Photo](../Images/Controllers/Arduino.png)

Figure 3[1]


## **Bill of Materials:**

|Device|Description|Used in which subsystem|Part Number| Manufacturer|Quantity|Price|Total|
|-------|---|---------|-------------|----|----|----|----|
| Arduino UNO R3 |converts analog data to digital inputs to move motors|Interceptor Controller Subsystem|A000066| Arduino|1|$27.60|$27.60|
|TB6600 Stepper Motor Driver|Regulates current and keeps from going reverse bias, and divides rotation into equal steps|Interceptor Controller Subsystem & Mechanical Subsystem|TB6600|DFRobot|0||purchased by ME team|
| | | | | | |Final Total|$27.60|

## **References:**
[1] Arduino, https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf (accessed Apr. 17, 2024). 

[2] Arduino, https://docs.arduino.cc/resources/schematics/A000066-schematics.pdf (accessed Apr. 17, 2024). 

[3] Arduino, https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf (accessed Apr. 17, 2024). 

[4] Admin, Technology tutorials, https://toptechboy.com/arduino-tutorial-37-understanding-how-to-control-dc-motors-in-projects/ (accessed Apr. 17, 2024). 

[5] R. Sawkare, “Arduino Uno R3 with l293d motor driver,” Medium, https://vayuyaan.medium.com/arduino-uno-r3-with-l293d-motor-driver-550c4a65f612 (accessed Apr. 17, 2024). 

[6] “TB6600 Stepper Motor Driver,” Bulkman, https://bulkman3d.com/wp-content/uploads/2019/06/TB6600-Stepper-Motor-Driver-BM3D-v1.1.pdf (accessed Apr. 8, 2024).

[7] “TB6600 Stepper Motor Driver,” DFRobot, https://www.dfrobot.com/product-1547.html (accessed Apr. 8, 2024).

[8] S. Hall, Devcom. Devcom, 2024. S31 Paper Wad Interceptor Challenge 2024, Rulebook, (accessed Apr. 8, 2024).
