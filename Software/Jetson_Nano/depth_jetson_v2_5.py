import time
import numpy as np
import cv2
import Jetson.GPIO as GPIO  # Import the GPIO library
import pyrealsense2 as rs  # RealSense library
from typing import Tuple
import subprocess
import sys
import threading
import os
import smbus2
import time
import math

# I2C bus (1 for Jetson Nano)
bus = smbus2.SMBus(1)

# Arduino I2C address
slave_address = 0x08  # Ensure this matches your Arduino address (0x08 is 8 in hexadecimal)

# Pins for JettyNano
SCRIPT_RUNNING_PIN = 12
SCRIPT_PAUSE_PIN = 18
BUZZER_PIN = 37

# Data keeping
frame_data = []  # Array to store the frame information
processing_times = []  # List to track frame processing times
frame_count = 3
frame_valid_count = 0
frame_similarity_threshold = 0.1
frame_range_threshold = 25

# Data Sending
data_interval = 10
check_interval = 0

# Pass through code
def nothing(_):
    pass

# Look up table for positioning
lookup_table = {
    # Table structure:
    # DIST, X, Y: LINE
    
    # Info at 75" -- NOT CONFIRMED-- FINLAY CONFRIMED WITH NEW CAMERA
    (75, 71, 120): 1,
    (75, 91, 120): 2,
    (75, 113, 120): 3,
    (75, 138, 120): 4,
    (75, 158, 121): 5,
    (75, 178, 122): 6,
    (75, 199, 124): 7,
    (75, 222, 128): 8,
    (75, 242, 125): 9,
    (75, 261, 128): 10,
    (75, 283, 129): 11,
    (75, 303, 129): 12,
    (75, 324, 129): 13,
    (75, 345, 128): 14,
    (75, 370, 128): 15,

    # Info at 70" -- NOT CONFIRMED-- FINLAY CONFRIMED WITH NEW CAMERA
    (70, 70, 118): 1,
    (70, 90, 118): 2,
    (70, 112, 118): 3,
    (70, 137, 118): 4,
    (70, 159, 115): 5,
    (70, 180, 121): 6,
    (70, 200, 118): 7,
    (70, 223, 120): 8,
    (70, 245, 122): 9,
    (70, 266, 120): 10,
    (70, 287, 122): 11,
    (70, 309, 123): 12,
    (70, 331, 122): 13,
    (70, 352, 122): 14,
    (70, 374, 120): 15,
    
    # Info at 65" -- NOT CONFRIMED-- FINLAY CONFRIMED WITH NEW CAMERA
    (65, 73, 112): 1,
    (65, 93, 112): 2,
    (65, 115, 94): 3,
    (65, 140, 112): 4,
    (65, 158, 114): 5,
    (65, 180, 112): 6,
    (65, 204, 113): 7,
    (65, 225, 114): 8,
    (65, 249, 114): 9,
    (65, 268, 115): 10,
    (65, 292, 117): 11,
    (65, 313, 118): 12,
    (65, 337, 117): 13,
    (65, 360, 116): 14,
    (65, 377, 118): 15,

    # Info at 60" -- FINLAY CONFRIMED WITH NEW CAMERA
    (60, 61, 106): 1,
    (60, 85, 110): 2,
    (60, 107, 108): 3,
    (60, 132, 109): 4,
    (60, 153, 109): 5,
    (60, 176, 108): 6,
    (60, 200, 110): 7,
    (60, 222, 109): 8,
    (60, 244, 108): 9,
    (60, 279, 109): 10,
    (60, 291, 109): 11,
    (60, 317, 105): 12,
    (60, 340, 110): 13,
    (60, 359, 110): 14,
    (60, 383, 108): 15,

    # Info at 55" -- FINLAY CONFRIMED WITH NEW CAMERA
    (55, 57, 95): 1,
    (55, 81, 99): 2,
    (55, 105, 96): 3,
    (55, 131, 94): 4,
    (55, 154, 96): 5,
    (55, 178, 97): 6,
    (55, 203, 98): 7,
    (55, 225, 98): 8,
    (55, 250, 95): 9,
    (55, 275, 95): 10,
    (55, 300, 95): 11,
    (55, 324, 95): 12,
    (55, 349, 99): 13,
    (55, 372, 100): 14,
    (55, 393, 100): 15,

    # Info at 50" -- FINLAY CONFRIMED WITH NEW CAMERA
    (50, 53, 84): 1,
    (50, 76, 87): 2,
    (50, 102, 83): 3,
    (50, 130, 84): 4,
    (50, 154, 88): 5,
    (50, 179, 87): 6,
    (50, 207, 88): 7,
    (50, 230, 88): 8,
    (50, 255, 87): 9,
    (50, 282, 88): 10,
    (50, 307, 88): 11,
    (50, 332, 88): 12,
    (50, 359, 90): 13,
    (50, 383, 93): 14,
    (50, 403, 89): 15,

    # Info at 45" -- FINLAY CONFRIMED WITH NEW CAMERA
    (45, 47, 72): 1,
    (45, 72, 77): 2,
    (45, 101, 74): 3,
    (45, 129, 73): 4,
    (45, 151, 79): 5,
    (45, 180, 78): 6,
    (45, 207, 81): 7,
    (45, 232, 78): 8,
    (45, 260, 77): 9,
    (45, 288, 77): 10,
    (45, 315, 75): 11,
    (45, 340, 77): 12,
    (45, 370, 77): 13,
    (45, 396, 80): 14,
    (45, 423, 74): 15,

    # Info at 40" -- FINLAY CONFRIMED WITH NEW CAMERA
    (40, 42, 59): 1,
    (40, 68, 61): 2,
    (40, 95, 60): 3,
    (40, 127, 62): 4,
    (40, 153, 68): 5,
    (40, 181, 65): 6,
    (40, 211, 66): 7,
    (40, 237, 65): 8,
    (40, 265, 65): 9,
    (40, 295, 66): 10,
    (40, 324, 62): 11,
    (40, 351, 62): 12,
    (40, 383, 63): 13,
    (40, 410, 66): 14,
    (40, 437, 60): 15,

    # Info at 35" -- FINLAY CONFRIMED WITH NEW CAMERA
    (35, 31, 37): 1,
    (35, 60, 40): 2,
    (35, 90, 35): 3,
    (35, 125, 36): 4,
    (35, 153, 45): 5,
    (35, 182, 41): 6,
    (35, 217, 41): 7,
    (35, 245, 41): 8,
    (35, 275, 40): 9,
    (35, 308, 40): 10,
    (35, 341, 37): 11,
    (35, 369, 39): 12,
    (35, 403, 42): 13,
    (35, 430, 48): 14,
    (35, 459, 42): 15,

    # Info at 30" -- FINLAY CONFRIMED WITH NEW CAMERA
    (30, 17, 22): 1,
    (30, 53, 19): 2,
    (30, 84, 12): 3,
    (30, 123, 12): 4,
    (30, 153, 18): 5,
    (30, 186, 13): 6,
    (30, 225, 14): 7,
    (30, 255, 15): 8,
    (30, 288, 14): 9,
    (30, 325, 15): 10,
    (30, 356, 19): 11,
    (30, 388, 15): 12,
    (30, 426, 19): 13,
    (30, 460, 20): 14,
    (30, 496, 17): 15,
}

# Function to find closet match Line inside the saved data array.
def find_line(distance: float, x: float, y: float) -> int:
    # Sort by closest distance first, then by closest x, and finally closest y
    sorted_entries = sorted(
        lookup_table.keys(),
        key=lambda k: (abs(k[0] - distance), abs(k[1] - x), abs(k[2] - y))
    )
    
    # Retrieve the int value corresponding to the closest (distance, x, y)
    closest_key = sorted_entries[0]
    return lookup_table[closest_key]

def calculate_intercept_time(initial_position, target_position, initial_velocity, acceleration):
    if acceleration == 0:
        # Avoid division by zero; use constant velocity formula instead
        if initial_velocity == 0:
            return 0  # Object won't move without velocity or acceleration
        return (target_position - initial_position) / initial_velocity
    
    # Coefficients of the quadratic equation at^2 + bt + c = 0
    A = 0.5 * acceleration
    B = initial_velocity
    C = initial_position - target_position

    # Calculate the discriminant
    discriminant = B**2 - 4 * A * C
    
    # Check if the discriminant is non-negative, else return None for no real solution
    if discriminant < 0:
        return 0  # No real solutions (complex roots)

    # Calculate both solutions for time
    time1 = (-B + math.sqrt(discriminant)) / (2 * A)
    time2 = (-B - math.sqrt(discriminant)) / (2 * A)

    # Filter out negative time values and return the smallest positive one
    times = [t for t in [time1, time2] if t >= 0]
    return min(times) if times else 0  # Return the positive time if it exists, else None

def Buzz(delay):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on buzzer
    time.sleep(delay)  # Keep it on for half the period
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn on buzzer
    time.sleep(delay)  # Keep it on for half the period
   
# Send data to Arduino
def send_data(data):
    pause_state = GPIO.input(18)
    if pause_state == GPIO.HIGH:
        print("Paused!")
    else:
        try:
            bus.write_byte(slave_address, data)
            print(f"Data sent: {bin(data)}")
        except OSError as e:
            print(f"I2C Error: {e}")

# Fire mechanism
def Fire(remaining_bits):
    fire_time = int(remaining_bits)
    print("Delay: ", fire_time)
        
    pause_state = GPIO.input(18)
    if pause_state == GPIO.HIGH:
        print("Paused!")
    else:
        print("Fire!")
        
        if fire_time > 126:
            time.sleep((fire_time-126)/1000)
            fire_time = 126
        
        fire_data = 0b10000000 | fire_time  # MSB is 1, and append remaining 7 bits
        send_data(fire_data)
        
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on buzzer
        time.sleep(fire_time/1000)  # Keep it on for half the period
        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off buzzer
        
        Buzz(.05)
        Buzz(.1)
        Buzz(.05)
        Buzz(.1)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.05)
        Buzz(.5)
        Buzz(.5)
        Buzz(.5)

# Send coordinates to Arduino
def SendCords(X, Y):
    if X > 31:
        X = 31
    elif X < 0:
        X = 0
    if Y > 3:
        Y = 3
    elif Y < 0:
        Y = 0
    print("Sending Coordinates")
    non_fire_data = (Y << 5) | X  # 0b00 + Y bits (2 bits) + X bits (5 bits)
    send_data(non_fire_data)

# Setup GPIO pin to control an external component (e.g., LED)
def setup_gpio():
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(SCRIPT_RUNNING_PIN, GPIO.OUT)  # Set Light output
    GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Set pin as output
    GPIO.setup(
    SCRIPT_PAUSE_PIN
, GPIO.IN)  # Set Pause switch input

# Initialize and configure the RealSense depth camera pipeline
def setup_pipeline():
    pipe = rs.pipeline()  # Create a pipeline to configure and start streaming
    cfg = rs.config()  # Create a configuration object for the pipeline
    cfg.enable_stream(rs.stream.depth, rs.format.z16, 90)  # Enable depth stream at 90 fps
    pipe.start(cfg)  # Start streaming with the configured settings
    return pipe


def shape_score(contour, _circularity):
    # Checks for valid contour
    if contour is None or len(contour) == 0:
        return 0
    
    # Does area check before doing shape_score
    area = cv2.contourArea(contour)
    if area > 65:
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return 0
        circularity = (4 * np.pi * area) / (perimeter ** 2)

        x, y, w, h = cv2.boundingRect(contour)
        if h == 0:
            return 0
        aspect_ratio = float(w) / h

        circularity_score = min(circularity, 1.0) * 100
        aspect_ratio_score = (1 - abs(1 - aspect_ratio)) * 100
        final_score = (circularity_score + aspect_ratio_score) / 2
        return final_score
      
    # Makes sure there is a return so no "None" return.  
    return 0


# Create the OpenCV window and the control sliders (trackbars)
def create_trackbars():
    cv2.namedWindow('depth')  # Create a window named 'depth' to display the image

    # Create trackbars for various parameters used in processing
    cv2.createTrackbar('alpha', 'depth', 1, 1000, nothing)  # Trackbar for adjusting contrast
    cv2.createTrackbar('param1', 'depth', 1, 1000, nothing)  # Trackbar for edge detection parameter 1
    cv2.createTrackbar('param2', 'depth', 1, 1000, nothing)  # Trackbar for edge detection parameter 2
    cv2.createTrackbar('blur', 'depth', 1, 10, nothing)  # Trackbar for controlling blur intensity
    cv2.createTrackbar('circpercent', 'depth', 35, 100, nothing)  # Trackbar for circularity threshold

    # Trackbars for thresholding color regions in the image
    cv2.createTrackbar('Min Color', 'depth', 0, 255, nothing)  # Trackbar for minimum color threshold
    cv2.createTrackbar('Max Color', 'depth', 0, 255, nothing)  # Trackbar for maximum color threshold

    # Set default positions for the trackbars
    cv2.setTrackbarPos('alpha', 'depth', 38)
    cv2.setTrackbarPos('param1', 'depth', 350)
    cv2.setTrackbarPos('param2', 'depth', 450)
    cv2.setTrackbarPos('blur', 'depth', 1) # Didn't seem to affect tested values
    cv2.setTrackbarPos('circpercent', 'depth', 80) # Didn't seem to affect tested values
    cv2.setTrackbarPos('Min Color', 'depth', 4)
    cv2.setTrackbarPos('Max Color', 'depth', 70)

# Process the depth frame to convert it into a colorized and gray-scale image
def process_depth_frame(depth_frame, alpha, param1, param2, blur, min_color, max_color):
    # Convert depth frame to a NumPy array
    depth_image = np.asanyarray(depth_frame.get_data())

    roi_image = depth_image[95:720, 230:750]

    # Convert the depth image into an 8-bit format and apply a color map
    depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(roi_image, alpha=alpha), cv2.COLORMAP_BONE)

    # Convert the color-mapped image to grayscale
    gframe = cv2.cvtColor(depth_cm, cv2.COLOR_BGR2GRAY)

    # Apply the color thresholding to isolate regions of interest
    gframe[gframe < min_color] = 255  # Set pixels below the min threshold to white
    gframe[gframe > max_color] = 255  # Set pixels above the max threshold to white

    # Apply median blur to reduce noise in the image
    bframe = cv2.medianBlur(gframe, (blur * 2) - 1)

    # Use Canny edge detection to detect edges in the grayscale image
    edges = cv2.Canny(gframe, param1, param2)

    return bframe, edges

# Find contours of ball-like objects based on their circularity score
def find_ball_contours(edges, circpercent):
    # Find contours from the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ball_contours = []

    # Filter contours by their circularity and aspect ratio score
    for contour in contours:
        score = shape_score(contour, circpercent)  # Calculate the shape score
        if score > circpercent:  # If the shape score is greater than the threshold
            ball_contours.append(contour)  # Add the contour to the list

    return ball_contours


# Helping function for calculating the distance between frames... For error checking
def frame_distance(frame1, frame2):
    return np.sqrt((frame1['x'] - frame2['x'])**2 + (frame1['y'] - frame2['y'])**2)

# Helping function for calculating the validity between frames... For error checking
def frame_valid_range(frame1, frame2):
    if (((frame1['x']-frame_range_threshold) < frame2['x']) and ((frame1['x']+frame_range_threshold) > frame2['x'])) and (((frame1['y']-frame_range_threshold) < frame2['y']) and ((frame1['y']+frame_range_threshold) > frame2['y'])):
        return 1
        
    return 0

# Global variable to store the timestamp of the first frame
first_frame_timestamp = None
# Draw the contours and calculate the distance of the object from the camera
def draw_and_measure(vframe, ball_contours, depth_frame):
    global frame_valid_count, first_frame_timestamp, frame_data
    
    if ball_contours:
        # Draw the contours on the image in red
        cv2.drawContours(vframe, ball_contours, -1, (0, 0, 255), 2)

        for contour in ball_contours:
            moment = cv2.moments(contour)
            if moment["m00"] != 0:
                x = int(moment["m10"] / moment["m00"])
                y = int(moment["m01"] / moment["m00"])
                coordinates = (x, y)
            else:
                coordinates = None

            # If valid coordinates are found, calculate the distance to the object
            if coordinates:
                z = (depth_frame.get_distance(230 + coordinates[0], 95 + coordinates[1]) * 3.281) # Convert meters to feet
                # If statements used to check if detected shape is in the gameboard and not in the glare
                if x >= 305 and x <= 315 and y >= 70 and y <= 85 and z >= 5.00: # Specifically for the glare
                    coordinates = None
                elif x >= 375 and x <= 390 and y >= 70 and y <= 85 and z >= 3.60: # Specifically for the glare
                    coordinates = None
                elif y >= 220: # For any other possible false detections
                    coordinates = None
                    return
                elif x >= 486 or x <= 33: # For any other possible false detections
                    coordinates = None
                    return
                timestamp = time.time()
                new_frame = {'time': timestamp, 'x': x, 'y': y, 'z': z}
                
                # If it's the first frame, store the timestamp
                if first_frame_timestamp is None:
                    first_frame_timestamp = timestamp

                # Check if 1 second has passed since the first frame
                if first_frame_timestamp and (timestamp - first_frame_timestamp >= 0.3):
                    # Clear the frame_data array after 1 second
                    frame_data = []
                    print("Frame data cleared after 1 second")

                    # Reset the timestamp to avoid multiple clears
                    first_frame_timestamp = None

                if len(frame_data) >= (frame_count - 1) and coordinates:
                    if len(frame_data) == (frame_count - 1):
                            is_valid_with_first_frame = frame_valid_range(frame_data[0], new_frame)
                            is_valid_with_second_frame = frame_valid_range(frame_data[1], new_frame)
                            is_past_frames_valid = frame_valid_range(frame_data[0], frame_data[1])
                            
                            if is_valid_with_first_frame == 1:
                                if is_valid_with_second_frame == 1:
                                    print("Valid Frame")
                                    frame_valid_count = 0
                                    frame_data.append(new_frame)
                                else:
                                    print("Frame0: X: ", frame_data[0]['x'], " Y: ", frame_data[0]['y'])
                                    print("NewFrame: X: ", new_frame['x'], " Y: ", new_frame['y'])
                                    frame_valid_count = 0
                                    frame_data.pop(1)
                                    frame_data.append(new_frame)
                            elif is_valid_with_second_frame == 1:
                                print("Frame1: X: ", frame_data[1]['x'], " Y: ", frame_data[1]['y'])
                                print("NewFrame: X: ", new_frame['x'], " Y: ", new_frame['y'])
                                frame_valid_count = 0
                                frame_data.pop(0)
                                frame_data.append(new_frame)
                            elif is_past_frames_valid == 1:
                                print("Old Frames valid")
                                frame_valid_count += 1
                                if frame_valid_count == 3:
                                    frame_data.pop(0)
                                    frame_data.pop(0)
                                    frame_data.append(new_frame)
                            else:
                                print("Clearing old frames due to invalid old frames")
                                print("Frame0: X: ", frame_data[0]['x'], " Y: ", frame_data[0]['y'])
                                print("Frame1: X: ", frame_data[1]['x'], " Y: ", frame_data[1]['y'])
                                print("NewFrame: X: ", new_frame['x'], " Y: ", new_frame['y'])
                                frame_valid_count = 0
                                frame_data.pop(0)
                                frame_data.pop(0)
                                frame_data.append(new_frame)
                else:
                    print("NewFrame: X: ", new_frame['x'], " Y: ", new_frame['y'])
                    frame_data.append(new_frame)
                    frame_valid_count = 0

                # Draw and display the calculated distance and coordinates on the frame
                cv2.circle(vframe, coordinates, 5, (255, 0, 0), -1)  # Draw a blue circle on the object
                cv2.putText(vframe, f"{z:.2f} ft", coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if len(frame_data) == frame_count:
                    print("Calculating Velocity and acceleration")
                    # Calculate velocity and acceleration using the last 3 frames
                    
                    print("F0 X: ", frame_data[0]['x'], " Y: ", frame_data[0]['y'])
                    print("F1 X: ", frame_data[1]['x'], " Y: ", frame_data[1]['y'])
                    print("F2 X: ", frame_data[2]['x'], " Y: ", frame_data[2]['y'])
                    
                    velocity1 = (frame_data[1]['z'] - frame_data[0]['z']) / (frame_data[1]['time'] - frame_data[0]['time'])
                    velocity2 = (frame_data[2]['z'] - frame_data[1]['z']) / (frame_data[2]['time'] - frame_data[1]['time'])
                    acceleration = (velocity2 - velocity1) / (frame_data[2]['time'] - frame_data[0]['time'])
                    # Displays the acceleration
                    cv2.putText(vframe, f"{acceleration:.2f}", (640,0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    print(acceleration)

                    AimAtBall()
                    print("going")
                    time.sleep(100/1000)
                    z_value = float(frame_data[2]['z'])
                    print(z_value*12)
                    fire_delay_time = calculate_intercept_time(25, (z_value*12), velocity2, acceleration)
               
                    print("going2")
                    Fire(fire_delay_time)

                    frame_data.pop(0)
                    frame_data.pop(0)
                    frame_data.pop(0)

def GetAverageLine():
    avg = 0
    data_points = 0

    # Check if frame_data is not empty
    if len(frame_data) > 0:
        for frame in frame_data:
            # Calculate the line data for the current frame
            line_data = find_line((frame['z'] * 12), frame['x'], frame['y'])
            # Sum up all line data
            avg += line_data
            print("Line: ", line_data, " Dist: ", frame['z'], " X: ", frame['x'], " Y: ", frame['y'])
            print(line_data)
            # Increment the data points counter
            data_points += 1
        
        # Calculate the average line data
        avg /= data_points
        print(avg)
        return round(avg)
    
    # Return a default value if there are no data points
    else:
        return 120

def AimAtBall():
    avg_line = GetAverageLine()
    X_line = int(avg_line)  # Make sure X is an integer
    Y_pos = 2  # Assuming Y is constant here; adjust as needed
    if X_line != 120:
        SendCords((X_line - 1), Y_pos)

# Main function that runs the program
def main():
    setup_gpio()  # Initialize GPIO pins
    pipe = setup_pipeline()  # Start the RealSense pipeline
    create_trackbars()  # Set up the OpenCV window and trackbars
    
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off buzzer
    
    time.sleep(1)
    
    # Starting sound
    Buzz(.05)
    Buzz(.25)
    Buzz(.05)
    Buzz(.25)
    Buzz(.05)
    Buzz(.25)
    Buzz(.05)
    Buzz(.25)

    # Testing find_line Function
    distance = 62
    x = 184
    y = 30
    starttime = time.time()
    find_line(distance, x, y)
    endtime = time.time()
    print(endtime-starttime)
    # End of testing find_line_function

    # Main Loop
    while True:
        start_time = time.time()
        
        # Get frames from the RealSense camera
        frame = pipe.wait_for_frames()
        depth_frame = frame.get_depth_frame()  # Get the depth frame

        # Get values from the trackbars
        alpha = cv2.getTrackbarPos('alpha', 'depth') / 1000
        param1 = cv2.getTrackbarPos('param1', 'depth')
        param2 = cv2.getTrackbarPos('param2', 'depth')
        blur = cv2.getTrackbarPos('blur', 'depth')
        circpercent = cv2.getTrackbarPos('circpercent', 'depth')
        min_color = cv2.getTrackbarPos('Min Color', 'depth')
        max_color = cv2.getTrackbarPos('Max Color', 'depth')

        # Process the depth frame to prepare it for contour detection
        bframe, edges = process_depth_frame(depth_frame, alpha, param1, param2, blur, min_color, max_color)
        ball_contours = find_ball_contours(edges, circpercent)  # Find circular contours

        # Convert the processed grayscale frame back to color for visualization
        vframe = cv2.cvtColor(bframe, cv2.COLOR_GRAY2BGR)
        draw_and_measure(vframe, ball_contours, depth_frame)  # Draw contours and measure distance
        
        end_time = time.time()
        processing_time = end_time - start_time
        #print(processing_time)

        #cv2.imshow('image', vframe)  # Display the frame

        # Set the GPIO output high while processing
        GPIO.output(SCRIPT_RUNNING_PIN, GPIO.LOW)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('b'):
            Fire(126)
            
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('c'):
            # Sent Info [x (0-31), y(0-3)]
            SendCords(10, 3)
            
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('v'):
            # Sent Info [x (0-31), y(0-3)]
            SendCords(20, 1)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up GPIO pins and stop the pipeline
    GPIO.output(SCRIPT_RUNNING_PIN, GPIO.LOW)  # Set GPIO output low
    GPIO.cleanup()  # Reset GPIO settings
    pipe.stop()  # Stop the RealSense pipeline
    cv2.destroyAllWindows()  # Close all OpenCV windows

# Start the program
if __name__ == "__main__":
    main()
