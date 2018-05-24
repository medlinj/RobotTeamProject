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

#Helper class for pc controller
#Todd Kuebelbeck
#Rose-Hulman Institute of Technology, CSSE120

import ev3dev.ev3 as ev3
import math
import time
import mqtt_remote_method_calls as com


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

        # self.pixy = ev3.Sensor(driver_name="pixy_lego")
        # self.pixy.mode = "SIG1"

        self.sig_str = "SIG1"

        self.target_area = 0

        self.soda_type = 'none'

        self.has_soda = False

        self.current_color = 'none'
        self.last_color = 'none'

        self.status = 'Connection to robot is established'

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
        exit()


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
        self.spin_left(90, speed=60, stop_action='brake')
        self.forward(18, speed=60, stop_action='brake')
        self.spin_right(90, speed=60, stop_action='brake')
        self.forward(20, speed=60, stop_action='brake')
        self.spin_right(90, speed=60, stop_action='brake')
        self.forward(18, speed=60, stop_action='brake')
        self.spin_left(90, speed=60, stop_action='brake')

    # def change_status(self, mqtt_client, status_to_send):
    #     mqtt_client.send_message("change_status", [status_to_send])

    def x_pos(self):
        self.set_curr_color()
        pixy = ev3.Sensor(driver_name="pixy-lego")
        pixy.mode = self.sig_str

        return (pixy.value(1) - 150) / 10

    def is_right(self):
        if self.x_pos() > 0:
            return True
        else:
            return False

    def is_left(self):
        if self.x_pos() < 0:
            return True
        else:
            return False

    def trace(self):
        # DONE: remove infinite loop
        corrected_x = self.x_pos() - 3

        while math.fabs(corrected_x) > 4:
            corrected_x = self.x_pos() - 3

            print(corrected_x)
            if math.fabs(corrected_x) > 4:
                if self.is_left():
                    self.spin_left(5, speed=50, stop_action='coast')
                if self.is_right():
                    self.spin_right(5, speed=50, stop_action='coast')


        # while True:
        #     if self.is_right() is True:
        #         self.spin_right(1, speed=40, stop_action='coast')
        #     elif self.is_left() is True:
        #         self.spin_left(1, speed=40, stop_action='coast')

    def test_trace_pos(self):

        while True:
            pixy = ev3.Sensor(driver_name="pixy-lego")
            self.set_curr_color()

            pixy.mode = self.sig_str

            print("Current color: ", self.current_color)
            print("X pos:   ", pixy.value(1))

            time.sleep(0.5)

    def set_curr_color(self):
        # runs a loop that will change the signature and determine which one the sensor is currently seeing
        # This will also set the last color if it has changed

        pixy = ev3.Sensor(driver_name="pixy-lego")

        area = list()

        pixy.mode = "SIG1"
        area.append(pixy.value(3) * pixy.value(4))

        pixy.mode = "SIG2"
        area.append(pixy.value(3) * pixy.value(4))

        pixy.mode = "SIG3"
        area.append(pixy.value(3) * pixy.value(4))

        pixy.mode = "SIG4"
        area.append(pixy.value(3) * pixy.value(4))

        primary_sig = area.index(max(area)) + 1

        self.target_area = area[primary_sig - 1]

        if primary_sig is 1:
            self.sig_str = "SIG1"
            self.last_color = self.current_color
            self.current_color = 'green'
            return

        if primary_sig is 2:
            self.sig_str = "SIG2"
            self.last_color = self.current_color
            self.current_color = 'blue'
            return

        if primary_sig is 3:
            self.sig_str = "SIG3"
            self.last_color = self.current_color
            self.current_color = 'red'
            return

        if primary_sig is 4:
            self.sig_str = "SIG4"
            self.last_color = self.current_color
            self.current_color = 'orange'
            return


        # area = 20
        # pixy = ev3.Sensor(driver_name="pixy-lego")
        #        while True:
        # # Check for green
        # pixy.mode = "SIG1"
        # if pixy.value(3) * pixy.value(4) > area:
        #     self.last_color = self.current_color
        #     self.current_color = 'green'
        #     return
        #
        # # Check for blue
        # pixy.mode = "SIG2"
        # if pixy.value(3) * pixy.value(4) > area:
        #     self.last_color = self.current_color
        #     self.current_color = 'blue'
        #     return
        # # Check for red
        # pixy.mode = "SIG3"
        # if pixy.value(3) * pixy.value(4) > area:
        #     self.last_color = self.current_color
        #     self.current_color = 'red'
        #     return
        # # Check for orange
        # pixy.mode = "SIG4"
        # if pixy.value(3) * pixy.value(4) > area:
        #     self.last_color = self.current_color
        #     self.current_color = 'orange'
        #     return

    def color_tester(self):
        # Tests the color detection

        # while True:
        #     pixy = ev3.Sensor(driver_name="pixy-lego")
        #     pixy.mode = "SIG1"
        #     print("(X, Y)=({}, {}) Width={} Height={}".format(
        #         pixy.value(1), pixy.value(2), pixy.value(3),
        #         pixy.value(4)))
        #     time.sleep(.5)

        while True:
            self.set_curr_color()
            print('Current Color: ', self.current_color, ' Previous color: ', self.last_color)
            print('Area: ', self.target_area)
            time.sleep(0.5)

    def soda_request(self, soda_input_pc):
        self.soda_type = soda_input_pc

    def delivery(self):
        ev3.Sound.speak("Your soda is here, but please wait until I tell you to grab it")
        self.arm_down()
        self.backward(5, speed=40, stop_action='brake')
        ev3.Sound.speak("You may now take your soda. Enjoy!")

    def vending(self):
        # TODO: Change back speed argument
        self.spin_left(90, speed=100, stop_action='brake')
        self.forward(15, speed=100, stop_action='brake')
        #TODO set correct distance

        # DONE REMOVE ARM DOWN


        ev3.Sound.speak("Excuse me")
        time.sleep(2)
        ev3.Sound.speak("I am down here, the robot")
        time.sleep(3)
        ev3.Sound.speak("Do you mind buying me a")
        time.sleep(4)
        ev3.Sound.speak("", str(self.soda_type))
        time.sleep(2)
        ev3.Sound.speak("Please put soda in my gripper")

        dist_sensor = ev3.InfraredSensor()


        # Waits until soda is placed within 4cm of the gripper
        #TODO remove print testing statement

        while True:
            dist = dist_sensor.proximity
            print('Distance:  ', int(dist))
            if int(dist) < 2:
                break
            time.sleep(0.75)

        self.has_soda = True
        self.is_going = False
        self.is_coming = True

        ev3.Sound.speak("Thank you very much human, please press my touch sensor to send me back")

        touch_sensor = ev3.TouchSensor()
        while True:
            if touch_sensor.is_pressed:
                break


        time.sleep(2)
        self.arm_up()

        # Set to coast, due to fear of angular momentum possibly tipping the robot if it were to brake
        self.spin_right(180, speed=100, stop_action='coast')
        self.forward(15, speed=100, stop_action='coast')
        self.spin_right(90, speed=100, stop_action='coast')

        #DONE REMOVE THE ARM DOWN!!!
        #self.arm_down()


    # DONE: Create a vending machine script for when red is reached


    def start_fetch(self):
        # function that will drive the bot
        in_robot_controller = com.MqttClient()
        in_robot_controller.connect_to_pc()

        in_robot_controller.send_message("change_status_code", [0])
        # TODO: Remove the test and change with self.status

        while self.current_color is not 'green':
            self.set_curr_color()
            print('Waiting for green. CURRENT:   ', self.current_color)
            print('Soda that is set currently is:   ', self.soda_type)
        if self.current_color is 'green':
            in_robot_controller.send_message("change_status_code", [1])
            self.forward(25, speed=75, stop_action='brake')
            self.spin_left(90, speed=75, stop_action='brake')

        while self.current_color is not 'blue':
            self.set_curr_color()
            print('Waiting for blue. CURRENT COLOR:   ', self.current_color)
        if self.current_color is 'blue':
            in_robot_controller.send_message("change_status_code", [2])
            self.drive_to()
            self.go_around()


        while self.current_color is not 'red':
            self.set_curr_color()
            print('Waiting for red. CURRENT COLOR:   ', self.current_color)
        if self.current_color is 'red':
            in_robot_controller.send_message("change_status_code", [3])
            self.drive_to()
            in_robot_controller.send_message("change_status_code", [4])
            self.vending()
            in_robot_controller.send_message("change_status_code", [5])

        while self.current_color is not 'blue':
            self.set_curr_color()
            print('Waiting for blue. CURRENT COLOR:   ', self.current_color)
        if self.current_color is 'blue':
            in_robot_controller.send_message("change_status_code", [2])
            self.drive_to()
            self.go_around()

        while self.current_color is not 'orange':
            self.set_curr_color()
            print('Waiting for orange. CURRENT COLOR:   ', self.current_color)
        if self.current_color is 'orange':
            in_robot_controller.send_message("change_status_code", [6])
            self.drive_to()
            self.spin_right(90, speed=50, stop_action='brake')

        self.delivery()
        in_robot_controller.send_message("change_status_code", [7])



      #DONE: create and add a "drive to" function that will take it to the vending machine
    def drive_to(self):

        while True:
            self.set_curr_color()

            pixy = ev3.Sensor(driver_name='pixy-lego')
            pixy.mode = self.sig_str

            # Checking to see whether it is close enough to no longer drive to object
            area = (pixy.value(3)*pixy.value(4))/10
            print("Area:  ", area)
            print("Current Color:   ", self.current_color)
            if area > 100:
                break

            self.trace()
            self.forward(7, speed=70, stop_action='coast')












