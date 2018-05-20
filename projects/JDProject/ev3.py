import mqtt_remote_method_calls as com
import controller
import pcdelegate
import ev3dev as ev3

def main():
    robot = controller.RobotDelegate()
    mqtt_client = com.MqttClient(robot)
    robot.mqtt = mqtt_client
    mqtt_client.connect_to_pc()
    robot.loop_forever()


# def sendpc(mqtt_client):
#     mqtt_client.send_message('send_to_pc')


main()

