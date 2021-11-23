import tkinter

import qrcode
from tkinter import *
from PIL import Image, ImageDraw, ImageFont


def qr_cred(ssid_cred, psw_cred):
    emp_img = Image.new(mode='RGB', color='white',
                        size=(350, 350))

    cred_draw = ImageDraw.Draw(emp_img)
    cred_font = ImageFont.truetype('Arial Unicode.ttf', 16)
    cred_draw.text((10, 20), f'SSID: {ssid_cred} \nPasswort: {psw_cred}', font=cred_font, fill=(0, 0, 0))

    #emp_img.show()
    emp_img.save('qrcode/cred.png')

    bilda = Image.open('qrcode/qr.png')
    bildb = Image.open('qrcode/cred.png')

    final_image = Image.new('RGB', color='white', size=(350,500))
    final_image.paste(bilda,(0,0))
    final_image.paste(bildb,(0,350))

    final_image.show()


def qr_gen():
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
    img.save(f'qrcode/qr.png')
    qr_cred(ssid, psw)
    # qr_show()


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
