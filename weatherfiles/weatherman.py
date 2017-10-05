import sys

from FileReader import FileReader
from MonthlyWeatherInfo import MonthlyWeatherInfo
from ReportGeneratorFactory import ReportGeneratorFactory


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('''usage: weatherman.py /path/to/files-dir -option year [-option year] [-option year]
        options: -a, -e, -c''')
        sys.exit(1)

    dir = args[0]

    options = args[1:]
    while len(options)>1:
        files_data = FileReader().read_files_from_path(dir, options[1])
        weathers_info = [MonthlyWeatherInfo(filedata) for filedata in files_data.values()]
        report_generator = ReportGeneratorFactory().get_report_generator(options[0])
        report_generator.generate_report(weathers_info)
        options = options[2:]
        print("-"*20)


if __name__ == '__main__':
    main()
