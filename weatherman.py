'''
This Module is used to calculate weather reports from data provided
in text files
'''
from datetime import datetime
from os import path as os_path
from sys import argv as sys_argv, exit as sys_exit

# global variables, private to this module
_usage_error = 'usage: path_to_files [-e yyyy] [-a yyyy/mm] [-c yyyy/mm]'
_file_prefix = 'Murree_weather_'
_data_file_ext = '.txt'
_months = [
	'January', 'February', 'March',
	'April', 'May', 'June',
	'July', 'August', 'September',
	'October', 'November', 'December'
]
_switches = [
	'-e', '-a', '-c', '-c1'
]
_file_columns = [
	'date', 'max_temperature', 'mean_temperature', 'min_temperature',
	'dew_point', 'mean_dew_point', 'min_dew_point', 'max_humidity',
	'mean_humidity', 'min_humidity', 'max_sea_level_pressure',
	'mean_sea_level_pressure', 'min_sea_level_pressure', 'max_visibility',
	'mean_visibility', 'min_visibility', 'max_wind_speed', 'mean_wind_speed',
	'max_guest_speed', 'precipitation', 'cloud_cover', 'events', 'wind_dir'
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def max_value():
	value = None
	date_str = None

	def update_value(t, date):
		nonlocal value, date_str		
		if value is None or t > value:
			value = t
			date_str = date

	def get_value():
		return value,date_str

	return update_value,get_value

def min_value():
	value = None
	date_str = None

	def update_value(t, date):
		nonlocal value, date_str		
		if value is None or t < value:
			value = t
			date_str = date

	def get_value():
		return value,date_str

	return update_value,get_value

def mean_value():
	value = 0
	count = 0

	def update_value(t):
		nonlocal value, count	
		value += t
		count += 1

	def get_value():
		return value / count

	return update_value,get_value

def generate_file_names(query_str):
	lst = query_str.split('/')
	size = len(lst)
	file_list = []

	if size == 1:
		year = lst[0]
		for m in _months:
			file_list.append(
				_file_prefix + year + '_' + m[:3] + _data_file_ext)
	elif size == 2:
		year = lst[0]
		month = int(lst[1])
		file_list.append(
			_file_prefix + year + '_' + _months[month-1][:3] + _data_file_ext)

	return file_list

def read_file_line(f):
	# ignore file header			
	f.readline()
	for line in f:
		yield line.rstrip('\n')
	
	f.close()

def open_file(file_name):
	try:
		f = open(file_name, 'r')
		return read_file_line(f)

	except FileNotFoundError as e:
#		print(str(e))
		return False

def get_day_name(date):
	lst = date.split('-')
	month = int(lst[1]) - 1
	day = lst[2]
	return '{} {}'.format(_months[month], day)

# for a given year calculate
# highest temperature and day,
# lowest temperature and day,
# most humid day and humidity.
def yearly_report(dir_path, query_str):
	file_list = generate_file_names(query_str)

	# create objects from closure functions
	# that will be used below.
	update_max_temp, get_max_temp = max_value()
	update_min_temp, get_min_temp = min_value()
	update_max_humidity, get_max_humidity = max_value()

	# get index of desired values in comma seperated
	# file line.
	date_index = _file_columns.index('date')
	max_temp_index = _file_columns.index('max_temperature')
	min_temp_index = _file_columns.index('min_temperature')
	max_humidity_index = _file_columns.index('max_humidity')

	# check all files of requested year
	for file_name in file_list:
		file_path = os_path.join(dir_path, file_name)	
		file_obj = open_file(file_path)
		if not file_obj:
			continue

		# go through file
		for line in file_obj:
			points = line.split(',')

			d = points[date_index]		
			max_t = points[max_temp_index]
			min_t = points[min_temp_index]
			max_h = points[max_humidity_index]

			if max_t:
				update_max_temp(int(max_t), d)
			if min_t:
				update_min_temp(int(min_t), d)
			if max_h:
				update_max_humidity(int(max_h), d)

	value, date = get_max_temp()
	print('Highest: {:.2f}C on {}'.format(value, get_day_name(date)))

	value, date = get_min_temp()
	print('Lowest: {:.2f}C on {}'.format(value, get_day_name(date)))

	value, date = get_max_humidity()
	print('Humidity: {:.2f}% on {}'.format(value, get_day_name(date)))


# for a given month calculate
# average highest temperature,
# average lowest temperature
# and average mean humidity.
def monthly_report(dir_path, query_str):
	file_name = generate_file_names(query_str)[0]	
	file_path = os_path.join(dir_path, file_name)	
	file_obj = open_file(file_path)
	if not file_obj:
		print('file not available: %s' %file_path)
		return

	# create objects from closure functions
	# that will be used below.
	update_avg_max_temp, get_avg_max_temp = mean_value()
	update_avg_min_temp, get_avg_min_temp = mean_value()
	update_avg_mean_humidity, get_avg_mean_humidity = mean_value()

	# get index of desired values in comma seperated
	# file line.
	date_index = _file_columns.index('date')
	max_temp_index = _file_columns.index('max_temperature')
	min_temp_index = _file_columns.index('min_temperature')
	mean_humidity_index = _file_columns.index('mean_humidity')

	# go through file
	for line in file_obj:
		points = line.split(',')

		d = points[date_index]		
		max_t = points[max_temp_index]
		min_t = points[min_temp_index]
		mean_h = points[mean_humidity_index]

		if max_t:
			update_avg_max_temp(int(max_t))
		if min_t:
			update_avg_min_temp(int(min_t))
		if	mean_h:
			update_avg_mean_humidity(int(mean_h))

	print('Highest Average: {:.2f}C'.format(get_avg_max_temp()))
	print('Lowest Average: {:.2f}C'.format(get_avg_min_temp()))
	print('Average Mean Humidity: {:.2f}%'.format(get_avg_mean_humidity()))

def draw_chart(value, color):
	# change it for color
	if color == 'red':
		use_color = bcolors.FAIL
	elif color == 'blue':
		use_color = bcolors.OKBLUE
	
	text = '{}'.format('+' * value)
	print(use_color + text + bcolors.ENDC, end='')

def two_row_chart(day_no, max_t, min_t):
	if max_t:
		print(day_no, end=' ')
		draw_chart(int(max_t), 'red')
		print(' {}C'.format(int(max_t)))

	if min_t:
		print(day_no, end=' ')
		draw_chart(int(min_t), 'blue')
		print(' {}C'.format(int(min_t)))

def one_row_chart(day_no, max_t, min_t):
	if max_t and min_t:	
		print(day_no, end=' ')	
		draw_chart(int(min_t), 'blue')		
		draw_chart(int(max_t), 'red')
		print(' {}C - {}C'.format(int(min_t), int(max_t)))

# for a given month draw two horizontal
# bar charts for each day.
def monthly_double_bar_chart(dir_path, query_str, chart_type):
	file_name = generate_file_names(query_str)[0]	
	file_path = os_path.join(dir_path, file_name)	
	file_obj = open_file(file_path)
	if not file_obj:
		print('file not available: %s' %file_path)
		return

	# get index of desired values in comma seperated
	# file line.
	date_index = _file_columns.index('date')
	max_temp_index = _file_columns.index('max_temperature')
	min_temp_index = _file_columns.index('min_temperature')

	# print month_name and year	
	lst = query_str.split('/')
	m = int(lst[1])-1
	print('{} {}'.format(_months[m], lst[0]))

	# go through file
	for line in file_obj:
		points = line.split(',')

		d = points[date_index]		
		max_t = points[max_temp_index]
		min_t = points[min_temp_index]

		day_no = '{0:02d}'.format(int(d.split('-')[2]))

		if chart_type == 'double':
			two_row_chart(day_no, max_t, min_t)
		elif chart_type == 'single':
			one_row_chart(day_no, max_t, min_t)

def generate_report(dir_path, query):
	key = query[0]
	value = query[1]

	if key == '-e':
		yearly_report(dir_path, value)
	elif key == '-a':
		monthly_report(dir_path, value)
	elif key == '-c':
		monthly_double_bar_chart(dir_path, value, 'double')
	elif key == '-c1':
		monthly_double_bar_chart(dir_path, value, 'single')

def check_valid_year(year):
	try:
		year = int(year)
	except ValueError as e:
		sys_exit(str(e))
	else:
		if year > datetime.now().year or  year < 1970:
			sys_exit('invalid or out of range year: %s' %year)

def check_valid_month(month):
	try:
		month = int(month)
	except ValueError as e:
		sys_exit(str(e))
	else:
		if month < 1 or month > 12:
			sys_exit('invalid or out of range month: %s' %month)

def validate_arguments(tups):
	for tup in tups:
		if tup[0] == '-e':
			check_valid_year(tup[1])

		elif tup[0] in ['-a', '-c', '-c1']:
			lst = tup[1].split('/')
			if len(lst) < 2:
				sys_exit('invalid switch value: %s' %str(tup))
			check_valid_year(lst[0])
			check_valid_month(lst[1])

def parse_arguments(args):
	query_list = []
	iterator = iter(args)

	for item in iterator:
		if item not in _switches:
			return (False, 'invalid switch: %s' %item)
		try:
			query_list.append((item, next(iterator)))
		except:
			return (False, 'switches not properly used')

	return (True, query_list)

def main():	
	if len(sys_argv) < 4:
		sys_exit(_usage_error)

	# pass arguments expect file_name and directory path
	code,value = parse_arguments(sys_argv[2:])
	if not code:
		sys_exit(value)
	
	# check switch values are valid
	validate_arguments(value)

	for query in value:
		generate_report(sys_argv[1], query)


if __name__ == '__main__':
	main()
