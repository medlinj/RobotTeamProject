"""
Functions for SPINNING the robot LEFT and RIGHT.
Authors: David Fisher, David Mutchler and JD Medlin.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# TODO: 2. Implement spin_left_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for spin_left_by_time.
#   Then repeat for spin_left_by_encoders.
#   Then repeat for the spin_right functions.


import ev3dev.ev3 as ev3
import time

left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)


def test_spin_left_spin_right():
    """
    Tests the spin_left and spin_right functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets degrees and runs spin_left_by_time.
      3. Same as #2, but runs spin_left_by_encoders.
      4. Same as #1, 2, 3, but tests the spin_right functions.
    """
    # while True:
    #     r1 = int(input('How long should the duration of movement be?'))
    #     if r1 != 0:
    #         break
    # r2 = int(input('How fast should motors move from -100 to 100?'))
    # r3 = input('How should motors stop? (brake, coast, hold)')
    #
    # spin_left_seconds(r1, r2, r3)

    # while True:
    #     r1 = int(input('How many degrees?'))
    #     if r1 != 0:
    #         break
    # r2 = int(input('How fast should motors move from -100 to 100?'))
    # r3 = input('How should motors stop? (brake, coast, hold)')
    # spin_left_by_time(r1, r2, r3)

    # while True:
    #     r1 = int(input('How many degrees?'))
    #     if r1 != 0:
    #         break
    # r2 = int(input('How fast should motors move from -100 to 100?'))
    # r3 = input('How should motors stop? (brake, coast, hold)')
    # spin_left_by_encoders(r1, r2, r3)

    # while True:
    #     r1 = int(input('How long should the duration of movement be?'))
    #     if r1 != 0:
    #         break
    # r2 = int(input('How fast should motors move from -100 to 100?'))
    # r3 = input('How should motors stop? (brake, coast, hold)')
    # spin_right_seconds(r1, r2, r3)

    # while True:
    #     r1 = int(input('How many degrees?'))
    #     if r1 != 0:
    #         break
    # r2 = int(input('How fast should motors move from -100 to 100?'))
    # r3 = input('How should motors stop? (brake, coast, hold)')
    # spin_right_by_time(r1, r2, r3)

    while True:
        r1 = int(input('How many degrees?'))
        if r1 != 0:
            break
    r2 = int(input('How fast should motors move from -100 to 100?'))
    r3 = input('How should motors stop? (brake, coast, hold)')
    spin_right_by_encoders(r1, r2, r3)

def spin_left_seconds(seconds, speed, stop_action):
    """
    Makes the robot spin in place left for the given number of seconds at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the given stop_action.
    """

    left_motor.run_forever(speed_sp=(-8*speed))
    right_motor.run_forever(speed_sp=(8*speed))

    time.sleep(seconds)

    left_motor.stop(stop_action=stop_action)
    right_motor.stop(stop_action=stop_action)


def spin_left_by_time(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    tiempo = degrees / 45
    left_motor.run_forever(speed_sp=(-8*speed))
    right_motor.run_forever(speed_sp=(8*speed))

    time.sleep(tiempo)

    left_motor.stop(stop_action=stop_action)
    right_motor.stop(stop_action=stop_action)


def spin_left_by_encoders(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """
    robot_degrees = degrees * 5

    left_motor.speed_sp = speed*(8)
    left_motor.run_to_rel_pos(position_sp=-robot_degrees)
    right_motor.speed_sp = speed*8
    right_motor.run_to_rel_pos(position_sp=robot_degrees)
    right_motor.wait_while('running')
    left_motor.wait_while('running')
    left_motor.stop(stop_action=stop_action)
    right_motor.stop(stop_action=stop_action)


def spin_right_seconds(seconds, speed, stop_action):
    """ Calls spin_left_seconds with negative speeds to achieve spin_right motion. """

    left_motor.run_forever(speed_sp=(8*speed))
    right_motor.run_forever(speed_sp=(-8*speed))

    time.sleep(seconds)

    right_motor.stop(stop_action=stop_action)
    left_motor.stop(stop_action=stop_action)


def spin_right_by_time(degrees, speed, stop_action):
    """ Calls spin_left_by_time with negative speeds to achieve spin_right motion. """

    tiempo = degrees / 43

    left_motor.run_forever(speed_sp=-8*speed)
    right_motor.run_forever(speed_sp=8*speed)

    time.sleep(tiempo)

    left_motor.stop(stop_action=stop_action)
    right_motor.stop(stop_action=stop_action)


def spin_right_by_encoders(degrees, speed, stop_action):
    """ Calls spin_left_by_encoders with negative speeds to achieve spin_right motion. """

    robot_degrees = degrees * 5

    left_motor.speed_sp = speed * 8
    right_motor.speed_sp = speed * 8
    left_motor.run_to_rel_pos(position_sp=robot_degrees)
    right_motor.run_to_rel_pos(position_sp=-robot_degrees)
    left_motor.wait_while('running')
    right_motor.wait_while('running')
    left_motor.stop(stop_action=stop_action)
    right_motor.stop(stop_action=stop_action)

test_spin_left_spin_right()
