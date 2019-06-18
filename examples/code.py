# using adafruit_cursor with adafruit_button
import time
import board
from micropython import const
import digitalio
from gamepadshift import GamePadShift
from adafruit_bitmap_font import bitmap_font
from adafruit_button import Button
import displayio
import adafruit_cursor

import busio
import adafruit_lis3dh

# PyBadge Button Masks
BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_A = const(2)
BUTTON_B = const(1)

# Initialize PyBadge Gamepad
pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

# Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
# otherwise check I2C pins.
if hasattr(board, 'ACCELEROMETER_SCL'):
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)
else:
    i2c = busio.I2C(board.SCL, board.SDA)
    int1 = digitalio.DigitalInOut(board.D9)  # Set this to the correct pin for the interrupt!
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
lis3dh.range = adafruit_lis3dh.RANGE_8_G
lis3dh.set_tap(1, 60)

# Create the display
display = board.DISPLAY
splash_grp = displayio.Group(max_size=20)

# Make the display context
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

##########################################################################
# Make a background color fill
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x404040
bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash_grp.append(bg_sprite)
##########################################################################

# Load the font
THE_FONT = "/fonts/Arial-12.bdf"
font = bitmap_font.load_font(THE_FONT)

buttons = []
button_0 = Button(x=BUTTON_MARGIN, y=BUTTON_MARGIN,
                  width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                  label="click me!", label_font=font)
buttons.append(button_0)

button_2 = Button(x=BUTTON_MARGIN*3+2*BUTTON_WIDTH, y=BUTTON_MARGIN,
                  width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                  label="or me!", label_font=font, label_color=0x0000FF,
                  fill_color=0x00FF00, outline_color=0xFF0000)
buttons.append(button_2)

for b in buttons:
    splash_grp.append(b.group)

# create the display object
display = board.DISPLAY

# initialize the mouse cursor object
# cursor style (plus, triangle, pointer, rectangle)
mouse_cursor = adafruit_cursor.Cursor(display, display_group=splash_grp)

# show displayio group
display.show(splash_grp)

def check_dpad(pad_btns):
    """Checks the d-pad presses"""
    if (pad_btns & BUTTON_RIGHT) > 0:
        mouse_cursor.x += mouse_cursor.speed
    elif (pad_btns & BUTTON_LEFT) > 0:
        mouse_cursor.x -= mouse_cursor.speed
    elif (pad_btns & BUTTON_UP) > 0:
        mouse_cursor.y -= mouse_cursor.speed
    elif (pad_btns & BUTTON_DOWN) > 0:
        mouse_cursor.y += mouse_cursor.speed

def check_btns(pad_btns):
    """Checks a/b button presses"""
    global is_a_clicked
    if (pad_btns & BUTTON_B) > 0:
        if mouse_cursor.hide:
            mouse_cursor.hide = False 
        else:
            mouse_cursor.hide = True
    elif ((pad_btns & BUTTON_A) > 0) and not mouse_cursor.hide:
        is_a_clicked = True

is_a_clicked = False
current_btns = pad.get_pressed()
while True:
    if lis3dh.tapped:
      print('tapped!')
      mouse_cursor.scale = 2
      time.sleep(0.5)
      mouse_cursor.scale = 1
    btns = pad.get_pressed()
    check_dpad(btns)
    if current_btns != btns:
        check_btns(btns)
        current_btns = btns
    # check the coordinates of the cursor
    p = mouse_cursor.x, mouse_cursor.y
    if p:
        for i, b in enumerate(buttons):
            if b.contains(p) and is_a_clicked:
                print("Button %d pressed"%i)
                b.selected = True
                is_a_clicked = False
            else:
                b.selected = False
    time.sleep(0.01)