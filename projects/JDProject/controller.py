import ev3dev.ev3 as ev3
import time


class RobotDelegate(object):
    def __init__(self):
        self.left_paw = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_paw = ev3.LargeMotor(ev3.OUTPUT_C)
        self.head = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.lights = ev3.Leds
        assert self.left_paw.connected
        assert self.right_paw.connected

    def bark(self):
        ev3.Sound.speak('bark, bark, woof, woof').wait()

    def walk(self, left_paw_speed, right_paw_speed):
        self.left_paw.run_forever(speed_sp=left_paw_speed)
        self.right_paw.run_forever(speed_sp=right_paw_speed)

    def head_up(self):
        self.head.run_forever(speed_sp=700)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.head.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def head_down(self):
        self.head.run_to_rel_pos(position_sp=-14.2*180)
        self.head.wait_while(ev3.Motor.STATE_RUNNING)

    def shake(self):
        self.head_up()
        self.head_down()
        for k in range(5):
            self.head.run_to_rel_pos(position_sp=360, speed_sp=800)
            self.head.wait_while(ev3.Motor.STATE_RUNNING)
            self.head.run_to_rel_pos(position_sp=-360, speed_sp=800)
            self.head.wait_while(ev3.Motor.STATE_RUNNING)

    def wag_tail(self):
        for k in range(10):
            if k % 2 == 0:
                self.right_paw.run_forever(speed_sp=-600)
                self.left_paw.run_forever(speed_sp=600)
                time.sleep(0.75)
                self.right_paw.stop(stop_action='brake')
                self.left_paw.stop(stop_action='brake')
            else:
                self.right_paw.run_forever(speed_sp=600)
                self.left_paw.run_forever(speed_sp=-600)
                time.sleep(0.75)
                self.right_paw.stop(stop_action='brake')
                self.left_paw.stop(stop_action='brake')

    def stay(self):
        self.left_paw.stop(stop_action='brake')
        self.right_paw.stop(stop_action='brake')
        self.head.stop(stop_action='brake')

    def nap_time(self):
        self.head.stop()
        self.left_paw.stop()
        self.right_paw.stop()
        self.running = False

    # def sniff(self):
    #     self.color_sensor

    # def pet_parade(self):
    #     self.lights.RIGHT()
    #     self.lights.set_color(self.lights.LEFT, list1)

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    # def loop_forever(self):
    #     self.running = True
    #     while self.running:
    #         time.sleep(0.1)
    #
    # def quit_program(mqtt_client, shutdown_ev3):
    #     if shutdown_ev3:
    #         print("shutdown")
    #         mqtt_client.send_message("shutdown")
    #     mqtt_client.close()
    #     exit()

