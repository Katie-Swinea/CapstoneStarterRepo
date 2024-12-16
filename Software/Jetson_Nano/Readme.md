# Code for the Jetson Nano

This is the code that was developed for the competition. It includes the integration of the jetson nano with the real sense camera including the color map and paramter
adjustments. The code also includes the image processing, false detection handling, frame storage, velocity and acceleration calculations, and trajectory predictions.
The location of the ball and predictions are sent to arduino via I2C. The code also include the buzzer noise for firing and light's pattern and the pause switch
functionality with the switches input into the nano being used to temporarily stop the program.

The code uses the opencv library, the real sense library, and the jestson's gpio pin interface. It also requires other libraries for functionality like the time, 
numpy, typing for tuple, subprocess, sys, threading, os, smbus2, time, and math. These are used for specfic operations and calculations.

This software can be uploaded on the jeston nano via a USB as it it. It can be set to run when the jetson nano is turned on with a simple program already uploaded on
the jeston nano. Use a monitor to see the jeston nano console and change the program that runs on start up.
