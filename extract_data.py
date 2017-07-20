import calendar
import collections
import csv
import glob


class ExtractData:
    def __init__(self):
        self.__file_names = ""
        self.__data_set = collections.defaultdict(lambda: 0)
        self.__header = []

    def get_file_names_yearly(self, files_dir, date_):
        header = []
        data_set = []
        self.__file_names = glob.glob("{0}/*{1}*.txt".format(files_dir, date_))

    def get_file_names_monthly(self, files_dir, date_):
        year, month = date_.split("/")
        month_name_ = calendar.month_name[int(month)]
        month_name_ = month_name_[:3]
        sub_string = year + "_" + month_name_
        self.__file_names = glob.glob("{0}/*{1}.txt".format(files_dir, sub_string))

    def read_data(self):
        list = []
        for f in self.__file_names:
            with open(f, 'rt') as csvfile:
                reader = csv.DictReader(csvfile)
                self.__header = reader.fieldnames
                x = [[] for i in range(len(self.__header))]
                list = x
                for row in reader:
                    for i in range(0, len(self.__header)):
                        list[i].append(row[self.__header[i]])
        for i in range(0, len(self.__header)):
            self.__data_set[self.__header[i]] = list[i]

        return self.__data_set
