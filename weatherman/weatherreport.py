import datetime
import constants


class colors:
    PURPULE = '\033[94m'
    BLUE = '\033[36m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class Weathereport:
    """ class take a caclulation list of data to generate a report"""
    def __init__(self, resultdict, arg_type, year="", month="", isbonus = 0):
        self.arg_type = arg_type
        self.month = month
        self.year = year
        self.resultdict = resultdict
        self.report = {}
        self.isbonus = isbonus

    def getDate(self, datestr):
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
        if self.resultdict['max_temp']:
            self.report['max_temp'] = int(self.resultdict['max_temp'][constants.MAX_TEMPERATURE_C])
            self.report['max_temp_date'] = self.resultdict['max_temp'][constants.PKT]
        if self.resultdict['min_temp']:
            self.report['min_temp'] = int(self.resultdict['min_temp'][constants.MIN_TEMPERATURE_C])
            self.report['min_temp_date'] = self.resultdict['min_temp'][constants.PKT]
        if self.resultdict['most_humidity']:
            self.report['most_humidity'] = int(self.resultdict['most_humidity'][constants.MAX_HUMIDITY])
            self.report['most_humidity_date'] = self.resultdict['most_humidity'][constants.PKT]

    def month_report(self):
        if self.resultdict:
            self.report = self.resultdict

    def month_chart_report(self):
        max_temp_dict = {}
        min_temp_dict= {}
        if self.resultdict['max_temp_list']:
            for dict in self.resultdict['max_temp_list']:
                temp = int(dict[constants.MAX_TEMPERATURE_C])
                date = str(dict[constants.PKT]).split('-')
                max_temp_dict[int(date[2])] = temp
        if self.resultdict['min_temp_list']:
            for dict in self.resultdict['min_temp_list']:
                temp = int(dict[constants.MIN_TEMPERATURE_C])
                date = str(dict[constants.PKT]).split('-')
                min_temp_dict[int(date[2])] = temp
        self.report['max_temp_dict'] = max_temp_dict
        self.report['min_temp_dict'] = min_temp_dict

    def print_report(self):
        if self.arg_type == constants.YEAR:
            date = self.getDate(self.report['max_temp_date'])
            print("Higgest: %dC %s" % (self.report['max_temp'], date.strftime("%B %d")))
            date = self.getDate(self.report['min_temp_date'])
            print("Lowest: %dC %s" % (self.report['min_temp'], date.strftime("%B %d")))
            date = self.getDate(self.report['most_humidity_date'])
            print("Humidity: %d%% %s" % (self.report['most_humidity'], date.strftime("%B %d")))

        elif self.arg_type == constants.MONTH:
            print("Higest Average: %dC" % self.report['avg_max_temp'])
            print("Lowest Average: %dC" % self.report['avg_min_temp'])
            print("Average Mean Humidity: %d%%" % self.report['avg_mean_humidity'])

        elif self.arg_type == constants.MONTHCHART and self.isbonus:
            print(self.month + "\t" + self.year)
            for x in range(1, 32):
                max = x in self.report['max_temp_dict']
                min = x in self.report['min_temp_dict']
                if max:
                    temp = self.report['max_temp_dict'][x]
                    print(colors.PURPULE + str(x) +
                          colors.BLUE + "+" * temp +
                          colors.ENDC, end="")
                if min:
                    if not max:
                        print(colors.PURPULE + str(x) +colors.ENDC, end="")
                    temp = self.report['min_temp_dict'][x]
                    print(colors.RED + "+" * temp +
                          colors.ENDC, end="")
                if max and min:
                    max_temp = self.report['max_temp_dict'][x]
                    min_temp = self.report['min_temp_dict'][x]
                    print(colors.PURPULE + "%dC-%dC" % (min_temp, max_temp) + colors.ENDC)

                elif max:
                    max_temp = self.report['max_temp_dict'][x]
                    print(colors.PURPULE + "%dC" % (max_temp) + colors.ENDC)

                elif min:
                    min_temp = self.report['min_temp_dict'][x]
                    print(colors.PURPULE + "%dC" % (min_temp) + colors.ENDC)

        elif self.arg_type == constants.MONTHCHART:
            print(self.month + "\t" + self.year)
            for x in range(1, 32):
                if x in self.report['max_temp_dict']:
                    temp = self.report['max_temp_dict'][x]
                    print(colors.PURPULE + str(x) +
                          colors.BLUE + "+" * temp +
                          colors.PURPULE + "%dC" % temp +
                          colors.ENDC)
                if x in self.report['min_temp_dict']:
                    temp = self.report['min_temp_dict'][x]
                    print(colors.PURPULE + str(x) +
                          colors.RED + "+" * temp +
                          colors.PURPULE + "%dC" % temp +
                          colors.ENDC)
