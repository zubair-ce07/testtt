import glob  # library for getting files from selected directory

from weather_data import WeatherData


class Parser:
    __files = []

    def __init__(self, path):
        self.path = path
        # getting (.txt) files from DIR and saving it in __files
        Parser.__files = glob.glob("{}/*.txt".format(self.path))
        print('reading files from {0}'.format(self.path))

    @staticmethod
    def get_files():
        return Parser.__files

    @staticmethod
    def read():
        if len(Parser.__files) == 0:
            print("No files found")
            return
        else:
            for file in Parser.__files:
                # return if there is any problem with files
                if not str(file).find('Murree'):
                    print(file, "Violates file structure")
                    return
                opened_file = open(file, 'r')  # opening file
                # separating month and year
                file_name = file.split('/')[-1].split('_')
                month, year = file_name[3].split('.')[0], file_name[2]

                line = opened_file.readline()
                WeatherData(year)
                while line:
                    line = opened_file.readline()
                    WeatherData.append_single_list(line)
                WeatherData.add_array_to_key({month: []}, month, year,  WeatherData.single_list)
                WeatherData.single_list = []  # Once populated clear data
        print("Files successfully populated")
