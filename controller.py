from data_calculator import DataCalculator
from input_handler import Parser
from report_generator import ReportGenerator


if __name__ == "__main__":
    arguments_handle = Parser
    input_arguments = arguments_handle.initialization(arguments_handle)
    path = input_arguments.file_path
    data_extracted = arguments_handle.data_extractor(arguments_handle, path)
    calculator = DataCalculator()
    report = ReportGenerator(calculator)

    if input_arguments.e:
        for arguments in input_arguments.e:
            result = calculator.yearly_analysis(
                data_extracted, arguments.date())
            report.generate_yearly_report(calculator)

    if input_arguments.a:
        for arguments in input_arguments.a:
            result = calculator.monthly_analysis(
                data_extracted, arguments.date())
            report.generate_monthly_report(calculator)

    if input_arguments.b:
        for arguments in input_arguments.b:
            report.generate_bonus_report(data_extracted, arguments.date())
