# -*- coding: utf-8 -*-
"""
This is basic run application scrip, the script is generalized and can be used to word with other applications as well.
"""
from configs.app_configs import AppConfig
from parser.args_parser import BaseArgsParser
from weather_man_app.weather_man import WeatherMan
from weather_man_app.utils.args_parser import ParserHelper
from weather_man_app.utils.global_content import ArgsParserCategoryHandler


__author__ = "Arslan"
app_name = "weather-man"


class AppRunner:
    """
    Application executor which get application objects and respective parsers as execution control depending on passed
    command line arguments it execute application.
    """
    def __init__(self, execution_control, application, args_hangler):
        """
        :param execution_control: Args Parser's parsed arguments to control the flow.
        :param application: Specific application required by the user.
        :param args_hangler: Specific application's arguments handler, having information of the arguments.
        """
        self.application = application
        self.execution_control = execution_control
        self.args_hangler = args_hangler

    def execute_app(self):
        """
        Executes application, by calling function with specific option argument.
        """
        for category in self.args_hangler.get_categories():
            control_value = getattr(self.execution_control, category)
            if control_value:
                self.application.show_result(
                    self.execution_control.file_path, category, control_value
                )


def start_app():
    """
    Parse specific app's arguments and get that particular weatherman application through AppRunner.
    """
    AppConfig.parser = BaseArgsParser()
    ParserHelper.add_arguments(AppConfig.parser)
    args = AppConfig.parser.parse_args()
    AppConfig.app_name = app_name
    application, args_handler = WeatherMan(), ArgsParserCategoryHandler
    AppRunner(args, application, args_handler).execute_app()


if __name__ == '__main__':
    """
    Calls start application functionality, if the file run_app.py is run.
    """
    start_app()
