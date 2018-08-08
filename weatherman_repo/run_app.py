from utils.args_parser import parser
from utils.weather_man import WeatherMan
from utils.globals import ArgsParserOptions


class WeatherManApp(object):

    def __init__(self, execution_control):
        self.weather_man = WeatherMan()
        self.execution_control = execution_control

    def execute_app(self):
        """
        Executes application, by calling WeatherMan function with specific option argument.
        """
        for option in ArgsParserOptions.get_options():
            control_value = getattr(self.execution_control, option)
            if control_value:
                self.weather_man.show_result(
                    self.execution_control.file_path, option, control_value
                )


def main():
    args = parser.parse_args()
    WeatherManApp(args).execute_app()


if __name__ == '__main__':
    main()
