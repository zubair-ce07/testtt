# -*- coding: utf-8 -*-
"""
This is basic run application scrip, the script is generalized and can be used to word with other applications as well.
"""
from app_factory.weather_man_app.utils.global_contants import ArgsParserCategoryHandler
from app_factory.weather_man_app.utils import weather_man_parser
from app_factory.weather_man_app.weather_man import WeatherMan
from app_factory.configs.app_configs import AppConfig


class App:
    """
    Application executor which get application objects and respective parsers as execution control depending on passed
    command line arguments it execute application.
    """
    def __init__(self, execution_control, application):
        self.application = application
        self.execution_control = execution_control

    def execute_app(self):
        """
        Executes application, by calling WeatherMan function with specific option argument.
        """
        for category in ArgsParserCategoryHandler.get_categories():
            control_value = getattr(self.execution_control, category)
            if control_value:
                self.application.show_result(
                    self.execution_control.file_path, category, control_value
                )


def start_weatherman_app():
    """
    Instantiate weather man and calls parse_args() which are utilized in app as application and execution control
    respectively. Also configures app configurations.
    """
    AppConfig.parser = weather_man_parser.parser
    AppConfig.app_name = 'weather-man'
    args = AppConfig.parser.parse_args()
    App(args, WeatherMan()).execute_app()


if __name__ == '__main__':
    """
    Start application.
    """
    start_weatherman_app()
