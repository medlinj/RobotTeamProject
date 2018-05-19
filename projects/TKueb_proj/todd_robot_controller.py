"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    # DONE: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        assert self.left_motor.connected
        assert self.right_motor.connected

        self.pixy = ev3.Sensor(driver_name="pixy_lego")

        self.soda_type = 'none'

        self.has_soda = False

        self.current_color = 'none'
        self.last_color = 'none'

        self.is_going = True
        self.is_coming = False

    def forward(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.2
        degrees_motor = k * inches
        self.left_motor.run_to_rel_pos(position_sp=degrees_motor, speed_sp=8 * speed, stop_action=stop_action)

        self.right_motor.run_to_rel_pos(position_sp=degrees_motor, speed_sp=8 * speed, stop_action=stop_action)
        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")

    def backward(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.2
        degrees_motor = -k * inches
        self.left_motor.run_to_rel_pos(position_sp=degrees_motor, speed_sp=-8 * speed, stop_action=stop_action)

        self.right_motor.run_to_rel_pos(position_sp=degrees_motor, speed_sp=-8 * speed, stop_action=stop_action)
        self.left_motor.wait_while("running")
        self.right_motor.wait_while("running")
    def turn_left(self, degrees, speed, stop_action='brake'):
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        right_motor.run_to_rel_pos(speed_sp=speed * 8, position_sp=degrees * 13)
        right_motor.wait_while(ev3.LargeMotor.STATE_RUNNING)
        right_motor.stop(stop_action=stop_action)

    def turn_right(self, degrees, speed, stop_action='brake'):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        left_motor.run_to_rel_pos(speed_sp=speed * -8, position_sp=degrees * -13)
        left_motor.wait_while(ev3.LargeMotor.STATE_RUNNING)
        left_motor.stop(stop_action=stop_action)

    def spin_left(self, degrees, speed, stop_action):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        robot_degrees = degrees * 4.2

        left_motor.speed_sp = speed * (8)
        left_motor.run_to_rel_pos(position_sp=-robot_degrees)
        right_motor.speed_sp = speed * 8
        right_motor.run_to_rel_pos(position_sp=robot_degrees)
        right_motor.wait_while('running')
        left_motor.wait_while('running')
        left_motor.stop(stop_action=stop_action)
        right_motor.stop(stop_action=stop_action)

    def spin_right(self, degrees, speed, stop_action):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        robot_degrees = degrees * 4.2

        left_motor.speed_sp = speed * 8
        right_motor.speed_sp = speed * 8
        left_motor.run_to_rel_pos(position_sp=robot_degrees)
        right_motor.run_to_rel_pos(position_sp=-robot_degrees)
        left_motor.wait_while('running')
        right_motor.wait_while('running')
        left_motor.stop(stop_action=stop_action)
        right_motor.stop(stop_action=stop_action)

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        self.arm.stop()
        self.left_motor.stop()
        self.right_motor.stop()
        self.running = False

    def move(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def arm_up(self):
        self.arm.run_forever(speed_sp=700)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm.run_to_rel_pos(position_sp=-14.2 * 360)
        self.arm.wait_while(ev3.Motor.STATE_RUNNING)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        self.arm.stop(stop_action='brake')

    def changing_direction(self):
        if self.is_going is True:
            self.is_going = False
        else:
            self.is_going = True

    def go_around(self):

        # used to navigate around objects
        self.spin_left(90, speed=300, stop_action='brake')
        self.forward(10, speed=300, stop_action='brake')
        self.spin_right(90, speed=300, stop_action='brake')
        self.forward(10, speed=300, stop_action='brake')
        self.spin_right(90, speed=300, stop_action='brake')
        self.forward(10, speed=300, stop_action='brake')
        self.spin_left(90, speed=300, stop_action='brake')

    def set_curr_color(self):
        # runs a loop that will change the signature and determine which one the sensor is currently seeing
        # This will also set the last color if it has changed
        # TODO: Figure out acceptable area
        area = 10

        # Check for green
        self.pixy.mode = "SIG1"
        if self.pixy.value(3) * self.pixy.value(4) > area:
            self.last_color = self.current_color
            self.current_color = 'green'
            return

        # Check for blue
        self.pixy.mode = "SIG2"
        if self.pixy.value(3) * self.pixy.value(4) > area:
            self.last_color = self.current_color
            self.current_color = 'blue'
            return
        # Check for red
        self.pixy.mode = "SIG3"
        if self.pixy.value(3) * self.pixy.value(4) > area:
            self.last_color = self.current_color
            self.current_color = 'red'
            return
        # Check for orange
        self.pixy.mode = "SIG4"
        if self.pixy.value(3) * self.pixy.value(4) > area:
            self.last_color = self.current_color
            self.current_color = 'orange'
            return

    def color_tester(self):
        # Tests the color detection
        self.set_curr_color()
        print('Current Color: ', self.current_color, ' Previous color: ', self.last_color)
        time.sleep(3)

    def soda_request(self, soda_input_pc):
        self.soda_type = soda_input_pc

    def vending(self):
        self.spin_left(90, speed=100, stop_action='brake')
        self.forward(72, speed=400, stop_action='brake')
        #TODO set correct distance

        ev3.Sound.speak("Excuse me")
        time.sleep(2)
        ev3.Sound.speak("I am down here, the robot")
        time.sleep(3)
        ev3.Sound.speak("Do you mind buying me a", self.soda_type,)
        time.sleep(2)
        ev3.Sound.speak("Please put soda in my gripper")


        dist_sensor = ev3.InfraredSensor
        dist = dist_sensor.proximity

        # Waits until soda is placed within 4 cm of the gripper
        while True:
            if dist < 4:
                break

        self.has_soda = True
        self.is_going = False
        self.is_coming = True

        ev3.Sound.speak("Thank you very much human")
        self.arm_up()

        # Set to coast, due to fear of angular momentum possibly tipping the robot if it were to brake
        self.spin_right(180, speed='200', stop_action='coast')
        self.forward(72, speed=400, stop_action='coast')
        self.spin_right(90, speed=200, stop_action='coast')


    # DONE: Create a vending machine script for when red is reached


    def start_fetch_loop(self):
        # function that will drive the bot

        self.color_tester()

        if self.current_color is 'green':
            self.spin_left(90, speed=100, stop_action='brake')

        if self.current_color is 'blue':
            #TODO: create and add a "drive to" function

        if self.current_color is 'red':
            #TODO: create and add a "drive to" function that will take it to the vending machine










