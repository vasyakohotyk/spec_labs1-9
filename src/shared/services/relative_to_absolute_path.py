"""
This module contains utility functions for path manipulation,
including functions to get absolute paths from relative paths
and to obtain the root directory of the project.
"""

from os.path import abspath, dirname, join


def absolute(relative_path=None):
    """
    Get absolute path from relative path list of components.

    :param relative_path: List of path components that need to be joined to form a relative path.
    :type relative_path: list
    :return: Absolute path generated from the relative path components.
    :rtype: str
    """
    if not relative_path:
        return root_dir()
    relative_path_string = join(*relative_path)
    return absolute_from_string(relative_path_string)


def root_dir():
    """
    Get the root directory of the project.

    :return: Root directory of the project.
    :rtype: str
    """
    return dirname(dirname(dirname(abspath(__file__))))


def absolute_from_string(relative_path):
    """
    Get absolute path from a relative path string.

    :param relative_path: A relative file system path from the root directory of the project.
    :type relative_path: str
    :return: The absolute file system path derived from the relative path.
    :rtype: str
    """
    root = root_dir()
    return join(root, relative_path)
