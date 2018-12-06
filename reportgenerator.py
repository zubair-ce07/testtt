
def report_generator(report, calculation_result):
    output = []
    if report == 'yearly':
        output = generate_yearly_report(calculation_result)
    elif report == 'monthly':
        output = generate_monthly_report(calculation_result)
    elif report == 'bar_chart':
        output = generate_bar_chart(calculation_result)

    for item in output:
        print(item)
    print('--------------------------------')


def generate_bar_chart(calculation_result):
    output, bonus_task = [], []
    output.append('\nBar Chart Report Generated : \n')
    bonus_task.append('\nBonus implementation single bar chart :')

    for item in calculation_result:
        max_temp_bar, low_temp_bar, remain_max_temp = '', '', ''
        if item['max_temp'] != '':
            max_temp_bar = '+' * int(item['max_temp'])

        if item['low_temp'] != '':
            low_temp_bar = '+' * int(item['low_temp'])

        remain_max_temp = '+' * (len(max_temp_bar) - len(low_temp_bar))
        output.append("%s \033[31m %s %sC"%(item['day'], max_temp_bar,item['max_temp']))
        output.append("%s \033[34m %s %sC" % (item['day'], low_temp_bar, item['low_temp']))
        bonus_task.append("%s \033[34m %s \033[31m %s \033[34m %sC - \033[31m %sC" % (item['day'], low_temp_bar, remain_max_temp, item['low_temp'], item['max_temp']))

    output.extend(bonus_task)

    return output


def generate_yearly_report(calculation_result):
    output = []
    output.append('\nYearly Analysis Report Generated : \n')
    output.append('Highest: %sC on %s' % (str(calculation_result.max_temp), calculation_result.max_temp_day))
    output.append('Lowest: %sC on %s' % (str(calculation_result.low_temp), calculation_result.low_temp_day))
    output.append('Humidity: %s%% on %s' % (str(calculation_result.max_humid), calculation_result.max_humid_day))
    return output

def generate_monthly_report(calculation_result):
    output = []
    output.append('\nMonthly Analysis Report Generated : \n')
    output.append('Highest Average: %sC' % (str(calculation_result.average_max_temp)))
    output.append('Lowest Average: %sC' % (str(calculation_result.average_low_temp)))
    output.append('Average Mean Humidity: %s%%' % (str(calculation_result.average_mean_humid)))
    return output
