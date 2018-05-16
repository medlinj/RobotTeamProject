import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

class RobotDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.left_paw = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_paw = ev3.LargeMotor(ev3.OUTPUT_C)
        self.head = ev3.MediumMotor(ev3.OUTPUT_A)

    def bark(self):
        ev3.Sound.speak('woof, woof. bark, bark').wait()

    def walk(self, left_paw_speed, right_paw_speed):
        self.left_paw.run_forever(speed_sp=left_paw_speed)
        self.right_paw.run_forever(speed_sp=right_paw_speed)

    def shake_hand(self):
        self.head.run_to_rel_pos()
        for k in range(5):
            self.head.run_to_rel_pos()

    def wag_tail(self):
        for k in range(10):
            if k % 2 == 0:
                self.right_paw.run_forever(speed_sp=-600)
                self.left_paw.run_forever(speed_sp=600)
                time.sleep(0.75)
            else:
                self.right_paw.run_forever(speed_sp=600)
                self.left_paw.run_forever(speed_sp=-600)
                time.sleep(0.75)

    def stay(self):
        self.left_paw.stop(stop_action='brake')
        self.right_paw.stop(stop_action='brake')
        self.head.stop(stop_action='brake')




    # def arm_up(self):
    #     self.arm.run_forever(speed_sp=700)
    #     while not self.touch_sensor.is_pressed:
    #         time.sleep(0.01)
    #     self.arm.stop(stop_action='brake')
    #     ev3.Sound.beep().wait()
    #
    # def arm_down(self):
    #     self.arm.run_to_rel_pos(position_sp=-14.2*360)
    #     self.arm.wait_while(ev3.Motor.STATE_RUNNING)
    #
    # def loop_forever(self):
    #     self.running = True
    #     while self.running:
    #         time.sleep(0.1)
    #
    # def shutdown(self):
    #     self.arm.stop()
    #     self.left_motor.stop()
    #     self.right_motor.stop()
    #     self.running = False
    #
    # def quit_program(mqtt_client, shutdown_ev3):
    #     if shutdown_ev3:
    #         print("shutdown")
    #         mqtt_client.send_message("shutdown")
    #     mqtt_client.close()
    #     exit()