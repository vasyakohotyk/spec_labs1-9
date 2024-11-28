import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


class AsciiRenderer:
    """
    AsciiRenderer:

    A class that converts graphical scenes rendered using OpenGL into ASCII art.

    __init__(self, width=None, height=None, ascii_height=None, ascii_chars=None, color_palette=None)
        Initialize the AsciiRenderer with desired attributes such as width, height, ASCII height, characters for ASCII representation, and an optional color palette.

    set_ascii_height(self, ascii_height)
        Set the height (number of rows) for the ASCII representation.

    map_pixel_to_ascii(self, gray_value, color_value)
        Map a pixel's grayscale value to a corresponding ASCII character and apply color using ANSI escape codes.

    render_to_ascii(self)
        Capture the current OpenGL framebuffer, process the image to scale and convert it to grayscale, then generate an ASCII art representation of the image with color data.

    display(self, scene_draw_callback)
        Clear the OpenGL buffers, draw the scene using the provided callback function, convert the output to ASCII art, and update the display.

    reshape(self, width, height, fov, aspect, z_near, z_far)
        Adjust the OpenGL viewport and projection matrix to handle window resizing and ensure a consistent field of view.
    """

    def __init__(
        self,
        width=None,
        height=None,
        ascii_height=None,
        ascii_chars=None,
        color_palette=None,
    ):
        self.width = width
        self.height = height
        self.ascii_height = ascii_height
        self.ascii_chars = ascii_chars
        self.color_palette = color_palette

    def set_ascii_height(self, ascii_height):
        self.ascii_height = ascii_height

    def map_pixel_to_ascii(self, gray_value, color_value):
        scale = gray_value / 255
        char = self.ascii_chars[int(scale * (len(self.ascii_chars) - 1))]
        r, g, b = color_value
        return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

    def render_to_ascii(self):
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (self.width, self.height), pixels)
        height_to_width_ratio = 3
        scaled_height = (
            self.ascii_height if self.ascii_height else int(self.height * 0.2)
        )
        scaled_width = (
            int(scaled_height * (self.width / self.height) * height_to_width_ratio)
            if self.height and self.width
            else int(scaled_height * 3)
        )
        image = image.resize((scaled_width, scaled_height), Image.NEAREST)

        grayscale_image = image.convert("L")
        color_image = np.array(image)

        pixel_data = np.array(grayscale_image)

        ascii_image = []
        for row, color_row in zip(pixel_data[::-1], color_image[::-1]):
            ascii_row = "".join(map(self.map_pixel_to_ascii, row, color_row))
            ascii_image.append(ascii_row)

        return "\n".join(ascii_image)

    def display(self, scene_draw_callback):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        scene_draw_callback()
        ascii_art = self.render_to_ascii()
        glutSwapBuffers()
        return ascii_art

    def reshape(self, width, height, fov, aspect, z_near, z_far):
        if height < 70:
            height = 70
            glutReshapeWindow(width, height)
        self.width = width
        self.height = height
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, aspect, z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
