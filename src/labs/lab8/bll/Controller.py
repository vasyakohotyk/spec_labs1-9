import logging

from labs.lab8.bll.Plots import *
from labs.lab8.dal.SettingsModel import SettingsModel
from shared.services.relative_to_absolute_path import absolute

logger = logging.getLogger(__name__)


class Controller:
    """
    Controller Class:
    This class encapsulates functionality to manage and visualize activity and sleep data.

    Methods:
    __init__(settings: SettingsModel, activity_data, sleep_data)
        Initializes the Controller with specified settings, activity data, and sleep data.

    get_default_save_dir()
        Retrieves the default directory path for saving plots from the settings.

    get_default_file_name()
        Gets the default file name for saving plots from the settings.

    steps_vs_calories()
        Plots the relationship between steps taken and calories burned from the activity data.

    rem_and_bed_time()
        Plots REM sleep and bed time data from the sleep data.

    sleep_activity_relationships()
        Plots the relationships between sleep data and activity data.

    steps_by_date()
        Plots the steps taken each day from the activity data.

    steps_by_years()
        Plots the steps taken each year from the activity data.

    sleep_duration()
        Plots the duration of sleep from the activity and sleep data.

    correlation_heatmap()
        Plots a heatmap showing correlations between various activity and sleep data metrics.

    sleep_phases_distribution()
        Plots the distribution of different sleep phases from the sleep data.

    rem_sleep_vs_steps()
        Plots the relationship between REM sleep and steps taken from the activity and sleep data.

    monthly_sleep_patterns()
        Plots the patterns of sleep on a monthly basis from the sleep data.

    nap_days_per_month()
        Plots the number of days naps were taken each month from the sleep data.

    is_plot_exist()
        Checks if a plot has been created and is stored in the instance variable.

    show()
        Displays the currently stored plot.

    save(file_path)
        Saves the current plot to the specified file path and then shows the plot.

    get_logger_path()
        Retrieves the logger path from the settings. Raises KeyError if logger path is not provided.
    """

    def __init__(self, settings: SettingsModel, activity_data, sleep_data):
        self.settings = settings
        self.activity_data = activity_data
        self.sleep_data = sleep_data
        self.plot = None

    def get_default_save_dir(self):
        save_path = self.settings.get_assets_save_dir()
        path = absolute(save_path)
        return path

    def get_default_file_name(self):
        return self.settings.get_default_file_name()

    def steps_vs_calories(self):
        activity = self.activity_data
        self.plot = plot_steps_vs_calories(activity)

    def rem_and_bed_time(self):
        sleep = self.sleep_data
        self.plot = plot_rem_and_bed_time(sleep)

    def sleep_activity_relationships(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_sleep_activity_relationships(activity, sleep)

    def steps_by_date(self):
        activity = self.activity_data
        self.plot = plot_steps_by_date(activity)

    def steps_by_years(self):
        activity = self.activity_data
        self.plot = plot_steps_by_years(activity)

    def sleep_duration(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_sleep_duration(activity, sleep)

    def correlation_heatmap(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_correlation_heatmap(activity, sleep)

    def sleep_phases_distribution(self):
        sleep = self.sleep_data
        self.plot = plot_sleep_phases_distribution(sleep)

    def rem_sleep_vs_steps(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_rem_sleep_vs_steps(activity, sleep)

    def monthly_sleep_patterns(self):
        sleep = self.sleep_data
        self.plot = plot_monthly_sleep_patterns(sleep)

    def nap_days_per_month(self):
        sleep = self.sleep_data
        self.plot = plot_nap_days_per_month(sleep)

    def is_plot_exist(self):
        return self.plot is not None

    def show(self):
        self.plot.show()

    def save(self, file_path):
        if file_path:
            self.plot.savefig(file_path)
        self.plot.show()

    def get_logger_path(self):
        path = self.settings.get_logger_path()
        if not path:
            raise KeyError("There no logger path provided!")

        absolute_path = absolute(path)
        return absolute_path
