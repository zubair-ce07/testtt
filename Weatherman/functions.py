import sys

from FIleGetters import get_file_names
from Classes import YearlyWeatherReport, MonthlyReport , MonthlyRecordBars


def read_files_for_arguments(directory_path ,arg_e , arg_a ,arg_c , arg_d):

    list_of_rows = get_file_names(directory_path, arg_e)
    if list_of_rows:
        get_yearly_record(list_of_rows)
    else:
        error_msg(arg_e)

    list_of_rows = get_file_names(directory_path, arg_a)
    if list_of_rows:
        get_monthly_average(list_of_rows)
    else:
        error_msg(arg_a)

    list_of_rows = get_file_names(directory_path, arg_c)
    if list_of_rows:
        get_monthly_record_bars(list_of_rows)
    else:
        error_msg(arg_c)

    list_of_rows = get_file_names(directory_path, arg_d)
    if list_of_rows:
        get_monthly_single_line_bars(list_of_rows)
    else:
        error_msg(arg_d)


def get_yearly_record(list_of_rows):

    yearly_report = YearlyWeatherReport()
    yearly_report.complete_records = list_of_rows

    new_records = [row for row in yearly_report.complete_records if row.max_temp]
    yearly_report.max_temp_row = max(new_records, key=lambda row: row.max_temp)

    new_records = [row for row in yearly_report.complete_records if row.min_temp]
    yearly_report.min_temp_row = min(new_records, key=lambda row: row.min_temp)

    new_records = [row for row in yearly_report.complete_records if row.max_humidity]
    yearly_report.max_humidity_row = max(new_records, key=lambda row: row.max_humidity)

    yearly_report.print_report()


def get_monthly_average(list_of_rows):

    monthly_report = MonthlyReport()
    monthly_report.complete_records = list_of_rows

    for rows in monthly_report.complete_records:

        if rows.max_temp:
            monthly_report.total_max_temp = monthly_report.total_max_temp + rows.max_temp
            monthly_report.max_temp_count += 1

        if rows.min_temp:
            monthly_report.total_min_temp = monthly_report.total_min_temp + rows.min_temp
            monthly_report.min_temp_count += 1
        if rows.mean_humidity:
            monthly_report.total_mean_humidity = monthly_report.total_mean_humidity + rows.mean_humidity
            monthly_report.mean_humidity_count += 1

    monthly_report.print_report()


def get_monthly_record_bars(list_of_rows):

    monthly_record_bars = MonthlyRecordBars()
    for rows in list_of_rows:

            monthly_record_bars.max_temp_values.append(int(rows.max_temp))
            monthly_record_bars.min_temp_values.append(int(rows.min_temp))
            monthly_record_bars.days.append(rows.get_day())

    print(rows.get_month_year())

    for index in range(0,len(monthly_record_bars.days)):

        sys.stdout.write('\033[1;30m' + monthly_record_bars.days[index] + ' ')
        if monthly_record_bars.max_temp_values[index]:
            printer_bars_charts(monthly_record_bars.max_temp_values[index],1)
        else:
            print('N/A')

        sys.stdout.write(monthly_record_bars.days[index] +' ')
        if monthly_record_bars.min_temp_values[index]:
            printer_bars_charts(monthly_record_bars.min_temp_values[index],0)
        else:
            print('N/A')


def get_monthly_single_line_bars(list_of_rows):

    single_line_records = MonthlyRecordBars()

    for rows in list_of_rows:

        single_line_records.max_temp_values.append(int(rows.max_temp))
        single_line_records.min_temp_values.append(int(rows.min_temp))
        single_line_records.days.append(rows.get_day())

    print '\n'
    print(rows.get_month_year())

    for index in range(0, len(single_line_records.days)):
        sys.stdout.write('\033[1;30m' +  single_line_records.days[index] + ' ')
        if  single_line_records.max_temp_values[index]:
            printer_single_line_chart( single_line_records.max_temp_values[index],  single_line_records.min_temp_values[index])
        else:
            print 'N/A'


def printer_bars_charts(temperature_value, color):

    if color:
        sys.stdout.write('\033[1;31m+' * temperature_value)
    else:
        sys.stdout.write('\033[1;34m+' * temperature_value)
    sys.stdout.write('\033[1;30m ' + str(temperature_value) + 'C')
    sys.stdout.write('\n')


def printer_single_line_chart(max_temp_value, min_temp_value) :

    sys.stdout.write('\033[1;34m+' * min_temp_value)
    sys.stdout.write('\033[1;31m+' * max_temp_value)
    sys.stdout.write('\033[1;30m  ' + str(min_temp_value) + "C - " + str(max_temp_value) + 'C')
    sys.stdout.write('\n')


def error_msg(arg):
    print "File Not Found For Argument {}".format(arg)
    print "Enter Year Between 2004 to 2016 \n"
