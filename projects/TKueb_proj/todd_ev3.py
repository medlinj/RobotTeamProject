import mqtt_remote_method_calls as com
import todd_robot_controller as robo


def main():
    robot = robo.Snatch3r()
    receiving_delegate = com.MqttClient(robot)
    receiving_delegate.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
