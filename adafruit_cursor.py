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
    :param dict custom_cursor: Information about the cursor including its cursor_path,
      cursor_scale, cursor_width, cursor_height, cursor_tile_width, and cursor_tile_height.
    :param bool is_hidden: Cursor hidden by default.
    """
    def __init__(self, display=None, display_group=None, cursor_speed=1, is_hidden=False,
                    cursor_style="cursor", scale=1):
        self._display = display
        self._scale = scale
        self._display_grp = display_group
        self._display_width = display.width
        self._display_height = display.height
        self._speed = cursor_speed
        self._is_hidden = is_hidden
        self._cursor_style = cursor_style
        self.generate_cursor()


    @property
    def scale(self):
        """Returns the cursor's bitmap scale"""
        return self._scale

    @scale.setter
    def scale(self, scale_value):
        """Scales the cursor by scale_value in x and y directions
        :param int scale_value: Amount to scale the cursor by.
        """
        self._scale = scale_value
        self._cursor_grp.scale = scale_value

    @property
    def speed(self):
        """Returns the cursor's speed."""
        return self._speed

    @speed.setter
    def speed(self, speed):
        """Sets the speed of the cursor.
        :param int speed: Cursor movement speed.
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
        if self._cursor_grp.x - self._speed < 0:
            self._cursor_grp.x = self._cursor_grp.x + 1
        elif self._cursor_grp.x + self._speed > self._display_width - 25:
            self._cursor_grp.x = self._cursor_grp.x - 1
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
        if self._cursor_grp.y - self._speed < 0:
            self._cursor_grp.y = self._cursor_grp.y + 1
        elif self._cursor_grp.y + self._speed > self._display_height - 25:
            self._cursor_grp.y = self._cursor_grp.y - 1
        elif not self._is_hidden:
            self._cursor_grp.y = y_val

    @property
    def is_hidden(self):
        """Returns if the cursor is hidden or visible on the display."""
        return self._is_hidden

    def hide(self):
        """Hides the cursor by removing the cursor subgroup from the display group.
        """
        self._is_hidden = True
        self._display_grp.remove(self._cursor_grp)

    def show(self):
        """Shows the cursor by appending the cursor subgroup into the display group.
        """
        self._is_hidden = False
        self._display_grp.append(self._cursor_grp)

    def generate_cursor(self):
        """Generates a cursor bitmap"""
        self._cursor_grp = displayio.Group(max_size=1, scale=self._scale)
        self._pointer_bitmap = displayio.Bitmap(20, 20, 3)
        self._pointer_palette = displayio.Palette(3)
        self._pointer_palette.make_transparent(0)
        self._pointer_palette[1] = 0xFFFFFF
        self._pointer_palette[2] = 0x0000
        # cursor bitmap generation
        if self._cursor_style is "plus":
            for i in range(0, self._pointer_bitmap.width, 2):
                self._pointer_bitmap[i, 10] = 1
            for j in range(0, self._pointer_bitmap.height, 2):
                self._pointer_bitmap[10, j] = 1
        elif self._cursor_style is "rectangle":
            for i in range(0, self._pointer_bitmap.height-1):
                for j in range(0, self._pointer_bitmap.width-1):
                    self._pointer_bitmap[i, j] = 1
        else: # cursor_style defaults to default cursor
            # left edge
            for i in range(0, self._pointer_bitmap.height):
                self._pointer_bitmap[0, i] = 2
            #for i in range(1, self._pointer_bitmap.height - 1):
            #    self._pointer_bitmap[1, i] = 1

            for j in range(1, 15):
                for i in range(j+1, self._pointer_bitmap.height - j):
                    self._pointer_bitmap[j, i] = 1
            # right diag.
            for i in range(1, 15):
                self._pointer_bitmap[i, i] = 2
                #self._pointer_bitmap[i, i-1] = 1
            # bottom diag
            for i in range(1, 5):
                self._pointer_bitmap[i, self._pointer_bitmap.height-i] = 2
                #self._pointer_bitmap[i, self._pointer_bitmap.height-i-1] = 1
            # bottom flat line
            for i in range(5, 15):
                self._pointer_bitmap[i, 15] = 2
                #self._pointer_bitmap[i-1, 14] = 1
        # create a tilegrid out of the bitmap and palette
        self._pointer_sprite = displayio.TileGrid(self._pointer_bitmap, pixel_shader=self._pointer_palette)
        self._cursor_grp.append(self._pointer_sprite)
        self._display_grp.append(self._cursor_grp)

    def load_cursor_bitmap(self, cursor_path, sheet_width, sheet_height, tile_width, tile_height):
        """Loads and creates a custom cursor bitmap from a sprite sheet bitmap image.
        :param str cursor_path: Path to cursor bitmap on the CIRCUITPY file system.
        :param int sheet_width: Width of sprite sheet bitmap, in pixels .
        :param int sheet_height: Height of sprite sheet bitmap, in pixels.
        :param int tile_width: Width of cursor image, in pixels.
        :param int tile_height: Height of cursor, in pixels
        """
        import adafruit_imageload
        # remove a pre-generated cursor image
        self._cursor_grp.remove(self._pointer_sprite)
        self._sprite_sheet, self._palette = adafruit_imageload.load(cursor_path,
                                                                    bitmap=displayio.Bitmap,
                                                                    palette=displayio.Palette)
        self._sprite = displayio.TileGrid(self._sprite_sheet, pixel_shader=self._palette,
                                          width=sheet_width,
                                          height=sheet_height,
                                          tile_width=tile_width,
                                          tile_height=tile_height)
        self._cursor_grp = displayio.Group(max_size=1, scale=self._scale)
        self._cursor_grp.append(self._sprite)
        self._display_grp.append(self._cursor_grp)
