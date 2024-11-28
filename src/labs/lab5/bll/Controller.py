from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from labs.lab5.ui.Keyboard import KeyboardHandler
from labs.lab5.ui.Mouse import MouseHandler
from labs.lab5.ui.Renderer import AsciiRenderer
from shared.classes.dict_json import DictJsonDataAccess
from shared.classes.file_data_access import FileDataAccess
from shared.classes.ordered_set import OrderedSet


class Controller:
    """
    Controller class to handle interactions with the scene, including keyboard and mouse events, rendering, and settings management.
    """

    def __init__(
        self,
        scene,
        keyboard_handler: KeyboardHandler,
        mouse_handler: MouseHandler,
        settings_path,
    ):
        self.scene = scene
        self.settings = DictJsonDataAccess(settings_path)
        self.renderer = None
        self.set_up_renderer()
        self.pressed_keys = OrderedSet()
        self.scenes_folder = self.settings.get("scenes_folder")
        self.__scenes_access = FileDataAccess()
        self.file_name = None
        self.keyboard_handler = keyboard_handler
        self.mouse_handler = mouse_handler
        self.keyboard_handler.set_controller(self)
        self.mouse_handler.set_controller(self)
        self.last_screen = None
        self.show_callback = None
        self.action_values = {
            "draw_points": {"action": self.set_draw_mode, "args": ("points",)},
            "draw_edges": {"action": self.set_draw_mode, "args": ("edges",)},
            "draw_faces": {"action": self.set_draw_mode, "args": ("faces",)},
            "translate_left": {
                "action": self.translate_figure_or_camera,
                "args": (-0.5, 0, 0),
            },
            "translate_right": {
                "action": self.translate_figure_or_camera,
                "args": (0.5, 0, 0),
            },
            "translate_forward": {
                "action": self.translate_figure_or_camera,
                "args": (0, 0, -0.5),
            },
            "translate_backward": {
                "action": self.translate_figure_or_camera,
                "args": (0, 0, 0.5),
            },
            "translate_up": {
                "action": self.translate_figure_or_camera,
                "args": (0, 0.5, 0),
            },
            "translate_down": {
                "action": self.translate_figure_or_camera,
                "args": (0, -0.5, 0),
            },
            "rotate_x_plus": {
                "action": self.rotate_figure_or_camera,
                "args": (0, -5, 0),
            },
            "rotate_x_minus": {
                "action": self.rotate_figure_or_camera,
                "args": (0, 5, 0),
            },
            "rotate_y_plus": {
                "action": self.rotate_figure_or_camera,
                "args": (5, 0, 0),
            },
            "rotate_y_minus": {
                "action": self.rotate_figure_or_camera,
                "args": (-5, 0, 0),
            },
            "increase_render_distance": {
                "action": self.change_camera_perspective,
                "args": (None, None, None, +10.0),
            },
            "decrease_render_distance": {
                "action": self.change_camera_perspective,
                "args": (None, None, None, -10.0),
            },
            "zoom_up": {
                "action": self.change_camera_perspective,
                "args": (-5.0, None, None, None),
            },
            "zoom_down": {
                "action": self.change_camera_perspective,
                "args": (5.0, None, None, None),
            },
            "exit": {"action": self.exit, "args": ()},
        }

    def shortcuts(self):
        return self.settings.get("shortcuts")

    def action_keys(self):
        return self.settings.get("action_keys")

    def handle_actions(self, modifiers):
        for pressed_key in self.pressed_keys:
            if modifiers:
                action_name = self.shortcuts().get(modifiers).get(pressed_key)
                if not action_name:
                    continue
                self.execute_command(action_name)
                break
            action_keys = self.action_keys()
            if pressed_key not in action_keys.keys():
                continue
            action_name = action_keys.get(pressed_key)
            self.execute_command(action_name)

    def handle_keyboard_up(self, key):
        self.pressed_keys.discard(key)

    def handle_keyboard(self, key, modifiers):
        self.pressed_keys.add(key)
        self.handle_actions(modifiers)
        glutPostRedisplay()

    def handle_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.scene.handle_click(x, y, button)
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            self.scene.data.is_rotating = True
            self.scene.data.last_mouse_x = x
            self.scene.data.last_mouse_y = y
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
            self.scene.data.is_rotating = False
        glutPostRedisplay()

    def handle_wheel(self, wheel, direction, x, y):
        if direction > 0:
            self.execute_command("zoom_up")
        else:
            self.execute_command("zoom_down")
        glutPostRedisplay()

    def handle_motion(self, x, y):
        self.scene.handle_motion(x, y)

    def execute_command(self, action_key):
        command = self.action_values.get(action_key)
        if not command:
            return
        action = command.get("action")
        args = command.get("args")
        action(*args)
        glutPostRedisplay()

    def reset_perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        fov = self.scene.data.camera.data.fovy if self.scene.data.camera.data else 45.0
        aspect = glutGet(GLUT_WINDOW_WIDTH) / max(glutGet(GLUT_WINDOW_HEIGHT), 1)
        z_near = (
            self.scene.data.camera.data.z_near if self.scene.data.camera.data else 1.0
        )
        z_far = (
            self.scene.data.camera.data.z_far if self.scene.data.camera.data else 50.0
        )
        gluPerspective(fov, aspect, z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
        glutPostRedisplay()

    def set_height(self, number):
        ascii_window = self.settings.get("ascii_window")
        ascii_window["ascii_height"] = number
        self.settings.set("ascii_window", ascii_window)
        self.renderer.set_ascii_height(number)

    def display(self):
        scene_draw_func = self.scene.draw
        self.last_screen = self.renderer.display(scene_draw_func)
        self.print_screen()

    def get_scene(self, remove_color=True):
        if remove_color:
            stripped_scene = []
            for line in self.last_screen.split("\n"):
                stripped_line = ""
                i = 0
                while i < len(line):
                    if (
                        line[i : i + 2] == "\033["
                    ):  # Detect the start of the ANSI escape sequence
                        i = (
                            line.find("m", i) + 1
                        )  # Skip to the end of the ANSI escape sequence
                    else:
                        stripped_line += line[i]
                        i += 1
                stripped_scene.append(stripped_line)
            return "\n".join(stripped_scene)
        return self.last_screen

    def print_screen(self):
        print_settings = self.settings.get("print_settings")
        title = print_settings.get("title")
        scene = self.get_scene(False)
        after_screen = print_settings.get("after_screen")
        text = "\n".join([title, scene, after_screen])
        print(text)

    def reshape(self, width, height):
        fov = self.scene.data.camera.data.fovy if self.scene.data.camera.data else 45.0
        aspect = width / height if width and height else 1.5
        z_near = (
            self.scene.data.camera.data.z_near if self.scene.data.camera.data else 1.0
        )
        z_far = (
            self.scene.data.camera.data.z_far if self.scene.data.camera.data else 50.0
        )
        self.renderer.reshape(width, height, fov, aspect, z_near, z_far)

    def set_draw_mode(self, draw_mode):
        if self.scene.data.selected_figure:
            self.scene.data.selected_figure.set_draw_mode(draw_mode)
        else:
            for figure in self.scene.data.figures:
                figure.set_draw_mode(draw_mode)

    def set_file_name(self, file_name):
        self.file_name = file_name

    def save_scene(self):
        scenes_folder = self.settings.get("scenes_folder")
        file_name = self.file_name
        full_path = scenes_folder + file_name
        self.__scenes_access.set_file_path(full_path)
        scene = self.get_scene()
        if not scene:
            raise ValueError("No scene to save")
        self.__scenes_access.set(scene)

    def make_scene(self):
        self.glut_init()
        self.add_handlers()
        glutMainLoop()

    def stop_scene(self):
        glutLeaveMainLoop()
        if self.file_name:
            self.save_scene()

    def translate_figure_or_camera(self, x, y, z):
        if self.scene.data.selected_figure:
            self.scene.data.selected_figure.translate(x, y, z)
        else:
            self.scene.data.camera.translate(x, y, z)

    def rotate_figure_or_camera(self, dx, dy, dz):
        if self.scene.data.selected_figure:
            self.scene.data.selected_figure.rotate(dx, dy, dz)
        else:
            self.scene.data.camera.rotate(dx, dy, dz)

    def change_camera_perspective(self, delta_fovy, aspect, delta_z_near, delta_z_far):
        if delta_z_far is not None:
            self.scene.data.camera.update_z_far(delta_z_far)
        if delta_fovy is not None:
            self.scene.data.camera.update_fovy(delta_fovy)
        if aspect is not None:
            self.scene.data.camera.update_aspect(aspect)
        if delta_z_near is not None:
            self.scene.data.camera.update_z_near(delta_z_near)
        self.reset_perspective()

    def exit(self):
        self.stop_scene()

    def set_up_renderer(self):
        window_settings = self.settings.get("window_settings")
        height = window_settings.get("height")
        width = window_settings.get("width")
        ascii_window = self.settings.get("ascii_window")
        ascii_chars = ascii_window.get("ascii_chars")
        color_palette = ascii_window.get("color_palette")
        ascii_height = ascii_window.get("ascii_height")
        self.renderer = AsciiRenderer(
            width, height, ascii_height, ascii_chars, color_palette
        )

    def glut_init(self):
        window_settings = self.settings.get("window_settings")
        height = window_settings.get("height")
        width = window_settings.get("width")
        title = window_settings.get("title")
        fov = window_settings.get("fov")
        z_near = window_settings.get("z_near")
        z_far = window_settings.get("z_far")
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
        glutInitWindowSize(width, height)
        glutCreateWindow(ctypes.c_char_p(title.encode("utf-8")).value)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, width / height, z_near, z_far)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_STENCIL_TEST)
        glDisable(GL_LIGHTING)

    def add_handlers(self):
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutSpecialFunc(self.keyboard_handler.special_keyboard)
        glutSpecialUpFunc(self.keyboard_handler.special_keyboard_up)
        glutKeyboardFunc(self.keyboard_handler.keyboard)
        glutKeyboardUpFunc(self.keyboard_handler.keyboard_up)
        glutMouseFunc(self.mouse_handler.mouse)
        glutMotionFunc(self.mouse_handler.motion)
        glutMouseWheelFunc(self.mouse_handler.wheel)
