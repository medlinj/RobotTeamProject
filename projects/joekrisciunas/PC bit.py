import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import time as time
class Recie(object):
    def __init__(self):
       pass

    def rec(self):
        print('narrator voice:  for you see, on the robots search for purpose, it found out that it was, in fact, a robot, and was forced to confront the fact that everything, even its existential crisis, was preprogrammed')

    def loop_forever(self):
        while True:
            time.sleep(.05)



def main():
    thing = Recie()
    mqtt_client = com.MqttClient(thing)
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

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)

    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<w>', lambda event: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<a>', lambda event: send_left(mqtt_client, left_speed_entry, right_speed_entry))


    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))


    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<d>', lambda event: send_right(mqtt_client, left_speed_entry, right_speed_entry))


    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_back(mqtt_client, right_speed_entry, left_speed_entry)
    root.bind('<s>', lambda event: send_back(mqtt_client, left_speed_entry, right_speed_entry))


    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    purp_button = ttk.Button(main_frame, text='Find Purpose')
    purp_button.grid(row=6,column=1)
    purp_button['command']=(lambda:find_purpose(mqtt_client, True))

    root.mainloop()


def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    l = int(left_speed_entry.get())
    r = int(right_speed_entry.get())

    mqtt_client.send_message("move", [l, r])





def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    l = int(left_speed_entry.get())
    r = int(right_speed_entry.get())

    mqtt_client.send_message("move", [-l, r])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    l = int(left_speed_entry.get())
    r = int(right_speed_entry.get())

    mqtt_client.send_message("move", [l, -r])


def send_back(mqtt_client, left_speed_entry, right_speed_entry):
    l = int(left_speed_entry.get())
    r = int(right_speed_entry.get())

    mqtt_client.send_message("move", [-l, -r])


def send_stop(mqtt_client):

    mqtt_client.send_message("stop")



def send_up(mqtt_client):

    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):

    mqtt_client.send_message("arm_down")



def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:

        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

def find_purpose(mqtt_client, find_purpose):
    if find_purpose:

        mqtt_client.send_message('find_purpose')





main()

