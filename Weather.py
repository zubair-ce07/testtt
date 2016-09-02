import os
path = '/home/umair/PycharmProjects/weatherReporting/weatherdata'


def skip_last_line(it):
    prev = next(it)
    for item in it:
        yield prev
        prev = item


class Weather:
    __date_max_min_temp_list = []
    # year, month, day, max, min
    __monthly_avg_temp = []
    # year, month, avg_max, avg_min
    __yearly_max_temp = []
    # year, month, day, maxTemp
    __yearly_min_temp = []
    # year, month, day, minTemp

    def __init__(self, path_to_dir):
        Weather.read_data(self, path_to_dir)

    def read_data(self, path_to_dir):
        file_count = 0
        for root, dirs, files in os.walk(path_to_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path) as file:
                    if file.closed:
                        print("unable to read from:", file_name)
                        continue
                    else:
                        print("Reading From:", file_name)
                        next(file)
                        next(file)
                        days_in_month = 0
                        max_temp_sum = 0
                        min_temp_sum = 0
                        d = ""
                        for line in skip_last_line(file):
                            current_line = line.split(",")
                            if current_line[3] == "" or current_line[1] == "":
                                continue
                            min_temp = int(current_line[3])
                            max_temp = int(current_line[1])
                            d = current_line[0].split("-")
                            self.__date_max_min_temp_list.append((d[0], d[1], d[2], max_temp, min_temp))
                            max_temp_sum += max_temp
                            min_temp_sum += min_temp
                            days_in_month += 1
                        if days_in_month > 0:
                            max_temp_avg = max_temp_sum / days_in_month
                            min_temp_avg = min_temp_sum / days_in_month

                            self.__monthly_avg_temp.append((d[0], d[1], round(max_temp_avg), round(min_temp_avg)))
                print(file_name, "Read successful")
                file_count += 1
        print("total Files:", file_count)

    def generate_annual_reports(self):
        max_temp = 0
        min_temp = 100

        for day in self.__date_max_min_temp_list:
            max_flag = -1
            for year in self.__yearly_max_temp:
                if year[0] == day[0]:
                    if max_temp < int(day[3]):
                        max_temp = int(day[3])
                    temp_tuple = (day[0], day[1], day[2], max_temp)
                    year = temp_tuple
                    print("year", year)
                    print("temp", temp_tuple)
                    max_flag = 1
                    break
            if max_flag == -1:
                self.__yearly_max_temp.append((day[0], day[1], day[2], day[3]))
            min_flag = -1
            for year in self.__yearly_min_temp:
                if year[0] == day[0]:
                    if min_temp > int(day[4]):
                        min_temp = int(day[4])
                    '''year[3] = min_temp
                    year[1] = day[1]
                    year[2] = day[2]'''
                    temp_tuple = (day[0], day[1], day[2], min_temp)
                    year = temp_tuple
                    min_flag = 1
                    break
            if min_flag == -1:
                self.__yearly_min_temp.append((day[0], day[1], day[2], day[4]))
        print("max")
        print(self.__yearly_max_temp)
        print("min")
        print(self.__yearly_min_temp)

    def monthly_avg_temp_report(self, _month, _year):
        for month in self.__monthly_avg_temp:
            if month[0] == _year and month[1] == _month:
                print(" year  month  max  min")
                print(month)
                break


weather = Weather(path)
weather.monthly_avg_temp_report('10', '1998')
weather.generate_annual_reports()


