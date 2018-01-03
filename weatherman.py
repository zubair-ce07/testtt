import argparse
import helper.common as Common
from controller.weatherman import WeatherMan as WM

Parser = argparse.ArgumentParser()

Parser.add_argument("-e", "--temprange", action="store_true")
Parser.add_argument("-a", "--avgtemp", action="store_true")
Parser.add_argument("-c", "--tempchart", action="store_true")
Parser.add_argument("-ca", "--drawmultiplebars", action="store_true")
Parser.add_argument("date")
Parser.add_argument("directory")

Args = Parser.parse_args()
CSVData = Common.read_file_data(Args.directory)

Weatherman = WM()

if Args.temprange:
    Weatherman.temperature_range(Args.date, CSVData)
elif Args.avgtemp:
    Weatherman.avg_temp(Args.date, CSVData)
elif Args.tempchart:
    Weatherman.temp_chart(Args.date, CSVData)
elif Args.drawmultiplebars:
    Weatherman.draw_multiple_bars(Args.date, CSVData)
else:
    print ("Please enter valid Feature Parameter")