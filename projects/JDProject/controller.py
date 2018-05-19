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
        self.mqtt = None

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
        self.head.run_to_rel_pos(position_sp=-14.2*180+30)
        self.head.wait_while(ev3.Motor.STATE_RUNNING)

    def shake(self):
        self.head_up()
        self.head_down()
        for k in range(5):
            self.head.run_to_rel_pos(position_sp=360, speed_sp=800)
            self.head.wait_while(ev3.Motor.STATE_RUNNING)
            self.head.run_to_rel_pos(position_sp=-360, speed_sp=800)
            self.head.wait_while(ev3.Motor.STATE_RUNNING)
        self.head_down()

    def wag_tail(self):
        for k in range(10):
            if k % 2 == 0:
                self.right_paw.run_forever(speed_sp=-800)
                self.left_paw.run_forever(speed_sp=800)
                time.sleep(0.15)
                self.right_paw.stop(stop_action='brake')
                self.left_paw.stop(stop_action='brake')
            else:
                self.right_paw.run_forever(speed_sp=800)
                self.left_paw.run_forever(speed_sp=-800)
                time.sleep(0.15)
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

    def sniff(self):
        self.walk(400, 400)
        while True:
            current_color = self.color_sensor.color
            if current_color == 1:
                self.mqtt.send_message('black')
                break
            if current_color == 5:
                self.mqtt.send_message('red')
                break
            if current_color == 2:
                self.mqtt.send_message('blue')
                break
            else:
                print('no smell')
            time.sleep(0.5)
        self.stay()
        time.sleep(0.5)
        self.wag_tail()


    def pet_parade(self):
        list1 = [ev3.Leds.GREEN, ev3.Leds.RED, ev3.Leds.YELLOW, ev3.Leds.GREEN, ev3.Leds.AMBER, ev3.Leds.BLACK, ev3.Leds.ORANGE]
        for j in range(4):
            for k in range(len(list1)):
                ev3.Leds.set_color(ev3.Leds.LEFT, list1[k])
                ev3.Leds.set_color(ev3.Leds.RIGHT, list1[k])
                time.sleep(0.4)

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

    def color_sensor_color(self):
        """ Example of detecting color with the color sensor. """

        # Potential values of the color_sensor.color property
        #   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
        #   ev3.ColorSensor.COLOR_BLACK   is the value 1
        #   ev3.ColorSensor.COLOR_BLUE    is the value 2
        #   ev3.ColorSensor.COLOR_GREEN   is the value 3
        #   ev3.ColorSensor.COLOR_YELLOW  is the value 4
        #   ev3.ColorSensor.COLOR_RED     is the value 5
        #   ev3.ColorSensor.COLOR_WHITE   is the value 6
        #   ev3.ColorSensor.COLOR_BROWN   is the value 7
        # From http://python-ev3dev.readthedocs.io/en/latest/sensors.html#special-sensor-classes

        for _ in range(20):
            current_color = self.color_sensor.color
            if current_color == 5:
                ev3.Sound.speak("I see Red").wait()
            else:
                print('no red')
            time.sleep(1.0)

    def testing(self):
        pixy = ev3.Sensor(driver_name="pixy-lego")
        # pixy.mode = "SIG1"
        while True:
            print("(X, Y)=({}, {}) Width={} Height={}".format(
                pixy.value(1), pixy.value(2), pixy.value(3),
                pixy.value(4)))
            time.sleep(1.0)
            if pixy.value(2) <= 100:
                self.left_paw.run_to_rel_pos(position_sp=90, speed_sp=200)
                time.sleep(1)
            if pixy.value(2) >= 150:
                self.right_paw.run_to_rel_pos(position_sp=90, speed=200)
                time.sleep(1)


