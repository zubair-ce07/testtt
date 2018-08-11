# -*- coding: utf-8 -*-
"""
This is basic run application scrip, the script is generalized and can be used to word with other applications as well.
"""

from factory import AppFactory
from weather_man_app.utils.global_contants import ArgsParserCategoryHandler
from parser.args_parser import BaseArgsParser
from configs.app_configs import AppConfig


class AppRunner:
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


def start_app():
    """
    Parse specific app's arguments and get that particular application from Application factory and execute flow \
    through AppRunner.
    """
    AppConfig.parser = BaseArgsParser()
    AppConfig.parser.add_sub_parsers()
    args = AppConfig.parser.parse_args()
    AppConfig.app_name = args.command
    application = AppFactory.get_specific_application()
    AppRunner(args, application).execute_app()


if __name__ == '__main__':
    """
    Calls start application functionality, if the file run_app.py is run.
    """
    start_app()
