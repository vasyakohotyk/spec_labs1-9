import math

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from labs.lab5.dal.Figure import colors, figures


class FigureWrapper:
    """
    A wrapper class for managing 3D figure data and operations.

    Methods
    -------
    __init__(data=None)
        Initializes the FigureWrapper instance with optional data.

    set_data(data)
        Sets the figure data.

    create(cls, name)
        Class method to create an instance with an example figure.

    set_example(name)
        Sets the figure data to a predefined example.

    set_color(color)
        Sets the color of the figure and its vertices.

    apply_color_transformation(transformation)
        Applies a color transformation to the figure.

    rotate(dx, dy, dz)
        Rotates the figure by specified angles in degrees about the x, y, and z axes.

    translate(x, y, z)
        Translates the figure by specified amounts along the x, y, and z axes.

    set_draw_mode(mode)
        Sets the drawing mode of the figure (points, edges, or faces).

    draw_points()
        Draws the vertices of the figure as points.

    draw_edges()
        Draws the edges of the figure.

    draw_faces()
        Draws the faces of the figure.

    draw_custom(point_size=5, line_width=2, alpha=0.5, highlight_color=(1, 1, 1), highlight_line_width=2)
        Custom drawing method with configurable parameters.

    draw_points_custom(point_size)
        Draws the vertices of the figure as points with custom size.

    draw_edges_custom(line_width, highlight_line_width)
        Draws the edges of the figure with custom line widths.

    draw_faces_custom(alpha, highlight_color, highlight_line_width)
        Draws the faces of the figure with custom transparency and highlight options.

    scale(scale_x, scale_y, scale_z)
        Scales the figure by specified factors along the x, y, and z axes.

    draw()
        Dispatches the draw call to the appropriate drawing method based on the current draw mode.

    project_vertices_to_screen(modelview, projection, viewport)
        Projects the 3D vertices of the figure to 2D screen coordinates.

    contains_point(x, y, modelview, projection, viewport)
        Checks if a screen point is within the bounds of the projected figure.
    """

    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        if data:
            self.data = data

    @classmethod
    def create(cls, name):
        instance = cls()
        instance.set_example(name)
        return instance

    def set_example(self, name):
        if name not in figures.keys():
            raise ValueError("Wrong example name")
        self.data = figures[name]

    def set_color(self, color):
        if color in colors.keys():
            color = colors[color]
        if len(color) != 3:
            raise ValueError("Color must be a tuple of 3 elements (R, G, B).")
        self.data.color = color
        for vertex in self.data.vertices:
            vertex.color = color

    def apply_color_transformation(self, transformation):
        if not callable(transformation):
            raise ValueError(
                "Transformation must be a callable function that returns a tuple of 3 elements (R, G, B)."
            )
        new_color = transformation(self.data.color)
        if len(new_color) != 3:
            raise ValueError(
                "Transformed color must be a tuple of 3 elements (R, G, B)."
            )
        self.data.color = new_color
        for vertex in self.data.vertices:
            vertex.color = new_color

    def rotate(self, dx, dy, dz):
        center = np.mean([v.position for v in self.data.vertices], axis=0)
        self.translate(-center[0], -center[1], -center[2])
        angle_rad_x = math.radians(dx)
        angle_rad_y = math.radians(dy)
        angle_rad_z = math.radians(dz)

        rotation_matrix_x = np.array(
            [
                [1, 0, 0],
                [0, math.cos(angle_rad_x), -math.sin(angle_rad_x)],
                [0, math.sin(angle_rad_x), math.cos(angle_rad_x)],
            ]
        )

        rotation_matrix_y = np.array(
            [
                [math.cos(angle_rad_y), 0, math.sin(angle_rad_y)],
                [0, 1, 0],
                [-math.sin(angle_rad_y), 0, math.cos(angle_rad_y)],
            ]
        )

        rotation_matrix_z = np.array(
            [
                [math.cos(angle_rad_z), -math.sin(angle_rad_z), 0],
                [math.sin(angle_rad_z), math.cos(angle_rad_z), 0],
                [0, 0, 1],
            ]
        )

        rotation_matrix = np.dot(
            np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x
        )

        for vertex in self.data.vertices:
            vertex.position = np.dot(vertex.position, rotation_matrix.T)
        self.translate(center[0], center[1], center[2])
        self.data.angle = [
            angle + delta for angle, delta in zip(self.data.angle, [dx, dy, dz])
        ]

    def translate(self, x, y, z):
        translation_matrix = np.array([x, y, z], dtype=np.float32)
        for vertex in self.data.vertices:
            vertex.position += translation_matrix

    def set_draw_mode(self, mode):
        if mode in ["points", "edges", "faces"]:
            self.data.draw_mode = mode

    def draw_points(self):
        glPointSize(5 if self.data.selected else 1)
        glBegin(GL_POINTS)
        for vertex in self.data.vertices:
            glColor3fv(self.data.color if self.data.figure_color else vertex.color)
            glVertex3fv(vertex.position)
        glEnd()

    def draw_edges(self):
        glLineWidth(2 if self.data.selected else 1)
        glBegin(GL_LINES)
        for edge in self.data.edges:
            glColor3fv(self.data.color if self.data.figure_color else edge.color)
            for vertex in edge.vertices:
                glVertex3fv(vertex.position)
        glEnd()

    def draw_faces(self):
        glBegin(GL_QUADS)
        for face in self.data.faces:
            face_color = list(
                self.data.color if self.data.figure_color else face.color
            ) + [0.2]
            glColor4fv(face_color)
            for vertex in face.vertices:
                glVertex3fv(vertex.position)
        glEnd()

        if self.data.selected:
            border_color = (1, 1, 1) if sum(self.data.color) <= 1.5 else (0, 0, 0)
            glColor3fv(border_color)
            glLineWidth(2)
            glBegin(GL_LINES)
            for face in self.data.faces:
                for i in range(len(face.vertices)):
                    start_vertex = face.vertices[i].position
                    end_vertex = face.vertices[(i + 1) % len(face.vertices)].position
                    glVertex3fv(start_vertex)
                    glVertex3fv(end_vertex)
            glEnd()

    def draw_custom(
        self,
        point_size=5,
        line_width=2,
        alpha=0.5,
        highlight_color=(1, 1, 1),
        highlight_line_width=2,
    ):
        glPushMatrix()
        if self.data.draw_mode == "points":
            self.draw_points_custom(point_size)
        elif self.data.draw_mode == "edges":
            self.draw_edges_custom(line_width, highlight_line_width)
        elif self.data.draw_mode == "faces":
            self.draw_faces_custom(alpha, highlight_color, highlight_line_width)
        glPopMatrix()

    def draw_points_custom(self, point_size):
        glPointSize(point_size if self.data.selected else 1)
        glBegin(GL_POINTS)
        for vertex in self.data.vertices:
            glColor3fv(self.data.color if self.data.figure_color else vertex.color)
            glVertex3fv(vertex.position)
        glEnd()

    def draw_edges_custom(self, line_width, highlight_line_width):
        glLineWidth(highlight_line_width if self.data.selected else line_width)
        glBegin(GL_LINES)
        for edge in self.data.edges:
            glColor3fv(self.data.color if self.data.figure_color else edge.color)
            for vertex in edge.vertices:
                glVertex3fv(vertex.position)
        glEnd()

    def draw_faces_custom(self, alpha, highlight_color, highlight_line_width):
        glBegin(GL_QUADS)
        for face in self.data.faces:
            if self.data.figure_color:
                face_color = (*self.data.color, alpha)
            else:
                face.color = (*face.color, alpha)
            # face_color = list((self.data.color if self.data.figure_color else face.color, alpha))
            glColor4fv(face_color)
            for vertex in face.vertices:
                glVertex3fv(vertex.position)
        glEnd()

        if self.data.selected:
            glColor3fv(highlight_color)
            glLineWidth(highlight_line_width)
            glBegin(GL_LINES)
            for face in self.data.faces:
                for i in range(len(face.vertices)):
                    start_vertex = face.vertices[i].position
                    end_vertex = face.vertices[(i + 1) % len(face.vertices)].position
                    glVertex3fv(start_vertex)
                    glVertex3fv(end_vertex)
            glEnd()

    def scale(self, scale_x, scale_y, scale_z):
        center = np.mean([v.position for v in self.data.vertices], axis=0)
        self.translate(-center[0], -center[1], -center[2])

        scale_matrix = np.array(
            [[scale_x, 0, 0], [0, scale_y, 0], [0, 0, scale_z]], dtype=np.float32
        )

        for vertex in self.data.vertices:
            vertex.position = np.dot(vertex.position, scale_matrix.T)

        self.translate(center[0], center[1], center[2])

    def draw(self):
        glPushMatrix()
        if self.data.draw_mode == "points":
            self.draw_points()
        elif self.data.draw_mode == "edges":
            self.draw_edges()
        elif self.data.draw_mode == "faces":
            self.draw_faces()
        glPopMatrix()

    def project_vertices_to_screen(self, modelview, projection, viewport):
        screen_coords = []
        for vertex in self.data.vertices:
            try:
                position = vertex.position.tolist()
                projected = gluProject(
                    position[0],
                    position[1],
                    position[2],
                    modelview,
                    projection,
                    viewport,
                )
                screen_coords.append(projected[:2])
            except ValueError as e:
                print(f"Projection failed for vertex: {vertex} with error {e}")
        return screen_coords

    def contains_point(self, x, y, modelview, projection, viewport):
        screen_coords = self.project_vertices_to_screen(modelview, projection, viewport)
        if not screen_coords:
            return False
        min_x = min(coord[0] for coord in screen_coords)
        max_x = max(coord[0] for coord in screen_coords)
        min_y = min(coord[1] for coord in screen_coords)
        max_y = max(coord[1] for coord in screen_coords)
        contains = min_x <= x <= max_x and min_y <= y <= max_y
        # if contains:
        #     self.data.selected =True
        # else:
        #     self.data.selected = False
        return contains
