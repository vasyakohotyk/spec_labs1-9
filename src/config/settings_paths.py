"""
This module sets up the paths for lab configuration files by converting
their relative paths to absolute paths.
"""

from os import getcwd

from shared.services.relative_to_absolute_path import absolute

current_dir = getcwd()
settings_path_lab1 = absolute(["config", "lab1_settings.json"])
settings_path_lab2 = absolute(["config", "lab2_settings.json"])
settings_path_lab3 = absolute(["config", "lab3_settings.json"])
settings_path_lab4 = absolute(["config", "lab3_settings.json"])
settings_path_lab5 = absolute(["config", "lab5_settings.json"])
settings_path_lab6 = absolute(["config", "lab6_settings.json"])
settings_path_lab7 = absolute(["config", "lab7_settings.json"])
settings_path_lab8 = absolute(["config", "lab8_settings.json"])
settings_path_lab9 = absolute(["config", "lab9_settings.json"])
