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
                        highest_temp = 0
                        htd = ""
                        # highest_temp_date
                        lowest_temp = 100
                        ltd = ""
                        # lowest_temp_date
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
                            if highest_temp < max_temp:
                                highest_temp = max_temp
                                htd = d
                            if lowest_temp > min_temp:
                                lowest_temp = min_temp
                                ltd = d
                        if days_in_month > 0:
                            max_temp_avg = max_temp_sum / days_in_month
                            min_temp_avg = min_temp_sum / days_in_month
                            self.__monthly_avg_temp.append((d[0], d[1], round(max_temp_avg), round(min_temp_avg)))
                            highest_temp_tuple = (htd[0], htd[1], htd[2], highest_temp)
                            for year in self.__yearly_max_temp:
                                if year[0] == htd[0]:
                                    self.__yearly_max_temp.remove(year)
                            self.__yearly_max_temp.append(highest_temp_tuple)
                            lowest_temp_tuple = (ltd[0], ltd[1], ltd[2], lowest_temp)
                            for year in self.__yearly_min_temp:
                                if year[0] == ltd[0]:
                                    self.__yearly_min_temp.remove(year)
                            self.__yearly_min_temp.append(lowest_temp_tuple)
                print(file_name, "Read successful")
                file_count += 1
        print("total Files:", file_count)

    def generate_annual_reports(self):
        print("Annual max Temp and hottest day of each year")
        print(self.__yearly_max_temp, end="\n")
        print("Annual Min Temp and coldest day of each year")
        print(self.__yearly_min_temp, end="\n")

    def monthly_avg_temp_report(self, _month, _year):
        for month in self.__monthly_avg_temp:
            if month[0] == _year and month[1] == _month:
                print(" year  month  max  min")
                print(month)
                break


weather = Weather(path)
weather.monthly_avg_temp_report('12', '2000')
weather.generate_annual_reports()


