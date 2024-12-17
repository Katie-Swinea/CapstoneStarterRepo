# Code for the Arduino

This is the code that was developed for the competition. It is used to control the stepper motors in order to position and aim the interceptor towards the incoming 
golfball. It uses the information from the jetson nano sent via I2C communication. The information is a byte that contains the x and y position for the motors and a 
fire bit for the solenoid to launch the projectile at the golfball.

This software can be uploaded on the adruino by connecting it to a computer with the code and uploading it when the adruino is ready to accept a new upload of code. 
Ensure the arduino and computer are connected to the same ground. This version of the code is currently uploaded on the arduino.
