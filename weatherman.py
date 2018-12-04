import sys
import analysis


class WeatherInformation(object):
    def __init__(
            self, date='', year='',
            month='', max_temp='', low_temp='',
            max_humid='', mean_humid=''):
        self.date = date
        self.year = year
        self.month = month
        self.max_temp = max_temp
        self.low_temp = low_temp
        self.max_humid = max_humid
        self.mean_humid = mean_humid

    def date(self):
        return self.date

    def year(self):
        return self.year

    def month(self):
        return self.month

    def max_temp(self):
        return self.max_temp

    def low_temp(self):
        return self.low_temp

    def max_humid(self):
        return self.max_humid

    def mean_humid(self):
        return self.mean_humid


class CalculationResults(object):
    def __init__(
            self, max_temp='', max_temp_day='', low_temp='',
            low_temp_day='',max_humid='',max_humid_day='', day='',
            average_max_temp='', average_low_temp='', average_mean_humid='',
            max_temp_str='', low_temp_str='', date=''):
        self.max_temp = max_temp
        self.max_temp_day = max_temp_day
        self.low_temp = low_temp
        self.low_temp_day = low_temp_day
        self.max_humid = max_humid
        self.max_humid_day = max_humid_day
        self.day = day
        self.average_max_temp = average_max_temp
        self.average_low_temp = average_low_temp
        self.average_mean_humid = average_mean_humid
        self.max_temp_str = max_temp_str
        self.low_temp_str = low_temp_str
        self.date = date

    def max_temp(self):
        return self.max_temp

    def max_temp_day(self):
        return self.max_temp_day

    def low_temp(self):
        return self.low_temp

    def low_temp_day(self):
        return self.low_temp_day

    def max_humid(self):
        return self.max_humid

    def max_humid_day(self):
        return self.max_humid_day

    def day(self):
        return self.day

    def average_max_temp(self):
        return self.average_max_temp

    def average_low_temp(self):
        return self.average_low_temp

    def average_mean_humid(self):
        return self.average_mean_humid

    def max_temp_str(self):
        return self.max_temp_str

    def low_temp_str(self):
        return self.low_temp_str


def main():

    # data_set = analysis.data_dict_preparation(sys.argv[1]+'/*.txt') # dictionary based implementation commented
    data_set = analysis.class_structured_data(sys.argv[1] + '/*.txt')

    if len(data_set) > 0:
        parameters = sys.argv[2:]
        if len(parameters) > 1 :
            for index in range(0, len(parameters), 2):
                # result = analysis.computation_dict_analysis(data_set, parameters[index:index+2])
                result = analysis.computation_analysis(data_set, parameters[index:index + 2])
                if result:
                    # analysis.dict_report_generator(parameters[index],result)
                    analysis.report_generator(parameters[index], result)
                else:
                    print('No calculation result found!')
        else:
            print('Parameters missing !')
    else:
        print('No data found!')


if __name__ == "__main__": main()
