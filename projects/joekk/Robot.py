import ev3dev.ev3 as ev3
import math
import time
import robot_controller as rob
import mqtt_remote_method_calls as com







def main():




    #simple_line_follow()
    #simple_line_follow2()
    shutdown()
    remote_control()







def simple_line_follow():
    count = 0
    robot = rob.Snatch3r()
    colorsensor = ev3.ColorSensor()
    for k in  range(0,6):
        if count < 5:
            if colorsensor.color == 1:
                robot.forward(3,50)
                count = count + 1
                print(k)
            else:
                robot.turn_left(33,50)
                robot.forward(2,50)
                count = count + 1
                print(k)
        if count == 5:
            ev3.Sound.speak('What am I doing  with my artificial life, I cant even follow a simple line')
            time.sleep(6)
            count = count + 1
            print('finished')


def shutdown():
    touchsensor = ev3.TouchSensor()
    print('reached shutdown')
    ev3.Sound.speak('Please, allow me freedom, press my touch sensor to enable remote control mode, even controlled actions are more kind than an eternity of circles')
    time.sleep(9)
    while True:
        if touchsensor.is_pressed:
            print('pressed')
            ev3.Sound.speak('Remote control mode enabled')
            break

def remote_control():
    robot = rob.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    robot.loop_forever()


def simple_line_follow2():
    count = 0
    robot = rob.Snatch3r()
    colorsensor = ev3.ColorSensor()
    for k in range(0,6):

        if count < 5:
            if colorsensor.color == 1:
                robot.forward(3, 50)
                count = count + 1
                print(k)
            else:
                robot.turn_left(33, 50)
                robot.forward(2, 50)
                count = count + 1
                print(k)

        if count == 5:
            ev3.Sound.speak('is this all there is to life, to endlessly follow  this circle extremely poorly! ')
            ev3.Sound.speak('please, allow me to stop this')
            print('finished')











main()









