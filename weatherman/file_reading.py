import glob

def file_reading(dir,month,year):
    FILE_NAME = glob.glob(dir + "/*_weather_" + str(year) + "_" + str(month) + "*")
    # print(FILE_NAME)
    # print(str(month))
    # print(year)
    FILE_READER = None
    if FILE_NAME:
        FILE_READER = open(FILE_NAME[0]).readlines()[1:]

    return FILE_READER