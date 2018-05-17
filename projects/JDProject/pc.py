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

    color_label = ttk.Label(main_frame, text="Color Code")
    color_label.grid(row=0, column=1)
    color_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    color_entry.insert(0, "600")
    color_entry.grid(row=1, column=2)

    # Buttons below

    forward_button = ttk.Button(main_frame, text="Walk")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_walk(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<w>', lambda event: send_walk(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text='Stay')
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stay(mqtt_client)
    root.bind('<space>', lambda event: stay(mqtt_client))

    wag_button = ttk.Button(main_frame, text='Wag Tail!')
    wag_button.grid(row=6, column=0)
    wag_button['command'] = lambda: wag_tail(mqtt_client)
    root.bind('<e>', lambda event: wag_tail(mqtt_client))

    shake_button = ttk.Button(main_frame, text='Shake Hand!')
    shake_button.grid(row=5, column=0)
    shake_button['command'] = lambda: shake(mqtt_client)
    root.bind('<q>', lambda event: shake(mqtt_client))

    quit_button = ttk.Button(main_frame, text='Nap (Quit)')
    quit_button.grid(row=6, column= 2)
    quit_button['command'] = lambda: nap_time(mqtt_client)
    root.bind('<p>', lambda event: nap_time(mqtt_client))

    bark_button = ttk.Button(main_frame, text='Bark')
    bark_button.grid(row=4, column=0)
    bark_button['command'] = lambda: bark(mqtt_client)
    root.bind('<e>', lambda event: bark(mqtt_client))

    test_button = ttk.Button(main_frame, text='cam')
    test_button.grid(row=4, column=1)
    test_button['command'] = lambda: testing(mqtt_client)
    root.bind('<t>', lambda event: testing(mqtt_client))

    colors_button = ttk.Button(main_frame, text='sniff')
    colors_button.grid(row=6, column=1)
    colors_button['command'] = lambda: sniff(mqtt_client)
    root.bind('<u>', lambda event: sniff(mqtt_client))

    parade_button = ttk.Button(main_frame, text='light parade')
    parade_button.grid(row=5, column=2)
    parade_button['command'] = lambda: pet_parade(mqtt_client)
    root.bind('<l>', lambda event: pet_parade(mqtt_client))

    root.mainloop()

#     Functions below


def send_walk(mqtt_client, left_speed_entry, right_speed_entry):
    l = int(left_speed_entry.get())
    r = int(right_speed_entry.get())
    print('time for a walk!')
    mqtt_client.send_message('walk', [l, r])


def stay(mqtt_client):
    print('stay!')
    mqtt_client.send_message('stay')


def wag_tail(mqtt_client):
    print('happy doggy!!!')
    mqtt_client.send_message('wag_tail')


def shake(mqtt_client):
    print('shake')
    mqtt_client.send_message('shake')


def bark(mqtt_client):
    print('bark, bark, woof, woof')
    mqtt_client.send_message('bark')


def nap_time(mqtt_client):
    print('nap time!')
    mqtt_client.send_message('nap_time')
    mqtt_client.close()
    exit()


def testing(mqtt_client):
    print('testing')
    mqtt_client.send_message('testing')


def sniff(mqtt_client):
    print('sniff')
    mqtt_client.send_message('sniff')


def pet_parade(mqtt_client):
    print('light show!')
    mqtt_client.send_message('pet_parade')


main()
