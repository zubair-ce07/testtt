import glob  # library for getting files from selected directory
from weather_data import WeatherData


class WeatherFilesParser:
    """
    Reads files from directory given from command line and saves it weather_txt_files
    read each file line by line and pass year, month and data to WeatherData
    """
    weather_txt_files = []

    def __init__(self, path):
        """
        :param path: path entered by user
        using library glob extract only .txt files from self.path
        saving files to weather_txt_files
        """
        self.path = path
        WeatherFilesParser.weather_txt_files = glob.glob(f"{self.path}/*.txt")
        print(f'reading files from {self.path}')

    @staticmethod
    def read():
        """
        reads weather files, if no specific files found then returns
        otherwise, open each file one by one and populate its data to master data structure
        :return:
        """
        if len(WeatherFilesParser.weather_txt_files) == 0:
            print("No files found")
            return
        else:
            for file in WeatherFilesParser.weather_txt_files:
                if not str(file).find('Murree'):  # return if there is any problem with files
                    print(f"{file} Violates file structure")
                    return
                opened_file = open(file, 'r')  # opening file
                file_name = file.split('/')[-1].split('_')  # separating month and year
                month, year = file_name[3].split('.')[0], file_name[2]

                line = opened_file.readline()
                WeatherData(year)
                while line:
                    line = opened_file.readline()
                    WeatherData.append_single_list(line)

                WeatherData.append_month_to_year(month, year, WeatherData.single_month_weather_list)
                WeatherData.single_month_weather_list = []  # Once populated clear data
        print("Files successfully populated")
