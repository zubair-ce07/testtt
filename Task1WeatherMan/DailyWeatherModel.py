from termcolor import colored
from datetime import datetime


class DailyWeatherModel():
    def __init__(self, row_data):
        self.PKT                        = row_data[0]
        self.MaxTemperatureC            = row_data[1]
        self.MinTemperatureC            = row_data[2]
        self.MeanTemperatureC           = row_data[3]
        self.DewPointC                  = row_data[4]
        self.MeanDewPointC              = row_data[5]
        self.MinDewpointC               = row_data[6]
        self.MaxHumidity                = row_data[7]
        self.MeanHumidity               = row_data[8]
        self.MinHumidity                = row_data[9]
        self.MeanSeaLevelPressurehPa    = row_data[10]
        self.MaxSeaLevelPressurehPa     = row_data[11]
        self.MinSeaLevelPressurehPa     = row_data[12]
        self.MaxVisibilityKm            = row_data[13]
        self.MeanVisibilityKm           = row_data[14]
        self.MinVisibilitykM            = row_data[15]
        self.MaxWindSpeedKmPh           = row_data[16]
        self.MeanWindSpeedKmPh          = row_data[17]
        self.MaxGustSpeedKmPh           = row_data[18]
        self.Precipitationmm            = row_data[19]
        self.CloudCover                 = row_data[20]
        self.Events                     = row_data[21]
        self.WindDirDegrees             = row_data[22]

    def print_weather_info(self):
        print('PKT ', self.PKT,
              ' MaxTemperatureC ', self.MaxTemperatureC,
              ' MeanTemperatureC ', self.MeanTemperatureC,
              ' MinTemperatureC ', self.MinTemperatureC,
              ' DewPointC ', self.DewPointC,
              ' MeanDewPointC ', self.MeanDewPointC,
              ' MinDewpointC ', self.MinDewpointC,
              ' MaxHumidity ', self.MaxHumidity,
              ' MeanHumidity ', self.MeanHumidity,
              ' MinHumidity ', self.MinHumidity,
              ' MaxSeaLevelPressurehPa ', self.MaxSeaLevelPressurehPa,
              ' MeanSeaLevelPressurehPa ', self.MeanSeaLevelPressurehPa,
              ' MinSeaLevelPressurehPa ', self.MinSeaLevelPressurehPa,
              ' MaxVisibilityKm ', self.MaxVisibilityKm,
              ' MeanVisibilityKm ', self.MeanVisibilityKm,
              ' MinVisibilitykM ', self.MinVisibilitykM,
              ' MaxWindSpeedKmPh ', self.MaxWindSpeedKmPh,
              ' MeanWindSpeedKmPh ', self.MeanWindSpeedKmPh,
              ' MaxGustSpeedKmPh ', self.MaxGustSpeedKmPh,
              ' Precipitationmm ', self.Precipitationmm,
              ' CloudCover ', self.CloudCover,
              ' Events ', self.Events,
              ' WindDirDegrees ', self.WindDirDegrees
              )

    def print_chart_string(self):
        components = datetime.strptime(self.PKT, "%Y-%m-%d")
        try:
            print(str(components.day), colored('+', 'red') * int(self.MaxTemperatureC), self.MaxTemperatureC + 'C')
        except:
            print(str(components.day), colored('Data N/A', 'red'))

        try:
            print(str(components.day), colored('+', 'blue') * int(self.MinTemperatureC), self.MinTemperatureC + 'C')
        except:
            print(str(components.day), colored('Data N/A', 'blue'))
