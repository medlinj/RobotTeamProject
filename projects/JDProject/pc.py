import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)


    forward_button = ttk.Button(main_frame, text="Walk")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_walk(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<w>', lambda event: send_walk(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text='Stay')
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stay(mqtt_client)
    root.bind('<space>', lambda event: stay(mqtt_client))

    root.mainloop()


def send_walk(mqtt_client, left_speed_entry, right_speed_entry):
    l = int(left_speed_entry.get())
    r = int(right_speed_entry.get())
    print('time for a walk!')
    mqtt_client.send_message('walk', [l, r])

def stay(mqtt_client):
    print('stay!')
    mqtt_client.send_message('stay')

main()

