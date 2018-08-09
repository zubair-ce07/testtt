# -*- coding: utf-8 -*-
"""
This is basic run application scrip, the script is generalized and can be used to word with other applications as well.
"""
from app_factory.weather_man_app.utils.global_contants import ArgsParserCategories
from app_factory.weather_man_app.utils import weather_man_parser
from app_factory.weather_man_app.weather_man import WeatherMan
from app_factory.configs.app_configs import AppConfigs


class App(object):

    def __init__(self, execution_control, application):
        self.application = application
        self.execution_control = execution_control

    def execute_app(self):
        """
        Executes application, by calling WeatherMan function with specific option argument.
        """
        for category in ArgsParserCategories.get_categories():
            control_value = getattr(self.execution_control, category)
            if control_value:
                self.application.show_result(
                    self.execution_control.file_path, category, control_value
                )


def start_weatherman_app():
    AppConfigs.parser = weather_man_parser.parser
    AppConfigs.app_name = 'weather-man'
    args = AppConfigs.parser.parse_args()
    App(args, WeatherMan()).execute_app()


if __name__ == '__main__':
    start_weatherman_app()
