

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import pc_delegate_helper


def main():
    pc = pc_delegate_helper.PcAction()
    pc_delegate = com.MqttClient(pc)
    pc_delegate.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    #pc.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.
    #creating mqtt object adn connecting the object to ev3

    mqtt_to_ev3 = com.MqttClient()
    mqtt_to_ev3.connect_to_ev3()

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
    soda_set['command'] = lambda: send_soda(mqtt_to_ev3, soda_entry.get())

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

    label_text = pc.status_code
    display_status = ttk.Label(main_frame, text = label_text)
    display_status.grid(row=2, column=3)

    #Start stop buttons
    start_button = ttk.Button(main_frame, text="Start")
    start_button.grid(row=6, column=1)
    start_button['command'] = lambda: start(mqtt_to_ev3)
    # TODO: add the button callback

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=6, column=2)
    quit_button['command'] = lambda: quit(mqtt_to_ev3, True)
    # DONE: add the button callback

    window.mainloop()
    pc_action_obj.loop_forever()


    # DONE: start and stop callback function

def send_soda(which_mqtt, soda_type):
    which_mqtt.send_message("soda_request", [soda_type])

def start(which_mqtt):
    which_mqtt.send_message("start_fetch")

def quit(which_mqtt, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        which_mqtt.send_message("shutdown")
    which_mqtt.close()
    exit()





main()
