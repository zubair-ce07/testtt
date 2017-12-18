import sys

from django.conf import settings

from forecast.core.monthly_weather_info import MonthlyWeatherInfo
from forecast.core.report_generator_factory import ReportGeneratorFactory

from forecast.core.file_reader import FileReader


def generate(options, dir):
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.

    if not options:
        print('''invalid request''')
        sys.exit(1)

    files_data = FileReader.read_files_from_path(dir, options['year'], options['month'])
    weathers_info = [MonthlyWeatherInfo(filedata) for filedata in files_data]
    report_generator = ReportGeneratorFactory.get_report_generator(options['type'])
    report = report_generator.generate_report(weathers_info, options['year'], options['month'])
    return report.to_json() if report else None
