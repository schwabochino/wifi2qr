# WiFi2QR
# Author: Philipp Schwarberg

# qrcode > https://pypi.org/project/qrcode/
# PIL > pillow https://pypi.org/project/Pillow/


import qrcode
from tkinter import *
from PIL import Image, ImageDraw, ImageFont


def qr_cred(ssid_cred, psw_cred):
    emp_img = Image.new(mode='RGB',
                        color='white',
                        size=(350, 350))

    cred_draw = ImageDraw.Draw(emp_img)
    cred_font = ImageFont.truetype('Arial Unicode.ttf', 16)
    cred_draw.text((10, 20),
                   f'SSID: {ssid_cred} \n'
                   f'Password: {psw_cred}',
                   font=cred_font,
                   fill=(0, 0, 0))

    emp_img.save('qrcode/cred.png')

    img_a = Image.open('qrcode/qr.png')
    img_b = Image.open('qrcode/cred.png')

    final_image = Image.new('RGB', color='white', size=(400, 500))
    final_image.paste(img_a, (0, 0))
    final_image.paste(img_b, (0, 400))

    final_image.show()


# Generate qr code and save it in /qrcode/qr.png
def qr_gen():
    ssid_gen = ssid_input.get()
    psw_gen = psw_input.get()

    input_data = f'WIFI:T:WPA;S:{ssid_gen};P:{psw_gen};;'
    # Creating an instance of qrcode

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)

    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    # Save img with timestamp
    img.save(f'qrcode/qr.png')
    qr_cred(ssid_gen, psw_gen)


# Create a tkinter window
window = Tk()

# Get width and height
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height height / 3 display a little above of the center
position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(window.winfo_screenheight() / 3 - window_height / 2)

window.geometry("+{}+{}".format(position_right, position_down))

# title of Window
window.title("WiFi2QR")

# Generate label and input
ssid_label = Label(window,
                   text='SSID: ')
ssid_input = Entry(window)

psw_label = Label(window,
                  text='Password: ')
psw_input = Entry(window)

ssid_label.grid(row=0, column=0)
ssid_input.grid(row=0, column=1)

psw_label.grid(row=1, column=0)
psw_input.grid(row=1, column=1)

ssid = ssid_input.get()
psw = psw_input.get()

# Generate button the lambda function prevents execution on startup without the button being clicked
button_make = Button(window,
                     text="Make QR",
                     command=lambda: qr_gen())

button_make.grid(row=3, column=1)

window.mainloop()
