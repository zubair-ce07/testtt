
def report_generator(report, calculation_result):
    if report == 'e':
        generate_yearly_report(calculation_result)
    elif report == 'a':
        generate_monthly_report(calculation_result)
    elif report == 'c':
        generate_bar_chart(calculation_result)


def generate_yearly_report(calculation_result):
    max_temp = calculation_result.get('max_temp')
    max_temp_day = calculation_result.get('max_temp_day')
    low_temp = calculation_result.get('low_temp')
    low_temp_day = calculation_result.get('low_temp_day')
    max_humid = calculation_result.get('max_humid')
    max_humid_day = calculation_result.get('max_humid_day')

    result = "\nYearly Analysis Report Generated :\n\n Highest: {0}C on {1}\n Lowest: {2}C on {3} \n Humidity: {4}% " \
             "on {5} \n".format(max_temp, max_temp_day, low_temp, low_temp_day, max_humid, max_humid_day)

    print(result)
    print('--------------------------------')


def generate_monthly_report(calculation_result):
    avg_max_temp = calculation_result.get('avg_max_temp')
    avg_low_temp = calculation_result.get('avg_low_temp')
    avg_mean_humid = calculation_result.get('avg_mean_humid')

    result = "\nMonthly Analysis Report Generated : \n\n Highest Average: {0}C \n Lowest Average: {1}C \n " \
             "Average Mean Humidity: {2}% \n".format(avg_max_temp, avg_low_temp, avg_mean_humid)

    print(result)
    print('--------------------------------')


def generate_bar_chart(calculation_result):
    print('\nBar Chart Report Generated : \n\n')
    for record in calculation_result:
        max_temp = record.get('max_temp')
        low_temp = record.get('low_temp')
        day = record.get('day')
        max_tmp_bar = '+' * max_temp
        low_tmp_bar = '+' * low_temp
        print("{0}\033[31m {1} {2}C \n{0}\033[34m {3} {4}C".format(day, max_tmp_bar, max_temp, low_tmp_bar, low_temp))

    print('--------------------------------')


def generate_bonus_bar_chart(calculation_result):
    print('\nBonus implementation single bar chart : \n\n')
    for record in calculation_result:
        max_temp = record.get('max_temp')
        low_temp = record.get('low_temp')
        day = record.get('day')
        low_tmp_bar = '+' * low_temp
        remain_tmp = '+' * (max_temp - low_temp)

        print("{0}\033[34m {1}\033[31m{2} \033[34m {3}C - \033[31m {4}C".format(day, low_tmp_bar, remain_tmp, low_temp,
                                                                                max_temp))

    print('--------------------------------')

