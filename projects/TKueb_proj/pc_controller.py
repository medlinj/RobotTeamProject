

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class PcAction(object):
    def __init__(self):
        self.status = 'No status / Waiting response from robot'


def main():

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

    #Creating variable status label FIGURE OUT HOW TO CHANGE LABEL
    text_var = PcAction.status
    display_status = ttk.Label(main_frame, text = text_var)
    display_status.grid(row=2, column=3)



    window.mainloop()

main()
