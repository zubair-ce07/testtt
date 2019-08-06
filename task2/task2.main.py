from task2.filesutility import FileUtility
from task2.calculation import Calculation
from task2.inpututility import InputUtility
from task2.report import Report


def main():
    base_path = "weatherfiles/"
    weathers = FileUtility.parse_files(base_path)
    if weathers:
        month, year = InputUtility.prompt_user()
        result = Calculation.calculate_report(month, year, weathers)
        Report.print_report(result)


main()
