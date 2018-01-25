import datetime
import constants


class Colors:
    PURPULE = '\033[94m'
    BLUE = '\033[36m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class WeatherReport:
    """ class take a caclulation list of data to generate a report"""
    def __init__(self, result_record, arg_type, year="", month="", isbonus = 0):
        self.arg_type = arg_type
        self.month = month
        self.year = year
        self.result_record = result_record
        self.report = {}
        self.isbonus = isbonus

    def get_date(self, datestr):
        date = str(datestr).split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def generate_report(self):
        if self.arg_type == constants.YEAR:
            self.year_report()
        if self.arg_type == constants.MONTH:
            self.month_report()
        if self.arg_type == constants.MONTHCHART:
            self.month_chart_report()

    def year_report(self):
        if self.result_record['max_temp']:
            self.report['max_temp'] = int(self.result_record['max_temp'][constants.MAX_TEMPERATURE_C])
            self.report['max_temp_date'] = self.result_record['max_temp'][constants.PKT]
        if self.result_record['min_temp']:
            self.report['min_temp'] = int(self.result_record['min_temp'][constants.MIN_TEMPERATURE_C])
            self.report['min_temp_date'] = self.result_record['min_temp'][constants.PKT]
        if self.result_record['most_humidity']:
            self.report['most_humidity'] = int(self.result_record['most_humidity'][constants.MAX_HUMIDITY])
            self.report['most_humidity_date'] = self.result_record['most_humidity'][constants.PKT]

    def month_report(self):
        if self.result_record:
            self.report = self.result_record

    def month_chart_report(self):
        max_temp_record = {}
        min_temp_record = {}
        if self.result_record['max_temp_data']:
            for dict in self.result_record['max_temp_data']:
                temp = int(dict[constants.MAX_TEMPERATURE_C])
                date = str(dict[constants.PKT]).split('-')
                max_temp_record[int(date[2])] = temp
        if self.result_record['min_temp_data']:
            for dict in self.result_record['min_temp_data']:
                temp = int(dict[constants.MIN_TEMPERATURE_C])
                date = str(dict[constants.PKT]).split('-')
                min_temp_record[int(date[2])] = temp
        self.report['max_temp_record'] = max_temp_record
        self.report['min_temp_record'] = min_temp_record

    def print_report(self):
        if self.arg_type == constants.YEAR:
            date = self.get_date(self.report['max_temp_date'])
            print("Higgest: %dC %s" % (self.report['max_temp'], date.strftime("%B %d")))
            date = self.get_date(self.report['min_temp_date'])
            print("Lowest: %dC %s" % (self.report['min_temp'], date.strftime("%B %d")))
            date = self.get_date(self.report['most_humidity_date'])
            print("Humidity: %d%% %s" % (self.report['most_humidity'], date.strftime("%B %d")))

        elif self.arg_type == constants.MONTH:
            print("Higest Average: %dC" % self.report['avg_max_temp'])
            print("Lowest Average: %dC" % self.report['avg_min_temp'])
            print("Average Mean Humidity: %d%%" % self.report['avg_mean_humidity'])

        elif self.arg_type == constants.MONTHCHART and self.isbonus:
            print(self.month + "\t" + self.year)
            for x in range(1, 32):
                max = x in self.report['max_temp_record']
                min = x in self.report['min_temp_record']
                if max:
                    temp = self.report['max_temp_record'][x]
                    print(Colors.PURPULE + str(x) +
                          Colors.BLUE + "+" * temp +
                          Colors.ENDC, end="")
                if min:
                    if not max:
                        print(Colors.PURPULE + str(x) + Colors.ENDC, end="")
                    temp = self.report['min_temp_record'][x]
                    print(Colors.RED + "+" * temp +
                          Colors.ENDC, end="")
                if max and min:
                    max_temp = self.report['max_temp_record'][x]
                    min_temp = self.report['min_temp_record'][x]
                    print(Colors.PURPULE + "%dC-%dC" % (min_temp, max_temp) + Colors.ENDC)

                elif max:
                    max_temp = self.report['max_temp_record'][x]
                    print(Colors.PURPULE + "%dC" % (max_temp) + Colors.ENDC)

                elif min:
                    min_temp = self.report['min_temp_record'][x]
                    print(Colors.PURPULE + "%dC" % (min_temp) + Colors.ENDC)

        elif self.arg_type == constants.MONTHCHART:
            print(self.month + "\t" + self.year)
            for x in range(1, 32):
                if x in self.report['max_temp_record']:
                    temp = self.report['max_temp_record'][x]
                    print(Colors.PURPULE + str(x) +
                          Colors.BLUE + "+" * temp +
                          Colors.PURPULE + "%dC" % temp +
                          Colors.ENDC)
                if x in self.report['min_temp_record']:
                    temp = self.report['min_temp_record'][x]
                    print(Colors.PURPULE + str(x) +
                          Colors.RED + "+" * temp +
                          Colors.PURPULE + "%dC" % temp +
                          Colors.ENDC)
