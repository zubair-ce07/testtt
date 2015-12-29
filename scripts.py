__author__ = 'adnan'
import os

year_min_humidity_groups = {}
year_max_humidity_groups = {}
year_min_temp_groups = {}
year_max_temp_groups = {}
data = {}


def read_all_files_for_hottest():
    for file in os.listdir("weatherdata"):
        if file.endswith(".txt"):
            find_hottest_day(file)
            find_coldest_day(file)


def read_all_files_for_clodest():
    for file in os.listdir("weatherdata"):
        if file.endswith(".txt"):
            find_coldest_day(file)


def read_all_files():
    for file in os.listdir("weatherdata"):
        if file.endswith(".txt"):
            read_file(file)


def make_df(file):
    file_lines = list(open(os.path.join('weatherdata', file), mode='r'))
    file_lines = map(lambda s: s.strip(), file_lines)
    headings = file_lines[1].split(',')
    headings = map(lambda h: h.strip(), headings)
    dict_list = []
    for line in file_lines[2:-2]:
        values = line.split(',')
        tuppe_items = zip(headings, values)
        line_dict = dict(tuppe_items)
        dict_list.append(line_dict)
    return dict_list


def get_column_value(df, column_names):
    column_values = []
    for a_dict in df:
        for heading, cell_value in a_dict.iteritems():
            if cell_value:
                if heading in column_names:
                    column_values.append(cell_value)
    return column_values


hotest_day = {}


def find_hottest_day(file):
    df = make_df(file)
    for record in df:
        pass
        dates = get_column_value([record], ['PKT', 'PKST'])
        the_date = dates[0]
        year = the_date.split('-')[0]
        max_temperature_cell = record['Max TemperatureC']

        if max_temperature_cell:
            if year in hotest_day:
                pervoius_date,pervious_temp = hotest_day[year]
                if max_temperature_cell > pervious_temp:
                    hotest_day[year] = (the_date, max_temperature_cell)
            else:
                hotest_day[year] = (the_date, max_temperature_cell)


def find_coldest_day(file):
    df = make_df(file)
    for record in df:
        pass
        dates = get_column_value([record], ['PKT', 'PKST'])
        the_date = dates[0]
        year = the_date.split('-')[0]
        max_temperature_cell = record['Max TemperatureC']

        if max_temperature_cell:
            if year in hotest_day:
                pervoius_date,pervious_temp = hotest_day[year]
                if max_temperature_cell < pervious_temp:
                    hotest_day[year] = (the_date, max_temperature_cell)
            else:
                hotest_day[year] = (the_date, max_temperature_cell)


def summarize_coldest_day(reportType):
    for year, value in hotest_day.iteritems():
        date, temp = value
        print '{:<20}'.format(date) + '{:<20}'.format(temp)


def summarize_hottest_day(reportType):
    for year, value in hotest_day.iteritems():
        date, temp = value
        print '{:<20}'.format(date) + '{:<20}'.format(temp)


def report_for_coldest_day():
        print '{:<20}'.format('Year') + '{:<20}'.format('MinTemp')


def report_for_hottest_day():
        print '{:<20}'.format('Year') + '{:<20}'.format('MaxTemp')


def read_file(file):
    df = make_df(file)
    dates = get_column_value(df, ['PKT', 'PKST'])
    year = dates[0].split('-')[0]
    min_temperature_column = get_column_value(df, 'Min TemperatureC')
    max_temperature_column = get_column_value(df, 'Max TemperatureC')
    min_humadity_column = get_column_value(df, 'Min Humidity')
    max_humadity_column = get_column_value(df, 'Max Humidity')

    if min_temperature_column:
        min_temperature = reduce(lambda x, y: min(float(x), float(y)), min_temperature_column)
        year_min_temp_groups.setdefault(year, []).append(min_temperature)

    if max_temperature_column:
        max_temperature = reduce(lambda x, y: max(float(x), float(y)), max_temperature_column)
        year_max_temp_groups.setdefault(year, []).append(max_temperature)

    if min_humadity_column:
        min_humadity = reduce(lambda x, y: min(float(x), float(y)), min_humadity_column)
        year_min_humidity_groups.setdefault(year, []).append(min_humadity)

    if max_humadity_column:
        max_humadity = reduce(lambda x, y: max(float(x), float(y)), max_humadity_column)
        year_max_humidity_groups.setdefault(year, []).append(max_humadity)


def summarize_data(reportType):
    all_years = year_max_temp_groups.keys() + year_min_temp_groups.keys() + year_min_humidity_groups.keys() + year_max_humidity_groups.keys()
    all_years = set(all_years)  # remove duplicate
    for year in all_years:
        min_temp = min(year_min_temp_groups[year])
        max_temp = min(year_max_temp_groups[year])
        min_humd = min(year_min_humidity_groups[year])
        max_humd = max(year_max_humidity_groups[year])
        data[year] = [min_temp, max_temp, min_humd, max_humd]


def show_values_in_nice_columns(a, b, c, d, e, padding_symbol=' '):
    print str(a).ljust(10, padding_symbol) + \
          str(b).ljust(10, padding_symbol) + \
          str(c).ljust(10, padding_symbol) + \
          str(d).ljust(10, padding_symbol) + \
          str(e).ljust(10, padding_symbol)


def show_values_in_nice_columns_for_hottest_day(a, b, padding_symbol=' '):
    print str(a).ljust(10, padding_symbol) + \
          str(b).ljust(10, padding_symbol)


def show_results():
    show_values_in_nice_columns('Year', 'Min Temp', 'Max Temp', 'Min Humd', 'Max Humd')
    show_values_in_nice_columns('', '', '', '', '', padding_symbol='-')
    for year, values in data.iteritems():
        b, c, d, e = values
        show_values_in_nice_columns(year, b, c, d, e)


def show_results_hottest_day():
    show_values_in_nice_columns_for_hottest_day('Year', 'Min Temp', 'Max Temp')
    show_values_in_nice_columns_for_hottest_day('', '', padding_symbol='-')
    for year, values in data.iteritems():
        b, c = values
        show_values_in_nice_columns_for_hottest_day(year, b, c)


# report type
one = 'WeatherSummary'
two = 'HottestDayOfYear'
three = 'ColdestDayOfYear'
reporttype = 'HottestDayOfYear'  # Pass one, two and three for particular report

if reporttype == one:
    read_all_files()
    summarize_data(reporttype)
    show_results()
elif reporttype == two:
    read_all_files_for_hottest()
    report_for_hottest_day()
    summarize_hottest_day(reporttype)
elif reporttype == three:
    read_all_files_for_clodest()
    report_for_coldest_day()
    summarize_coldest_day(reporttype)
else:
    print """ Please enter 'one' for Weather Summary, 'two' for Hottest Day Of the Year, 'three' Coldest Day Of Year"""