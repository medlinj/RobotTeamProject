import controller
import mqtt_remote_method_calls as com

def main():
    robot = controller.RobotDelegate()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

main()

