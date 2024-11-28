from OpenGL.GLUT import *

SHIFT = GLUT_ACTIVE_SHIFT
CTRL = GLUT_ACTIVE_CTRL
ALT = GLUT_ACTIVE_ALT
SHIFT_CTRL = SHIFT | CTRL
SHIFT_ALT = SHIFT | ALT
CTRL_ALT = CTRL | ALT
SHIFT_CTRL_ALT = SHIFT | CTRL | ALT

keys_map = {
    27: "esc",
    32: "enter",
    "\x1b": "esc",
    "\x03": "ctrl+c",
    "\x20": "enter",
    GLUT_KEY_F1: "f1",
    GLUT_KEY_F2: "f2",
    GLUT_KEY_F3: "f3",
    GLUT_KEY_F4: "f4",
    GLUT_KEY_F5: "f5",
    GLUT_KEY_F6: "f6",
    GLUT_KEY_F7: "f7",
    GLUT_KEY_F8: "f8",
    GLUT_KEY_F9: "f9",
    GLUT_KEY_F10: "f10",
    GLUT_KEY_F11: "f11",
    GLUT_KEY_F12: "f12",
    GLUT_KEY_LEFT: "left",
    GLUT_KEY_UP: "up",
    GLUT_KEY_RIGHT: "right",
    GLUT_KEY_DOWN: "down",
    GLUT_KEY_PAGE_UP: "page up",
    GLUT_KEY_PAGE_DOWN: "page down",
    GLUT_KEY_HOME: "home",
    GLUT_KEY_END: "end",
    GLUT_KEY_INSERT: "insert",
    SHIFT: "shift",
    CTRL: "ctrl",
    ALT: "alt",
    SHIFT_ALT: "shift_alt",
    SHIFT_CTRL: "shift_ctr",
    CTRL_ALT: "ctrl_alt",
    SHIFT_CTRL_ALT: "shift_ctr_alt",
    112: "shift",
    114: "ctrl",
    116: "alt",
}
