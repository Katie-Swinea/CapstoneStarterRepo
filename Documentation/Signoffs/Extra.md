# Extra

![System](../Images/Extra_jrneal.png)

Figure 1: Extra subsystem and the pause switch can be seen in this figure.

- The goal of this subsystem is to adhere to the rules as provided by the customer, Devcom, and to add lights and sounds to the design which will add to the point total as provided by Devcom. The system needs a pause switch to deactivate it between rounds. The system will also include lights and sounds before launching a projectile to add to the decoration portion of the design.

## **Constraints:**

| **Number:** | **Constraint:** | **Origin:** | 
| --- | --- | --- |
| 1. |  The interceptor shall have a switch that sets the system into a pause state that will keep the interceptor from firing. | Rulebook |
| 2. | The voltage switched by the pause switch shall be 5V. | System Constraint|
| 3. | The interceptor must have lights that are bright enough to be seen by the judges approximately six and a half feet away, which is the longest length of the gameboard. Therefore the lights must have a candela rating greater than that of a fire alarm which is 15 cd [1]. These lights must also emit a light that falls within the visual light spectrum of 380 to 720 nanometers [2]. | Rulebook / System |
| 4. | The interceptor must make sounds before firing. The sounds will need to fall within the range of frequency humans can hear which is 20 to 20,000Hz [3]. The volume, or loudness, must be 10db above the average of the room [3], which usually falls at 60 dB [3], in order for the judges to hear the sound. The sound must also not exceed 85dB for more than eight hours or it may cause hearing damage [3]. | Rulebook / Safety |
   
1. One of the requirements in the rulebook, given to us by the customer, is that the interceptor needs to have a pause switch that keeps the interceptor from firing when the board is being reset. This switch will need to be physical, but in the implementation, it will run to the processor where it will prevent it from outputting any signals. When the switch is engaged it will keep the processor block from outputting signals to the mechanical system. This will ensure that the interceptor does not fire while the judges are in the competition area.
   
2. The circuit that is implemented by the pause switch needs to fall within the limitations of the processor block. Based on the processors that could be chosen the voltage that will be switched will be 5V. This source will be connected to a PCB that will be connecting the circuit components.

3. To add to the total points for the competition, the interceptor must have lights. This constraint can be found in the official rulebook for the competition. Light that falls within the spectrum that we can see, which falls within 380 to 720 nanometers [2], is sufficient. Therefore two arrays of ten LED's will be used for this. Both of these LED's fall within these parameters. The LED's must be viewable by the judges from a minimum of 6.5ft. An applicable example of lights within a building, other than the room lighting, is a fire alarm. The current ADA expected candela value is a minimum of 15cd. If this rating is official for getting the attention of hearing impared people in a room, then it will be enough light to be seen by the judges 6.5ft away. 
   
4. To add to the total points for the competition, the interceptor must make sounds before firing. This constraint can be found in the official rulebook for the competition. The piezo buzzer must be able to work with an output of the Jetson Nano which will be 5V. It must also fall within the human hearing range of frequency which is 20 to approximately 20,000Hz. The piezo buzzer that was chosen operates at a frequency of 2500Hz to 3500Hz which will fall within the frequency range that humans can hear. When it comes to loudness, humans can tolerate a range of 0 to 120db and the sound must not exceed 85db for long periods which will keep the noise at a safe level [3]. The buzzer also needs to be 10db louder than the noise in the room which is the qualification for paging speakers [2]. The average room noise is 50db, therefore the buzzer should produce a noise with a minimum loudness of 60db. 
   
## Buildable Schematic
![System](../Images/Buildable_Extra_jrneal.png)

Figure 1: This represents the buildable schematic for the pause switch. This switch outputs 5V or ground that comes from the power subsystem. This output is sent to the processor block to determine the pause state. In this example, the green LED's will be at the top, and the red LED's will be at the bottom. 


## **Analysis**
For the pause switch component, there are many different switches that can be chosen. Switches range between single pole single throw and upwards. The switch that needs to be implemented for the pause switch should be a single pole double-throw switch that has a two on functions and an off function. This will ensure that with one connection the processor will be receiving 5V, which will count as a binary one, and when the switch is off the processor will be connected to ground which will be interpreted as a binary zero. The switch that was chosen for this task is the CIT Relay and Switch, ANT11SF1CQE [5]. This switch is rated for 5A and 28VDC which will be more than enough for this simple task. The other main portion of the pause switch is the implementation in the code of the processor. The Jetson Nano has been chosen as the processor that will be recieving the data. To be clear when the pause switch is on 5V will be allowed to pass and when it is off the circuit will be connected to ground. This input will be interpreted as a variable and when the circuit is switched to ground, the processor will be allowed to collect the data from the sensors. When the switch is set to 5V the processor will be in the pause state where it can not do anything but wait for the switch to be turned off.

When the output of the switch is connected to 5V this will be sent to the processor and an array of ten red LED's [6], with a wavelength of 624nm, and ten current limiting resistors that will indicate that the interceptor has been put into pause mode. This set of LED's will be connected to the processor node on one side and the gound on the other. This will allow current to flow when the switch is connected to 5V and will show that the interceptor is in the pause state. The array of ten green LED's [7], with a wavelength of 525nm, will be connected to the processor node on one side and 5V from the power subsystem on the other. When the switch is connected to the ground current will flow from the 5V to the ground which will light up the green LED's. This will serve to show that the interceptor is ready to fire.

![System](../Images/Led_Equation.png) [8]

The rated current for the LED's is 20mA for the green LED's and for the red it is 50mA. Because of the 5V being used a resistor value was chosen, using the equation above [8], to keep the LED's below their maximum ratings. Both resistors share the same Vs of 5V. The values for the red LED were found using the datasheet those values are: Vf = 2.5 (max of 3.0V) and If DC = max of 50mA [9]. For the green LED's the datasheet was used to find values of Vf = 3V (average) and If DC = 20mA max [10]. These values were then put into the equation above and resistance values were calculated to make both resistors. The green LED's need a resistance of 100 Ohm [11] and the red LED's need a resistance of 50 Ohm [12]. For the green LED this sets the voltage at 3V and the current at 20mA. This allows for the light intensity to be calculated from the datasheet, at 20mA the LED is rated for 25cd [10]. For the red LED, the values are set at 2.5V and 50mA. Based on the datasheet, a current of 50mA produces a value of 25cd [9]. This sets the power consumtion at 0.125W for the red LED and 0.03W for the green LED, according to the first equation below.

$$P=VI$$

The candela value for fire alarms was taken from the Americans with Disabilities Act's (ADA) guidelines on accessable designs. This value, which is considered enough light to get the attention of hearing impared individuals, has an ADA anticipated value of 15cd. This value takes into account ambient light and if the strobe is in the middle of the room [1]. Therefore, if this value is considered the standard for getting the attention of deaf individuals during an emergency, it will be adequate for viewing from approximately 6.5ft away by the judges. Just to be sure, once again the green and red LED's both have an output of 25cd which surpasses the given requirement. There is also an array of ten of them to increase the overall brightness for the judges.

The wiring schematic can be seen in figure one. The wiring diagram is very simple and only involves a few connections. The power source comes directly from the power block. The connection for the buzzer circuit would be from the GPIO (General Purpose Input Output) pins on the Jetson Nano to one connection of the buzzer and then the other connection will be connected to the ground of the board. The next connection would be the 5V terminal to the PCB and the second would be the ground. All that would be left is the code for making the sounds. The code written would need to send a 5V square wave to the piezo buzzer which would allow it to play a sound. This sound would be played for a defined period of time when the processor recieves the proper signal. This signal will most likely be the aiming signal and the sounds will be played for a predetermined amount of time. The buzzer that was chosen is the Mallory Sonalert Products Inc. PT-2130PQ [15]. This buzzer is rated for 5V and can operate from 5.0 - 30.0 Vp-p and a frequency of 2500Hz to 3500Hz. This buzzer needs to have a decibel value at 6.5ft that falls within the rating for paging speakers which is 10db above the ambient noise level [4]. The equation below [14] shows the relationship between decibels and distance. As distance increases the decible level drops. As the datasheet for the buzzer states, the rating for the chosen buzzer is 90db at 5V from 10cm away [13]. A calculation from 6.5ft away (1.98m) shows that the decibel level will be reduced by 25.93db, therefore the decibel rating at 6.5ft (1.98m) will be 90db - 25.93db which is 64.07db. This value falls more than 10db above the rating for the noise in the room which is 60db therefore the volume meets the qulifications of a paging speaker. Because the qualifications are met, the judges will be able to hear the buzzer from 6.5ft (1.98m). 

$$dL =  20 log (R2 / R1)$$ [14]

## Bill of Materials

| **Items:** | **Quantity:** | **Price:** | **Total:** |
| --- | --- | --- | --- |
| CIT Relay and Switch, ANT11SF1CQE (Switch) | 1 | $3.48 | $3.48 |
|  Vishay Semiconductor Opto Division, VLCS5130 (Red LED) | 10 | $4.10 | $7.58 |
|  American Bright Optoelectronics Corporation, BL-BGX3V1 (Green LED) | 10 | $3.47 | $11.05 |
|  TE Connectivity Passive Product, LR1F100R (100 Ohm Resistor) | 10 | $0.55 | $ 11.60|
|  Vishay Dale, CMF5550R000FKEK70 (50 Ohm resistor) | 10 | $3.78 | $15.38 |
|  Mallory Sonalert Products Inc. PT-2130PQ (Buzzer) | 1 | $2.14 | $17.52 |


| **Item:** | **URL** |
| --- | --- |
| CIT Relay and Switch, ANT11SF1CQE (Switch) |  https://www.digikey.com/en/products/detail/cit-relay-and-switch/ANT11SF1CQE/12503396 |
| Vishay Semiconductor Opto Division, VLCS5130 (Red LED) | https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VLCS5130/4073547 |
| American Bright Optoelectronics Corporation, BL-BGX3V1 (Green LED) | https://www.digikey.com/en/products/detail/american-bright-optoelectronics-corporation/BL-BGX3V1/9678159 |
|  TE Connectivity Passive Product, LR1F100R (100 Ohm Resistor) | https://www.digikey.com/en/products/detail/te-connectivity-passive-product/LR1F100R/2381158 |
| Vishay Dale, CMF5550R000FKEK70 (50 Ohm Resistor) | https://www.digikey.com/en/products/detail/vishay-dale/CMF5550R000FKEK70/3616606 |
| Mallory Sonalert Products Inc. PT-2130PQ (Buzzer) | https://www.digikey.com/en/products/detail/mallory-sonalert-products-inc/PT-2130PQ/969807 |


## References
1. “Audible/Visible Appliance Reference Guide Introduction: The Need for an Audible/Visible Compliance Reference Guide.”, firetechs.net, https://www.firetechs.net/library/ReferenceGuides/SystemSensor/AudibleVisibleRefGuide.pdf (accessed Apr. 22, 2024).
2.  A. Hadhazy, “What are the limits of human vision?,” BBC News, https://www.bbc.com/future/article/20150727-what-are-the-limits-of-human-vision (accessed Apr. 17, 2024).
3. “What is the human hearing range in hz and DB?: Miracle-ear,” Miracle Ear, https://www.miracle-ear.com/blog-news/human-hearing-range (accessed Apr. 17, 2024).
4. B. Mesnik, “What is the right sound level for your paging speakers?,” Kintronics, https://kintronics.com/right-sound-level-paging-system/ (accessed Apr. 23, 2024). 
5. “Ant11sf1cqe CIT relay and switch | switches | DigiKey,” Digikey, https://www.digikey.com/en/products/detail/cit-relay-and-switch/ANT11SF1CQE/12503396 (accessed Apr. 16, 2024). 
6. “VLCS5130,” DigiKey, https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VLCS5130/4073547 (accessed Apr. 21, 2024).
7. “BL-BGX3V1,” DigiKey, https://www.digikey.com/en/products/detail/american-bright-optoelectronics-corporation/BL-BGX3V1/9678159 (accessed Apr. 21, 2024). 
8. V. Lynch, “Led resistor calculator,” The Engineering Mindset, https://theengineeringmindset.com/led-resistor-calculator/ (accessed Apr. 21, 2024). 
9. “VLCS5130,” Vishay, https://www.vishay.com/docs/81938/vlcs5130.pdf (accessed Apr. 21, 2024). 
10. “BL-BGX3V1,” BRIGHT LED ElLECTRONICS CORP., https://www.americanbrightled.com/pdffiles/led-components/through-hole/BL-BGX3V1.pdf (accessed Apr. 21, 2024). 
11. “LR1F100R,” DigiKey, https://www.digikey.com/en/products/detail/te-connectivity-passive-product/LR1F100R/2381158 (accessed Apr. 28, 2024). 
12. “CMF5550R000FKEK70,” DigiKey, https://www.digikey.com/en/products/detail/vishay-dale/CMF5550R000FKEK70/3616606 (accessed Apr. 21, 2024). 
13. “PT-2130PQ,” DigiKey, https://www.digikey.com/en/products/detail/mallory-sonalert-products-inc/PT-2130PQ/969807 (accessed Apr. 28, 2024). 
14. E. Engineeringtoolbox, “Sound propagation - The Inverse Square Law,” Engineering ToolBox, https://www.engineeringtoolbox.com/inverse-square-law-d_890.html (accessed Apr. 23, 2024). 

‌
