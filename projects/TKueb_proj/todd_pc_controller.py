

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class PcAction(object):

    def __init__(self):
        self.status_label = 'Waiting on response from robot. No connection made.'

    def change_status(self, status):
        message_to_display = status
        self.status_label.configure(text=message_to_display)


def main():
    pc = PcAction
    mqtt_client = com.MqttClient(pc)
    mqtt_client.connect_to_pc()




    #creating mqtt object adn connecting the object to ev3
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    #Creating the window
    window = tkinter.Tk()
    window.title("Soda Robot")

    #Establishin the type of window
    main_frame = ttk.Frame(window, padding=20, relief='raised')
    main_frame.grid()

    #creating lables for the entry boxes
    color_title = ttk.Label(main_frame, text="Color")
    color_title.grid(row=0, column=0)
    location_title = ttk.Label(main_frame, text="Location")
    location_title.grid(row=0, column=1)

    green_label = ttk.Label(main_frame, text="Green:")
    green_label.grid(row=1, column=0)

    blue_label = ttk.Label(main_frame, text="Blue:")
    blue_label.grid(row=2, column=0)

    red_label = ttk.Label(main_frame, text="Red:")
    red_label.grid(row=3, column=0)

    orange_label = ttk.Label(main_frame, text="Orange:")
    orange_label.grid(row=4, column=0)

    soda_label = ttk.Label(main_frame, text="Soda Type: ")
    soda_label.grid(row=1, column=2)

    soda_entry = ttk.Entry(main_frame, width=16)
    soda_entry.insert(0, "")
    soda_entry.grid(row=1, column=3)

    soda_set = ttk.Button(main_frame, text="Set soda")
    soda_set.grid(row=1, column=4)
    soda_set['command'] = lambda: send_soda(mqtt_client, soda_entry.get())

    # DONE add button callback

    status_label = ttk.Label(main_frame, text="Current Status: ")
    status_label.grid(row=2, column=2)

    #creating entry boxes
    green_entry = ttk.Entry(main_frame, width=16)
    green_entry.insert(0, "")
    green_entry.grid(row=1, column=1)

    blue_entry = ttk.Entry(main_frame, width=16)
    blue_entry.insert(0, "")
    blue_entry.grid(row=2, column=1)

    red_entry = ttk.Entry(main_frame, width=16)
    red_entry.insert(0,"")
    red_entry.grid(row=3, column=1)

    orange_entry = ttk.Entry(main_frame, width=16)
    orange_entry.insert(0, "")
    orange_entry.grid(row=4,column=1)

    #Creating variable status label TODO: FIGURE OUT HOW TO CHANGE LABEL
    pc_action_obj = PcAction()
    label_text = pc_action_obj.status_label
    display_status = ttk.Label(main_frame, text = label_text)
    display_status.grid(row=2, column=3)

    #Start stop buttons
    start_button = ttk.Button(main_frame, text="Start")
    start_button.grid(row=6, column=1)
    start_button['command'] = lambda: start(mqtt_client)
    # TODO: add the button callback

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=6, column=2)
    quit_button['command'] = lambda: quit(mqtt_client, True)
    # DONE: add the button callback

    window.mainloop()

    # DONE: start and stop callback function

def send_soda(mqtt_client, soda_type):
    mqtt_client.send_message("soda_request", [soda_type])

def start(mqtt_client):
    mqtt_client.send_message("start_fetch")

def quit(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()





main()
