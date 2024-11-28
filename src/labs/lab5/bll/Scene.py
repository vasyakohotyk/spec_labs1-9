from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from labs.lab5.dal.Scene import SceneData


class Scene:
    """
    Class representing a scene containing figures and a camera.

    Attributes:
        data (SceneData): The scene's data, including figures, camera, and selection information.
    """

    def __init__(self, data=None):
        self.data = data if data else SceneData()

    def set_data(self, data):
        if data:
            self.data = data

    @classmethod
    def create(cls, data=None):
        return cls(data)

    def add_figure(self, figure):
        self.data.figures.append(figure)

    def set_camera(self, camera):
        self.data.camera = camera

    def deselect_figure(self):
        if self.data.selected_figure is not None:
            self.data.selected_figure.data.selected = False
            self.data.selected_figure = None

    def select_figure(self, figure):
        figure.data.selected = True
        self.data.selected_figure = figure

    def selection(self, x, y):
        window_width = glutGet(GLUT_WINDOW_WIDTH)
        window_height = glutGet(GLUT_WINDOW_HEIGHT)
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        self.deselect_figure()
        for figure in self.data.figures:
            if figure.contains_point(
                x, window_height - y - 1, modelview, projection, viewport
            ):
                self.select_figure(figure)
                break

    def handle_click(self, x, y, button):
        if button == GLUT_LEFT_BUTTON:
            window_width = glutGet(GLUT_WINDOW_WIDTH)
            window_height = glutGet(GLUT_WINDOW_HEIGHT)
            viewport = glGetIntegerv(GL_VIEWPORT)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            self.deselect_figure()
            for figure in self.data.figures:
                if figure.contains_point(
                    x, window_height - y - 1, modelview, projection, viewport
                ):
                    self.select_figure(figure)
                    break

    def handle_mouse(self, x, y, button):
        if button == GLUT_LEFT_BUTTON:
            window_width = glutGet(GLUT_WINDOW_WIDTH)
            window_height = glutGet(GLUT_WINDOW_HEIGHT)
            viewport = glGetIntegerv(GL_VIEWPORT)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            self.deselect_figure()
            for figure in self.data.figures:
                if figure.contains_point(
                    x, window_height - y - 1, modelview, projection, viewport
                ):
                    self.select_figure(figure)
                    break

    def handle_motion(self, x, y):
        if self.data.is_rotating and self.data.camera:
            # Update the camera with the movement difference
            dx = x - self.data.last_mouse_x
            dy = y - self.data.last_mouse_y
            sensitivity = 0.1  # adjust sensitivity as needed
            self.data.camera.rotate(dy * sensitivity, dx * sensitivity)

            self.data.last_mouse_x = x
            self.data.last_mouse_y = y
        glutPostRedisplay()

    def draw(self):
        point_size = self.data.point_size if self.data.point_size is not None else 5
        line_width = self.data.line_width if self.data.line_width is not None else 2
        alpha = self.data.alpha if self.data.alpha is not None else 0.5
        highlight_color = (
            self.data.highlight_color
            if self.data.highlight_color is not None
            else (1, 1, 1)
        )
        highlight_line_width = (
            self.data.highlight_line_width
            if self.data.highlight_line_width is not None
            else 2
        )
        if self.data.camera:
            self.data.camera.apply_transformations()
        for figure in self.data.figures:
            figure.draw_custom(
                point_size, line_width, alpha, highlight_color, highlight_line_width
            )
