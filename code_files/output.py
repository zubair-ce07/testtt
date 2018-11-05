from termcolor import colored, cprint


def display_monthly_report(report, report_specs):
    """Output function for monthly reports"""
    year = report_specs.year
    month = report_specs.strftime('%B')
    cprint(colored(f'\n{month}, {year}', attrs=['underline', 'bold']))

    print(f'Highest Average: {round(report["avg_max_temp"], 2)}C')
    print(f'Lowest Average: {round(report["avg_min_temp"], 2)}C')
    print(f'Average Mean Humidity: {round(report["avg_mean_humidity"], 2)}%')

    print('\n---------------------------------')


def display_monthly_graph(reports, report_specs):
    """Output function for monthly graphs"""
    year = report_specs.year
    month = report_specs.strftime('%B')
    cprint(colored(f'\n{month}, {year}', attrs=['underline', 'bold']))

    for index, max_temp, min_temp in enumerate(reports, start=1):

        bar_chart = (colored('-'*abs(min_temp), 'blue', attrs=['bold']) +
                     colored('+'*max_temp, 'red', attrs=['bold']))
        day_count = str(index).rjust(2, '0')
        cprint(f'{day_count} {bar_chart} {min_temp}C-{max_temp}C')

    print('\n---------------------------------')


def display_yearly_report(report, report_specs):
    """Output function for yearly reports"""
    year = report_specs.year
    cprint(colored(f'\nYear {year}', attrs=['underline', 'bold']))

    print(f'Highest: {report["max_temp"].max_temp}C on '\
          f'{report["max_temp"].pkt.strftime("%B")} {report["max_temp"].pkt.strftime("%d")}')

    print(f'Lowest: {report["min_temp"].min_temp}C on '\
          f'{report["min_temp"].pkt.strftime("%B")} {report["min_temp"].pkt.strftime("%d")}')

    print(f'Humidity: {report["max_humidity"].max_humidity}C on '\
          f'{report["max_humidity"].pkt.strftime("%B")} {report["max_humidity"].pkt.strftime("%d")}')


    print('\n---------------------------------')
