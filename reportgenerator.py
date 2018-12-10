
def generate_yearly_report(calculation_result):
    max_temp = calculation_result['max_temp']
    low_temp = calculation_result['low_temp']
    max_humid = calculation_result['max_humid']
    max_temp_day = calculation_result['max_temp_day'].strftime('%B %d')
    low_temp_day = calculation_result['low_temp_day'].strftime('%B %d')
    max_humid_day = calculation_result['max_humid_day'].strftime('%B %d')

    print(f"Yearly Analysis Report Generated :\n\n Highest: {max_temp}C on {max_temp_day}\n Lowest: {low_temp}C on "
          f"{low_temp_day} \n Humidity: {max_humid}% on {max_humid_day}")
    print('--------------------------------')


def generate_monthly_report(calculation_result):
    avg_max_temp = calculation_result['avg_max_temp']
    avg_low_temp = calculation_result['avg_low_temp']
    avg_mean_humid = calculation_result['avg_mean_humid']

    print(f"\nMonthly Analysis Report Generated : \n\n Highest Average: {avg_max_temp}C \n Lowest Average: "
          f"{avg_low_temp}C \n Average Mean Humidity: {avg_mean_humid}% \n")
    print('--------------------------------')


def generate_bar_chart(calculation_result):
    print('\nBar Chart Report Generated : \n')
    for record in calculation_result:
        max_temp = record['max_temp']
        low_temp = record['low_temp']
        day = record['date'].strftime('%d')
        max_tmp_bar = '+' * max_temp
        low_tmp_bar = '+' * low_temp
        print("{0}\033[31m {1} {2}C \n{0}\033[34m {3} {4}C".format(day, max_tmp_bar, max_temp, low_tmp_bar, low_temp))
    print('--------------------------------')


def generate_bonus_bar_chart(calculation_result):
    print('\nBonus implementation single bar chart : \n')
    for record in calculation_result:
        max_temp = record['max_temp']
        low_temp = record['low_temp']
        day = record['date'].strftime('%d')
        low_tmp_bar = '+' * low_temp
        remain_tmp = '+' * (max_temp - low_temp)
        print(f"{day}\033[34m {low_tmp_bar}\033[31m{remain_tmp} \033[34m {low_temp}C - \033[31m {max_temp}C")
    print('--------------------------------')
