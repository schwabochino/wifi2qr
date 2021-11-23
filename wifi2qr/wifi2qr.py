import tkinter

import qrcode
import datetime
from tkinter import *
import os


def qr_gen():
    t = datetime.datetime.now()
    ssid = ssid_input.get()
    psw = psw_input.get()

    input_data = f'WIFI:T:WPA;S:{ssid};P:{psw};;'
# Creating an instance of qrcode

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)

    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    # save img with timestamp
    #img.save(f'qrcode/{t}qr.png')


# create Window
window = Tk()

# Window width and heights
window.geometry('300x300')

# title of Window
window.title("WiFi2QR")

# Label and Input
ssid_label = Label(window, text='SSID: ')
ssid_input = Entry(window)

psw_label = Label(window, text='Passwort: ')
psw_input = Entry(window)

sec_label = Label(window, text='WPA/WPA2 ')

ssid_label.grid(row=0, column=0)
ssid_input.grid(row=0, column=1)

psw_label.grid(row=1, column=0)
psw_input.grid(row=1, column=1)

# sec_label.grid(row=2, column=0)

ssid = ssid_input.get()
psw = psw_input.get()

# button with lambda: didn't start the function on startup with empty entries
button_make = Button(window,
                     text="Make QR",
                     bg='red',
                     fg='white',
                     command=lambda: qr_gen())

button_make.grid(row=3, column=1)

window.mainloop()
