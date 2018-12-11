
def generate_yearly_report(record):
    max_temp_day = record['max_temp_day'].strftime('%B %d')
    low_temp_day = record['low_temp_day'].strftime('%B %d')
    max_humid_day = record['max_humid_day'].strftime('%B %d')

    print(f"Yearly Analysis Report Generated :\n\n Highest: {record['max_temp']}C on {max_temp_day}\n Lowest: "
          f"{record['low_temp']}C on {low_temp_day} \n Humidity: {record['max_humid']}% on {max_humid_day}")


def generate_monthly_report(record):
    print(f"\nMonthly Analysis Report Generated : \n\n Highest Average: {record['avg_max_temp']}C \n Lowest Average: "
          f"{record['avg_low_temp']}C \n Average Mean Humidity: {record['avg_mean_humid']}% \n")


def generate_bar_chart(records):
    print('\nBar Chart Report Generated : \n')
    blue = '\033[34m'
    red = '\033[31m'

    for record in records:
        day = record['date'].strftime('%d')
        max_tmp_bar = '+' * record['max_temp']
        low_tmp_bar = '+' * record['low_temp']
        print(f"{day} {blue}{max_tmp_bar} {record['max_temp']}C \n{day} {red}{low_tmp_bar} {record['low_temp']}C")


def generate_bonus_bar_chart(records):
    print('\nBonus implementation single bar chart : \n')
    blue = '\033[34m'
    red = '\033[31m'

    for record in records:
        day = record['date'].strftime('%d')
        low_tmp_bar = '+' * record['low_temp']
        remain_tmp = '+' * (record['max_temp'] - record['low_temp'])
        print(f"{day} {blue}{low_tmp_bar}{red}{remain_tmp} {blue}{record['low_temp']}C - {red}{record['max_temp']}C")
