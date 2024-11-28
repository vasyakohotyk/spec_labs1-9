import logging
import tkinter as tk
from tkinter import filedialog

import pyautogui

from labs.lab8.bll.Controller import Controller
from shared.classes.input import BoolInput
from shared.classes.menu_builder import MenuBuilder

logger = logging.getLogger(__name__)


class UserInterface:
    """
    Class UserInterface is responsible for handling the user interface elements, including building the main menu, displaying options, and managing user choices for visualizing and saving sleep and activity data.

    Methods:
        __init__(self, controller: Controller)
            Constructor to initialize the UserInterface with a controller.

        show(self)
            Displays the main menu.

        build_main(self)
            Builds the main menu with various data visualization options.

        steps_vs_calories(self)
            Handles the steps versus calories visualization option.

        rem_and_bed_time(self)
            Handles the REM sleep and bed time visualization option.

        sleep_activity_relationships(self)
            Handles the sleep and activity relationships visualization option.

        steps_by_date(self)
            Handles the total steps by date visualization option.

        steps_by_years(self)
            Handles the total steps by years visualization option.

        sleep_duration(self)
            Handles the sleep duration visualization option.

        correlation_heatmap(self)
            Handles the correlation heatmap visualization option.

        sleep_phases_distribution(self)
            Handles the sleep phases distribution visualization option.

        rem_sleep_vs_steps(self)
            Handles the REM sleep vs steps visualization option.

        monthly_sleep_patterns(self)
            Handles the monthly sleep pattern visualization option.

        nap_days_per_month(self)
            Handles the nap days per month visualization option.

        want_to_save(self)
            Prompts the user if they want to save the visualization and processes their choice.

        get_results(self)
            Gets the current state of plot visualization and returns status messages.

        save(self)
            Saves the current plot to the specified file path.

        save_file_dialog(self)
            Opens a file dialog for saving the plot to a chosen file path and returns the path.
    """

    def __init__(self, controller: Controller):
        self.controller = controller

        self.main_menu = self.build_main()

    def show(self):
        self.main_menu.show()

    def build_main(self):
        menu = (
            MenuBuilder()
            .set_title("Sleep and activity data visualization")
            .add_option("1", "\n1. Steps vs calories", self.steps_vs_calories)
            .add_option("2", "\n2. REM and bed time", self.rem_and_bed_time)
            .add_option(
                "3",
                "\n3. Sleep and activity relationships",
                self.sleep_activity_relationships,
            )
            .add_option("4", "\n4. Total steps", self.steps_by_date)
            .add_option("5", "\n5. Total steps by years", self.steps_by_years)
            .add_option("6", "\n6. Sleep duration", self.sleep_duration)
            .add_option("7", "\n7. Correlation heatmap", self.correlation_heatmap)
            .add_option(
                "8", "\n8. Sleep phases distribution", self.sleep_phases_distribution
            )
            .add_option("9", "\n9. REM sleep vs steps", self.rem_sleep_vs_steps)
            .add_option(
                "10", "\n10. Monthly sleep pattern", self.monthly_sleep_patterns
            )
            .add_option("11", "\n11. Nap days in month", self.nap_days_per_month)
            .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
            .build()
        )
        return menu

    def steps_vs_calories(self):
        self.controller.steps_vs_calories()
        self.want_to_save()

    def rem_and_bed_time(self):
        self.controller.rem_and_bed_time()
        self.want_to_save()

    def sleep_activity_relationships(self):
        self.controller.sleep_activity_relationships()
        self.want_to_save()

    def steps_by_date(self):
        self.controller.steps_by_date()
        self.want_to_save()

    def steps_by_years(self):
        self.controller.steps_by_years()
        self.want_to_save()

    def sleep_duration(self):
        self.controller.sleep_duration()
        self.want_to_save()

    def correlation_heatmap(self):
        self.controller.correlation_heatmap()
        self.want_to_save()

    def sleep_phases_distribution(self):
        self.controller.sleep_phases_distribution()
        self.want_to_save()

    def rem_sleep_vs_steps(self):
        self.controller.rem_sleep_vs_steps()
        self.want_to_save()

    def monthly_sleep_patterns(self):
        self.controller.monthly_sleep_patterns()
        self.want_to_save()

    def nap_days_per_month(self):
        self.controller.nap_days_per_month()
        self.want_to_save()

    def want_to_save(self):
        true_options = ["yes", "y", "+"]
        false_options = ["no", "n", "-"]
        message = "Do you want to save (yes/no)?"
        warning_message = (
            f"There no such option. {",".join(true_options + false_options)} only"
        )
        is_want = BoolInput.input(
            message, [true_options, false_options], warning_message
        )
        if is_want:
            self.save()
        else:
            self.controller.show()

    def get_results(self):
        if not self.controller.is_plot_exist():
            return "No plot yet"
        self.controller.show()
        return "Shown"

    def save(self):
        if not self.controller.is_plot_exist():
            print("No plot yet")
            return
        file_path = self.save_file_dialog()
        extensions = [".png", ".pdf", ".svg"]
        if not file_path.endswith(tuple(extensions)):
            print("Invalid file extension!")
            return
        if file_path == "":
            print("Empty filepath!")
        self.controller.save(file_path)

    def save_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        default_name = self.controller.get_default_file_name()
        default_path = self.controller.get_default_save_dir()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
            ],
            initialfile=default_name,
            initialdir=default_path,
            title="Save. You can choose .png, .pdf or .svg file types. ",
        )
        root.destroy()
        return file_path or ""
