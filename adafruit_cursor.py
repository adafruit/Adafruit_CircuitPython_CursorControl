# The MIT License (MIT)
#
# Copyright (c) 2019 Brent Rubell for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_cursor`
================================================================================

Simulated mouse cursor for display interaction

* Author(s): Brent Rubell

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""
import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Cursor.git"

class Cursor:
    """Mouse cursor-like interaction for CircuitPython.

    :param displayio.Display: CircuitPython display object.
    :param displayio.Group: CircuitPython group object to append the cursor to.
    :param int cursor_speed: Speed of the cursor, in pixels.
    ;param int scale: Scale amount for the cursor in both directions.
    :param bool is_hidden: Cursor is hidden on init.
    """
    def __init__(self, display=None, display_group=None, is_hidden=False, cursor_speed=5, scale=1):
        self._display = display
        self._scale = scale
        self._display_grp = display_group
        self._disp_x = display.height
        self._disp_y = display.width
        self._disp_sz = self._disp_x - 1, self._disp_y - 1
        self._speed = cursor_speed
        self._is_hidden = is_hidden
        self.generate_cursor()

    @property
    def scale(self):
        """Returns the cursor's scale amount as an integer."""
        return self._scale

    @scale.setter
    def scale(self, scale_value):
        """Scales the cursor by scale_value in both directions.
        :param int scale_value: Amount to scale the cursor by.
        """
        if scale_value > 0:
            self._scale = scale_value
            self._cursor_grp.scale = scale_value

    @property
    def speed(self):
        """Returns the cursor's speed, in pixels."""
        return self._speed

    @speed.setter
    def speed(self, speed):
        """Sets the speed of the cursor.
        :param int speed: Cursor movement speed, in pixels.
        """
        self._speed = speed

    @property
    def x(self):
        """Returns the cursor's x-coordinate."""
        return self._cursor_grp.x

    @x.setter
    def x(self, x_val):
        """Sets the x-value of the cursor.
        :param int x_val: x position, in pixels.
        """
        if x_val < 0 and not self._is_hidden:
            self._cursor_grp.x = self._cursor_grp.x
        elif x_val > self._disp_sz[1] and not self._is_hidden:
            self._cursor_grp.x = self._cursor_grp.x
        elif not self._is_hidden:
            self._cursor_grp.x = x_val

    @property
    def y(self):
        """Returns the cursor's y-coordinate."""
        return self._cursor_grp.y

    @y.setter
    def y(self, y_val):
        """Sets the y-value of the cursor.
        :param int y_val: y position, in pixels.
        """
        if y_val < 0 and not self._is_hidden:
            self._cursor_grp.y = self._cursor_grp.y
        elif y_val > self._disp_sz[0] and not self._is_hidden:
            self._cursor_grp.y = self._cursor_grp.y
        elif not self._is_hidden:
            self._cursor_grp.y = y_val

    @property
    def is_hidden(self):
        """Returns if the cursor is hidden or visible on the display."""
        return self._is_hidden

    @property
    def hide(self):
        """Returns if the cursor is hidden or visible on the display."""
        return self._is_hidden
    
    @hide.setter
    def hide(self, is_hidden):
        if is_hidden:
            self._is_hidden = True
            self._display_grp.remove(self._cursor_grp)
        else:
            self._is_hidden = False
            self._display_grp.append(self._cursor_grp)

    def generate_cursor(self):
        """Generates a cursor icon bitmap"""
        self._cursor_grp = displayio.Group(max_size=1, scale=self._scale)
        self._pointer_bitmap = displayio.Bitmap(20, 20, 3)
        self._pointer_palette = displayio.Palette(3)
        self._pointer_palette.make_transparent(0)
        self._pointer_palette[1] = 0xFFFFFF
        self._pointer_palette[2] = 0x0000
        # left edge, outline
        for i in range(0, self._pointer_bitmap.height):
            self._pointer_bitmap[0, i] = 2
        # inside fill
        for j in range(1, 15):
            for i in range(j+1, self._pointer_bitmap.height - j):
                self._pointer_bitmap[j, i] = 1
        # right diag., outline
        for i in range(1, 15):
            self._pointer_bitmap[i, i] = 2
        # bottom diag., outline
        for i in range(1, 5):
            self._pointer_bitmap[i, self._pointer_bitmap.height-i] = 2
        # bottom flat line, outline
        for i in range(5, 15):
            self._pointer_bitmap[i, 15] = 2
        # right side fill
        for i in range(5, 15):
            self._pointer_bitmap[i-1, 14] = 1
            self._pointer_bitmap[i-2, 13] = 1
            self._pointer_bitmap[i-3, 12] = 1
            self._pointer_bitmap[i-4, 11] = 1
        # create a tilegrid out of the bitmap and palette
        self._pointer_sprite = displayio.TileGrid(self._pointer_bitmap, pixel_shader=self._pointer_palette)
        self._cursor_grp.append(self._pointer_sprite)
        self._display_grp.append(self._cursor_grp)
