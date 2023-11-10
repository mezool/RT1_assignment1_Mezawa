from __future__ import print_function

import time
from sr.robot import *

"""
assignment python script

control the robot to put all the golden boxes together
	This code can be run with:
	$ python run.py assignment.py
"""

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

d_put = 0.5
""" float: Threshold for collecting boxes"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(gra):
    """
    Function to find the token
    If the robot is grabbing a token, find the second closest token to locate the place where the robot collect them,
    otherwise, find the closest token to grab.

    Args: gra (int): show whether robot is grabing a token or not.
          0: robot is not grabbing a token.
          1: robot is grabbing a token.
    """
    dist = 100
    for token in R.see():
        if gra == 0:
            if token.dist < dist:
                dist = token.dist
                rot_y = token.rot_y
        else:
            if d_th < token.dist < dist: #Prevent the robot from finding the token it already has
                dist = token.dist
                rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

def move(gra,i):
    """
    Function to collect tokens.

    Args, returns: 
            gra (int): show whether robot is grabing a token or not.
                0: robot is not grabbing a token.
                1: robot is grabbing a token.
            i (int) the number of boxes the robot has already gathered
    """
    dist, rot_y = find_token(gra)  # look for markers
    if dist == -1:  # if no token is detected, the robot turns
        print("I don't see any token!!")
        if gra == 0:
            turn(+10, 1)
        else:
            turn(-10,1) # Rotate in opposite directions to prevent tokens from gathering in more than one place.
    elif gra == 0 and dist < d_th:  # if the robot is close to the token and robot is not grabbing any token, the robot grabs it.
        print("Found it!")
        if R.grab(): 
            print("Gotcha!")
            gra = 1 # change the variable which shows the robot is grabbing a token.
        else:
            print("Aww, I'm not close enough.")
    elif gra == 1 and dist < d_put:  # if the robot is close to the token and robot is grabbing a token, the robot releases it.
        print("Arrived!")  
        R.release()
        gra = 0 # change the variable which shows the robot is not grabbing any token.
        i = i + 1 #increase the number of boxes the robot has already gathered
        drive(-20, 2)
        turn(10, 2) #move and turn to prevent the robot from grabbing the same box
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(30, 0.5)
    elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)    
    return gra, i

marker = 6
i = 0 #the boxes robot gathered
gra = 0 #variable which show whether robot have token or not
while i < marker - 1: #To gather all tokens, the robot has to move all tokens minus one
    gra, i = move(gra,i)
print("Mission Completed") #complete