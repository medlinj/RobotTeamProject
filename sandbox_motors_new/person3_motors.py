"""
Functions for TURNING the robot LEFT and RIGHT.
Authors: David Fisher, David Mutchler and Joe Krisciunas.
"""  # Done

# Done
#          Test and correct as needed.
#   Then repeat for turn_left_by_time.
#   Then repeat for turn_left_by_encoders.
#   Then repeat for the turn_right functions.

import ev3dev.ev3 as ev3cd
import time


def test_turn_left_turn_right():
    while True:
        seconds = int(input('how many seconds we going?'))
        speed = int(input('what speed we going?'))
        stop_action = input('what stop action we using?')
        secondsx = int(input('how many seconds we going?'))
        if secondsx == 0:
            break



    turn_left_seconds(seconds,speed, stop_action)
    while True:

        seconds2 = int(input('how many seconds we going?'))
        speed = int(input('what speed we going?'))
        stop_action = input('what stop action we using?')
        degrees = int(input('how many degrees we going?'))
        secondsx = int(input('how many seconds we going?'))
        if secondsx == 0:
            break

    turn_left_by_time(degrees, speed, stop_action)

    while True:

        seconds1 = int(input('how many seconds we going?'))
        speed = int(input('what speed we going?'))
        stop_action = input('what stop action we using?')
        degrees = int(input('how many degrees we going?'))
        secondsx = int(input('how many seconds we going?'))
        if secondsx == 0:
            break
    turn_left_by_encoders(degrees, speed, stop_action)

    while True:

        seconds3 = int(input('how many seconds we going?'))

        speed = int(input('what speed we going?'))
        stop_action = input('what stop action we using?')
        degrees = int(input('how many degrees we going?'))
        secondsx = int(input('how many seconds we going?'))
        if secondsx == 0:
            break

    turn_right_by_time(degrees,speed,stop_action)
    turn_right_seconds(seconds3,speed,stop_action)
    turn_right_by_encoders(degrees,speed,stop_action)


    """
    Tests the turn_left and tupythonrn_right functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets degrees and runs turn_left_by_time.
      3. Same as #2, but runs turn_left_by_encoders.
      4. Same as #1, 2, 3, but tests the turn_right functions.
    """


def turn_left_seconds(seconds, speed, stop_action):
    left_motor = ev3cd.LargeMotor(ev3cd.OUTPUT_B)
    left_motor.run_forever(speed_sp = speed*8)
    time.sleep(seconds)
    left_motor.stop(stop_action = stop_action)





    """
    Makes the robot turn in place left for the given number of seconds at the given speed,
    where speed is between -100 (full speed turn_right) and 100 (full speed turn_left).
    Uses the given stop_action.
    """


def turn_left_by_time(degrees, speed, stop_action):
    left_motor = ev3cd.LargeMotor(ev3cd.OUTPUT_B)
    t1 = degrees/speed
    left_motor.run_forever(speed_sp=speed * 8)
    time.sleep(t1)
    left_motor.stop(stop_action = stop_action)
    """
    Makes the robot turn in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed turn_right) and 100 (full speed turn_left).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """


def turn_left_by_encoders(degrees, speed, stop_action):
    left_motor = ev3cd.LargeMotor(ev3cd.OUTPUT_B)
    left_motor.run_to_rel_pos(speed_sp=speed * 8, position_sp=degrees*4.2)
    left_motor.wait_while(ev3cd.LargeMotor.STATE_RUNNING)
    left_motor.stop(stop_action=stop_action)
    """
    Makes the robot turn in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed turn_right) and 100 (full speed turn_left).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should turn to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """


def turn_right_seconds(seconds, speed, stop_action):
    """ Calls turn_left_seconds with negative speeds to achieve turn_right motion. """
    left_motor = ev3cd.LargeMotor(ev3cd.OUTPUT_B)
    left_motor.run_forever(speed_sp=-speed * 8)
    time.sleep(seconds)
    left_motor.stop(stop_action=stop_action)


def turn_right_by_time(degrees, speed, stop_action):
    left_motor = ev3cd.LargeMotor(ev3cd.OUTPUT_B)
    t1 = degrees/speed
    left_motor.run_forever(speed_sp=-speed * 8)
    time.sleep(t1)
    left_motor.stop(stop_action = stop_action)
""" Calls turn_left_by_time with negative speeds to achieve turn_right motion. """
def turn_right_by_encoders(degrees, speed, stop_action):
    degrees = degrees * 8
    left_motor = ev3cd.LargeMotor(ev3cd.OUTPUT_B)
    left_motor.run_to_rel_pos(speed_sp=-speed * 8, position_sp=degrees*4)
    left_motor.wait_while(ev3cd.LargeMotor.STATE_RUNNING)
    left_motor.stop(stop_action=stop_action)
    """ Calls turn_left_by_encoders with negative speeds to achieve turn_right motion. """


test_turn_left_turn_right()