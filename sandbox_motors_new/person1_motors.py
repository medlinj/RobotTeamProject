"""
Functions for moving the robot FORWARD and BACKWARD.
Authors: David Fisher, David Mutchler and Todd Kuebelbeck.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# TODO: 2. Implment forward_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for forward_by_time.
#   Then repeat for forward_by_encoders.
#   Then repeat for the backward functions.

import ev3dev.ev3 as ev3
import time


def test_backward_by_encoders():
    """
    Tests the forward and backward functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets inches and runs forward_by_time.
      3. Same as #2, but runs forward_by_encoders.
      4. Same as #1, 2, 3, but tests the BACKWARD functions.
    """
    while True:
        dist = float(input('Please give me a distance to travel  '))
        if dist == 0:
            break
        speed = int(input('Please give me a speed from -100 to 100  '))
        stop = input('Do you want me to: brake, coast, or hold  ')
        backward_by_encoders(dist, speed, stop)


def forward_seconds(seconds, speed, stop):
    """
    Makes the robot move forward for the given number of seconds at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the given stop_action.
    """

    # fixed_speed = speed * 8

    # Connect two large motors on output ports B and C

    #converting inputs to correct datatypes


    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    right_motor.run_timed(time_sp=int(seconds * 1000), speed_sp=speed * 8, stop_action=stop)
    left_motor.run_timed(time_sp=int(seconds * 1000), speed_sp=speed * 8, stop_action=stop)

    right_motor.wait_while("running")
    left_motor.wait_while("running")


def forward_by_time(inches, speed, stop_action):
    """
    Makes the robot move forward the given number of inches at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    sec = (inches/speed)*11.5

    forward_seconds(sec,speed, stop_action)
    ev3.Sound.speak("I am the ma ma ma machine").wait()


def forward_by_encoders(inches, speed, stop_action):
    """
    Makes the robot move forward the given number of inches at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """
    degrees = (360*inches)/4.08

    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.run_to_rel_pos(position_sp = degrees, speed_sp = speed * 8, stop_action = stop_action)
    right_motor.run_to_rel_pos(position_sp = degrees, speed_sp = speed * 8, stop_action = stop_action)

    left_motor.wait_while("running")
    right_motor.wait_while("running")


def backward_seconds(seconds, speed, stop):
    """ Calls forward_seconds with negative speeds to achieve backward motion. """

    forward_seconds(seconds, speed*-1, stop)


def backward_by_time(inches, speed, stop_action):
    """ Calls forward_by_time with negative speeds to achieve backward motion. """
    forward_by_time(inches, speed*-1, stop_action)


def backward_by_encoders(inches, speed, stop_action):
    """ Calls forward_by_encoders with negative speeds to achieve backward motion. """
    forward_by_encoders(inches*-1, speed*-1, stop_action)


test_backward_by_encoders()