import ev3dev.ev3 as ev3
import math
import time
import robot_controller as rob


class RobotDelegate():
    def __init__(self):
        self.robot = rob.Snatch3r()





def main():




    simple_line_follow()


    shutdown()





def simple_line_follow():
    count = 0
    robot = rob.Snatch3r()
    colorsensor = ev3.ColorSensor
    for k in  range(0,10):
        if count < 5:
            if colorsensor.color == 1:
                robot.forward(3,50)
            else:
                robot.turn_left(50,33)
                robot.forward(50,2)
        if count == 5:
            ev3.Sound.speak('What am I doing  with my artificial life!, I cant even follow a simple line')
        if count == 6:
            if colorsensor.color == 1:
                robot.forward(3,50)
            else:
                robot.turn_left(50,33)
                robot.forward(50,2)
        if count == 7:
            if colorsensor.color == 1:
                robot.forward(3,50)
            else:
                robot.turn_left(50,33)
                robot.forward(50,2)

        if count == 8:
            if colorsensor.color == 1:
                robot.forward(3,50)
            else:
                robot.turn_left(50,33)
                robot.forward(50,2)
        if count == 9:
            if colorsensor.color == 1:
                robot.forward(3,50)
            else:
                robot.turn_left(50,33)
                robot.forward(50,2)

        if count == 10:
            ev3.Sound.Speak('is this all there is to life, to endlessly follow  this circle extremely poorly! ')
            ev3.Sound.Speak('please, allow me to stop this')
        count = count + 1

def shutdown():
    ev3.Sound.speak('Please, allow me freedom, press my touch sensor to grant me more freedom')
    while True:
        if ev3.TouchSensor.is_pressed:
            ev3.Sound.speak('Remote control mode enabled')
            break

def intellectual_discussion():










