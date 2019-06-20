import board
import digitalio
from micropython import const
import displayio
from adafruit_cursorcontrol import Cursor
from gamepadshift import GamePadShift

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

# Create the display
display = board.DISPLAY

# Create the display context
splash = displayio.Group(max_size=22)

# initialize the mouse cursor object
mouse_cursor = Cursor(display, display_group=splash)

# show displayio group
display.show(splash)

def check_dpad(d_pad_buttons):
    """Checks the directional pad for button presses."""
    if d_pad_buttons & BUTTON_RIGHT:
        mouse_cursor.x += mouse_cursor.speed
    elif d_pad_buttons & BUTTON_LEFT:
        mouse_cursor.x -= mouse_cursor.speed
    if d_pad_buttons & BUTTON_DOWN:
        mouse_cursor.y += mouse_cursor.speed
    elif d_pad_buttons & BUTTON_UP:
        mouse_cursor.y -= mouse_cursor.speed

is_pressed = False
while True:
    display.wait_for_frame()
    pressed = pad.get_pressed()
    check_dpad(pressed)
    if is_pressed:
        if not pressed & (BUTTON_A | BUTTON_B):
            is_pressed = False
        continue
    if pressed & BUTTON_A:
        is_pressed = True
        if mouse_cursor.hide:
            mouse_cursor.hide = False
        else:
            mouse_cursor.hide = True
