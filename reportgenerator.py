blue = '\033[34m'
red = '\033[31m'


def generate_yearly_report(record):
    max_temp_record, low_temp_record, humidity_record = record

    print(
        f"Yearly Analysis Report Generated :\n\n"
        f" Highest: {max_temp_record.max_temp}C on {max_temp_record.date.strftime('%B %d')}\n"
        f" Lowest: {low_temp_record.low_temp}C on {low_temp_record.date.strftime('%B %d')} \n "
        f"Humidity: {humidity_record.max_humid}% on {humidity_record.date.strftime('%B %d')}"
    )


def generate_monthly_report(record):
    avg_max_temp, avg_low_temp, avg_mean_humid = record

    print(
        f"\nMonthly Analysis Report Generated : \n\n"
        f"Highest Average: {avg_max_temp}C \n"
        f"Lowest Average: {avg_low_temp}C \n"
        f"Average Mean Humidity: {avg_mean_humid}%\n"
    )


def generate_bar_chart(records):
    print('\nBar Chart Report Generated : \n')

    for record in records:
        day = record.date.day
        max_tmp_bar = '+' * record.max_temp
        low_tmp_bar = '+' * record.low_temp
        print(
            f"{day} {red}{max_tmp_bar} {record.max_temp}C \n"
            f"{day} {blue}{low_tmp_bar} {record.low_temp}C"
        )


def generate_bonus_bar_chart(records):
    print('\nBonus implementation single bar chart : \n')

    for record in records:
        day = record.date.day
        low_tmp_bar = '+' * record.low_temp
        remain_tmp = '+' * (record.max_temp - record.low_temp)
        print(f"{day} {blue}{low_tmp_bar}{red}{remain_tmp} {blue}{record.low_temp}C - {red}{record.max_temp}C")
