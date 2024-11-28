from labs.lab5.dal.Camera import CameraData


class SceneData:
    """
    SceneData class holds information related to a graphical scene.

    Attributes:
        figures (list): A list to store the figures in the scene.
        selected_figure (object): The currently selected figure in the scene.
        is_rotating (bool): A flag indicating whether rotation is active.
        last_mouse_x (int): X-coordinate of the last mouse position.
        last_mouse_y (int): Y-coordinate of the last mouse position.
        camera (CameraData): An instance of CameraData representing the scene's camera.
        point_size (int): Size of points in the scene.
        line_width (int): Width of lines in the scene.
        alpha (float): Transparency level.
        highlight_color (tuple): RGB values for highlight color.
        highlight_line_width (int): Line width for the highlighted figure.
    """

    def __init__(self):
        self.figures = []
        self.selected_figure = None
        self.is_rotating = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.camera = CameraData()
        self.point_size = 30
        self.line_width = 10
        self.alpha = 0.2
        self.highlight_color = (1, 1, 1)
        self.highlight_line_width = 20
