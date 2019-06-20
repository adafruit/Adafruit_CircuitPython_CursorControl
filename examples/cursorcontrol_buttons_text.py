import board
from micropython import const
import digitalio
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_button import Button
from adafruit_cursorcontrol import Cursor
from adafruit_display_text import label
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

# Load the font
THE_FONT = "/fonts/Arial-12.bdf"
font = bitmap_font.load_font(THE_FONT)

# Create the display
display = board.DISPLAY

# Create the display context
splash = displayio.Group(max_size=22)

##########################################################################
# Make a background color fill

color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x404040
bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

##########################################################################

# Set up button size info
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

# Create the buttons
buttons = []

button_speed_inc = Button(x=BUTTON_MARGIN, y=BUTTON_MARGIN+BUTTON_HEIGHT,
                          width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                          label="+ Speed", label_font=font)
buttons.append(button_speed_inc)

button_speed_dec = Button(x=BUTTON_MARGIN, y=BUTTON_MARGIN*4+BUTTON_HEIGHT,
                          width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                          label="- Speed", label_font=font)
buttons.append(button_speed_dec)

button_scale_pos = Button(x=BUTTON_MARGIN*3+2*BUTTON_WIDTH, y=BUTTON_MARGIN+BUTTON_HEIGHT,
                          width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                          label="+ Scale", label_font=font, style=Button.SHADOWRECT)
buttons.append(button_scale_pos)

button_scale_neg = Button(x=BUTTON_MARGIN*3+2*BUTTON_WIDTH, y=BUTTON_MARGIN*4+BUTTON_HEIGHT,
                          width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                          label="- Scale", label_font=font, style=Button.SHADOWRECT)
buttons.append(button_scale_neg)

# Show the button
for b in buttons:
    splash.append(b.group)

# Create a text label
text_label = label.Label(font, text="CircuitPython Cursor!", color=0x00FF00,
                         x = 100, y = 20)
splash.append(text_label)

text_speed = label.Label(font, max_glyphs = 15, color=0x00FF00,
                         x = 120, y = 40)
splash.append(text_speed)

text_scale = label.Label(font, max_glyphs = 15, color=0x00FF00,
                         x = 120, y = 60)
splash.append(text_scale)

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
    text_speed.text = 'Speed: {0}px'.format(mouse_cursor.speed)
    text_scale.text = 'Scale: {0}px'.format(mouse_cursor.scale)
    pressed = pad.get_pressed()
    check_dpad(pressed)
    if is_pressed:
        if not pressed & (BUTTON_A | BUTTON_B):
            # buttons de-pressed
            is_pressed = False
            for i, b in enumerate(buttons):
                b.selected=False
        # otherwise, continue holding
        continue
    if pressed & BUTTON_B:
        is_pressed = True
        if mouse_cursor.hide:
            mouse_cursor.hide = False
        else:
            mouse_cursor.hide = True
    if pressed & BUTTON_A:
        is_pressed = True
        for i, b in enumerate(buttons):
            if b.contains((mouse_cursor.x, mouse_cursor.y)):
                print("Button %d pressed"%i)
                if i == 0: # Increase the cursor speed
                    mouse_cursor.speed += 1
                elif i == 1: # Decrease the cursor speed
                    mouse_cursor.speed -= 1
                if i == 2: # Increase the cursor scale
                    mouse_cursor.scale += 1
                elif i == 3: # Decrease the cursor scale
                    mouse_cursor.scale -= 1
                b.selected=True
