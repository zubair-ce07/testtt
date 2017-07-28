""" Task 1 assigned my Hamza Gul.
Looking into git, basic Python, and csv data
manipulation using Python
"""
import csv
from collections import OrderedDict
from collections import Counter
from operator import itemgetter
from record import Record
from record import mean


class CSV:
    """ Class to manipulate the CSV document """

    def __init__(self, file_name):
        """ Constructor

        Keyword arguments:
        file_name -- name/path of csv file to read
        """
        input_file = csv.DictReader(open(file_name))
        self.record_list = []
        for row in input_file:
            new_record = Record(row['date'],
                                row['max_temp'],
                                row['mean_temp'],
                                row['min_temp'],
                                row['max_dew'],
                                row['mean_dew'],
                                row['min_dew'],
                                row['max_humidity'],
                                row['mean_humidity'],
                                row['min_humidity'],
                                row['max_sea_pressure'],
                                row['mean_sea_pressure'],
                                row['min_sea_pressure'],
                                row['max_visibility'],
                                row['mean_visibility'],
                                row['min_visibility'],
                                row['max_wind_speed'],
                                row['mean_wind_speed'],
                                row['max_gust_speed'],
                                row['precipitation'],
                                row['cloud_cover'],
                                row['events'],
                                row['wind_direction'])
            self.record_list.append(new_record)

    def get_data(self, *args, **kwargs):
        """ gets summary data for each attribute in args and then writes
            the data to file_name in kwargs
        """

        if 'file_name' in kwargs:
            file_name = kwargs['file_name']
        else:
            file_name = 'output.txt'
        the_file = open(file_name, 'w')
        for arg in args:
            try:
                max_value = max(getattr(record, 'max_%s' % arg)
                                for record in self.record_list)
                max_date = max(record.date for record in self.record_list
                               if getattr(record, 'max_%s' % arg) == max_value)
                mean_value = int(mean(list(getattr(record, 'mean_%s' % arg)
                                           for record in self.record_list)))
                min_value = min(getattr(record, 'min_%s' % arg)
                                for record in self.record_list)
                min_date = min(record.date for record in self.record_list
                               if getattr(record, 'min_%s' % arg) == min_value)

                the_file.write(str("For " + arg + ":\n").upper())
                the_file.write("Maximum value was {:d} on {}\n".format(
                    max_value, max_date))
                the_file.write("Mean temperature was {:d}\n".format(
                    mean_value))
                the_file.write("Minimum temperature was {:d} on {}\n".format(
                    min_value, min_date))
                #######################################################
                max_list = [getattr(record, 'max_%s' % arg)
                            for record in self.record_list]
                min_list = [getattr(record, 'min_%s' % arg)
                            for record in self.record_list]
                max_list = sorted(Counter(max_list).items(),
                                  key=itemgetter(0), reverse=True)
                min_list = sorted(Counter(min_list).items(), key=itemgetter(0))

                the_file.write("The 10 Maximum values recorded were:\n")
                for i in range(10):
                    value_date = max_list[i]
                    if int(value_date[1]) == 1:
                        the_file.write("{0}: on {1}\n".format(
                            value_date[0], max(
                                record.date for record in self.record_list
                                if getattr(record, 'max_%s' % arg) == value_date[0])))
                    else:
                        the_file.write("{0}: on {1} days\n".format(
                            value_date[0], value_date[1]))
                the_file.write("The 10 Minimum values recorded were:\n")
                for i in range(10):
                    value_date = min_list[i]
                    if int(value_date[1]) == 1:
                        the_file.write("{0}: on {1}\n".format(
                            value_date[0], max(
                                record.date for record in self.record_list
                                if getattr(record, 'min_%s' % arg) == value_date[0])))
                    else:
                        the_file.write("{0}: on {1} days\n".format(
                            value_date[0], value_date[1]))
                the_file.write('\n')
            except AttributeError:
                error = "Attribute %s is not a part of the data set" % arg
                # the_file.write(error)
                print(error)
        the_file.close()


def main():
    """ main function """
    csv_reader = CSV('madrid.csv')
    csv_reader.get_data('temp', 'sea_pre2ssure', 'dew',
                        'visibility', file_name='output.txt')
    # csv_reader.write_summary_to_file('output.txt')


if __name__ == "__main__":
    main()
