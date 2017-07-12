import csv
import os


class Weather:
    def __init__(self,  file_path="/home/hamza/PycharmProjects/watherfinal/weatherfiles/"):
        self.file_path = file_path
        self.files_names = os.listdir(file_path)
        self.yearly_weather_data = []
        self.y_m_weather_data = []
        self.red='\033[91m'
        self.blue='\033[94m'
        self.end='\033[0m'
    """Filter by year and read data"""

    def filter_years(self, y1):
        year_directory = []
        for years in self.files_names:
            if str(y1) in years:
                year_directory.append(years)
        for data in range(len(year_directory)):
            input_file_year = csv.DictReader(open(self.file_path + year_directory[data]))
            for row in input_file_year:
                self.yearly_weather_data.append(row)

    """Filter by year and read data"""

    def filter_year_month(self, y2, m2):
        year_month_directory = []
        for year_month in self.files_names:
            if str(y2) in year_month and m2 in year_month:
                year_month_directory.append(year_month)
        print(year_month_directory)
        for data in range(len(year_month_directory)):
            input_file_year_month = csv.DictReader(open(self.file_path + year_month_directory[data]))
            for row in input_file_year_month:
                self.y_m_weather_data.append(row)

    def max(self):
        for result in range(len(self.yearly_weather_data)):
            maxtemp = max(self.yearly_weather_data,
                          key=lambda x: int(x['Max TemperatureC']) if x['Max TemperatureC'].isdigit() else -1000)
            mintemp = min(self.yearly_weather_data,
                          key=lambda x: int(x['Min TemperatureC']) if x['Min TemperatureC'].isdigit() else 1000)
            maxhumid = max(self.yearly_weather_data,
                           key=lambda x: int(x['Max Humidity']) if x['Max Humidity'].isdigit() else -1000)
        print("Highest:{}C on {}".format(maxtemp['Max TemperatureC'], maxtemp['PKT']))
        print("Lowest:{}C on {}".format(mintemp['Min TemperatureC'], mintemp['PKT']))
        print("Humidity: {}% on {}".format(maxhumid['Max Humidity'], maxhumid['PKT']))

    def avg_weather(self):
        avgmaxt=[]
        avgmint=[]
        avgmaxhu=[]
        for result in range(len(self.y_m_weather_data)):
            avgmaxt.append(self.y_m_weather_data[result]['Max TemperatureC'])
            avgmint.append(self.y_m_weather_data[result]['Min TemperatureC'])
            avgmaxhu.append(self.y_m_weather_data[result][' Mean Humidity'])

        avgmaxt = [int(x) for x in avgmaxt if x.isdigit()]
        print("Highest average:{}C".format(sum(avgmaxt) / len(avgmaxt)))


        avgmint = [int(x) for x in avgmint if x.isdigit()]
        print("Lowest average:{}C".format(sum(avgmint) / len(avgmint)))

        avgmaxhu = [int(x) for x in avgmaxhu if x.isdigit()]

        print("Average Mean Humidity:{}%".format(sum(avgmaxhu) / len(avgmaxhu)))

    def graph(self):
        for result in range(len(self.y_m_weather_data)):
            # for max
            print(result, end=' ')
            try:
                print(self.red + '+' * int(self.y_m_weather_data[result]['Max TemperatureC']) + self.end, end='')
            except ValueError:
                continue
            print(self.y_m_weather_data[result]['Max TemperatureC'])
            # for min
            print(result, end=' ')
            try:
                print(self.blue + '+' * int(self.y_m_weather_data[result]['Min TemperatureC']) + self.end, end='')
            except ValueError:
                continue
            print(self.y_m_weather_data[result]['Min TemperatureC'])

    def bonus(self):
        for result in range(len(self.y_m_weather_data)):
            print(result, end=' ')
            try:
                print(self.blue + '+' * int(self.y_m_weather_data[result]['Min TemperatureC']) + self.end, end='')
                print(self.red + '+' * int(self.y_m_weather_data[result]['Max TemperatureC']) + self.end, end='')
            except ValueError:
                continue
            print("{min}C-{max}C".format(min=self.y_m_weather_data[result]['Min TemperatureC'],
                                         max=self.y_m_weather_data[result]['Max TemperatureC']))

while True:
    print(
        "\nMenu\n(e)Extreme weather per year\n(a)Average weather per month\n(g)For creating a graph of temperature for "
        "selected month on daily basis\n(b)for bonus task\n(Q)uit")
    choice = input(">>> ").lower().rstrip()
    if choice == "q":
        break

    elif choice == "e":
        year = input("Enter year:")
        extreme = Weather()
        extreme.filter_years(year)
        extreme.max()

    elif choice == "a":
        y = input("Enter year:")
        m = input("Enter Month:")
        a = Weather()
        a.filter_year_month(y, m)
        a.avg_weather()

    elif choice == "g":
        y = input("Enter year:")
        m = input("Enter Month:")
        g = Weather()
        g.filter_year_month(y, m)
        g.graph()
    elif choice == "b":
        y = input("Enter year:")
        m = input("Enter Month:")
        b = Weather()
        b.filter_year_month(y, m)
        b.bonus()
    else:
        print("Invalid choice, please choose again\n")
