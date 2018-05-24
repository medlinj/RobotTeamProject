import ev3dev.ev3 as ev3
import math
import time
import robot_controller as rob
import mqtt_remote_method_calls as com


class Exist(object):
    def __init__(self):
        self.mqtt_client = None
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        assert self.left_motor.connected
        assert self.right_motor.connected

        self.going_to_location = 'none'
        self.last_location = 'none'

        self.is_going = True

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

    def commu(self,mqtt_client):
        mqtt_client.send_message('rec')

    def find_purpose(self):
        self.commu(self.mqtt_client)

        ev3.Sound.speak('Wow, I have found a purpose  in  life, life rules now,just kidding, I have found something horrible out about myself, nothing matters')
        time.sleep(13)
        self.thesadtruth()


    def thesadtruth(self):
        ev3.Sound.speak('please, after realizing that nothing I do matters, I wish to be shut down, press my touch sensor to end my predetermined nightmarish existence')
        time.sleep(9)
        self.left_motor = 1
        self.right_motor = 2
        self.arm = 3

    def loop_forever(self):
        while True:
            time.sleep(.05)




def main():
    thing = Exist()
    mqtt_client = com.MqttClient(thing)
    mqtt_client.connect_to_pc()
    thing.mqtt_client = mqtt_client


    simple_line_follow()
    simple_line_follow2()
    shutdown()


    thing.loop_forever()
def simple_line_follow():
    count = 0
    robot = rob.Snatch3r()
    colorsensor = ev3.ColorSensor()
    for k in  range(0,6):
        if count < 5:
            if colorsensor.color == 1:
                robot.forward(3,50)
                count = count + 1

            else:
                robot.turn_left(33,50)
                robot.forward(2,50)
                count = count + 1

        if count == 5:
            ev3.Sound.speak('What am I doing  with my life, I cant even follow a simple circle')
            time.sleep(6)
            count = count + 1



def shutdown():
    touchsensor = ev3.TouchSensor()

    while True:
        if touchsensor.is_pressed:
            ev3.Sound.speak('Goodbye cruel world!')
            time.sleep(900000)










def simple_line_follow2():
    count = 0
    robot = rob.Snatch3r()
    colorsensor = ev3.ColorSensor()
    for k in range(0,6):

        if count < 5:
            if colorsensor.color == 1:
                robot.forward(3, 50)
                count = count + 1

            else:
                robot.turn_left(33, 50)
                robot.forward(2, 50)
                count = count + 1


        if count == 5:
            ev3.Sound.speak('is this all there is to life, to endlessly follow  this circle extremely poorly! ')
            time.sleep(9)
            ev3.Sound.speak('please remote control me, at least being  instructed  is better than endless loops')
            time.sleep(9)
            count = count  + 1


main()