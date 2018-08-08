import glob  # library for getting files from selected directory
from models.YearlyWeatherData import YearlyWeatherData
from models.WeatherEntity import WeatherEntity


class Parser:
    __files = []

    def __init__(self, path):
        self.path = path
        # getting (.txt) files from DIR and saving it in __files
        Parser.__files = glob.glob("{}/*.txt".format(self.path))

    @staticmethod
    def read():
        for file in Parser.__files:
            opened_file = open(file, 'r')  # opening file
            # separating month and year
            file_name = file.split('/')[-1].split('_')
            month, year = file_name[3].split('.')[0], file_name[2]

            line = opened_file.readline()
            while line:
                line = opened_file.readline()
                WeatherEntity(line)
                # read complete file, populate data in array
                # after reading populate in parent array in following format
                # {'year' => {'month' => [entries]}}
            YearlyWeatherData(year, month, WeatherEntity.get_data())
            WeatherEntity.clear()  # Once populated clear data
