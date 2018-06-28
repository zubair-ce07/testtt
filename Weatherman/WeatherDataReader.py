from os import listdir
from os.path import isfile, join
import WeatherData


class WeatherDataReader:

    @staticmethod
    def read_line(line):
        dayData = WeatherData.WeatherData()
        lst = line.split(',')
        if len(lst) > 10:
            for index in range(1, 9):
                if lst[index] =='':
                    lst[index] = -100
                else:
                    lst[index] = float(lst[index])
            date = lst[0].split('-')
            dayData.year = int(date[0])
            dayData.month = int(date[1])
            dayData.day = int(date[2])
            dayData.highestT = lst[1]
            dayData.meanT = lst[2]
            dayData.lowestT = lst[3]
            dayData.meanT = lst[2]
            dayData.highestH = lst[7]
            dayData.meanH = lst[8]
            dayData.lowestH = lst[9]
            return dayData
        else:
            return []

    @staticmethod
    def read_file(path):
        lst = []
        with open(path) as data:
            text = data.read()
            split_text = text.split('\n')
            lines = list(split_text)
            for counter in range(1, len(lines)):
                line = lines[counter]
                lst.append(WeatherDataReader.read_line(line))
            return lst

    @staticmethod
    def read(path):
        data = []
        files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]
        for file_path in files:
            data.append(WeatherDataReader.read_file(path + '/' + file_path))
        return data
