import dataparser
import calculator
import report_generator
import sys


def get_report(result):
    report = report_generator.ReportGenerator()
    report.get_report(result)

    return report.report


def get_results(command, data):
    c = calculator.Calculator()
    c.compute(command, data)

    return c.result


def get_commands():
    commands = []

    if len(commands) % 2 == 0:
        # We need to ignore 1st and 2nd param
        for x in range(2,len(sys.argv)-1, 2):
            commands.append((sys.argv[x], sys.argv[x+1]))
    else:
        commands.append((0, 0))

    return commands


def get_multi_reports(commands, data):
    multi_reports = ""
    if data is not None:
        for command in commands:
            # The condition checks for validation of requested command
            if is_command_valid(command):
                result = get_results(command, data)
                report = get_report(result)

                multi_reports += "User Command : {} {}\n".format(command[0], command[1])
                multi_reports += (report+"\n\n")

                data.reset_iter()
            else:
                multi_reports += "The user command is not valid!\n\n"

        return multi_reports
    else:
        return "The data provided is not valid!\n\n"


def is_command_valid(command):
    if command[0] == '-e':
        if command[1].isdigit():
            return True
    elif command[0] in ['-a', '-c', '-cb']:
        year_month = command[1].split("/")
        if len(year_month) == 2:
            if year_month[0].isdigit() and year_month[1].isdigit():
                return True

    return False


if __name__ == "__main__":
    # The user provided params starts from index 1
    file_path = sys.argv[1]
    data_parser = dataparser.DataParser()
    data = data_parser.get_data(file_path)

    commands = get_commands()
    reports = get_multi_reports(commands, data)

    print(reports)
