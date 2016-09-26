import os


class color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


class weathermantask:
    def part1(year_arg, pathtofile_arg):
        if 1996 <= int(year_arg) and 2011 >= int(year_arg):
            count = 0
            HighestTemp = 0
            LowestTemp = 1000
            HighestTempDay = 'none'
            LowestTempDay = 'none'
            MostHumidDay = 'none'
            MHumidity = 0

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']

            for m in months:
                my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg + '_' + m[:3] + '.txt')
                if my_file:
                    f = open(pathtofile_arg + '/lahore_weather_' + year_arg + '_' + m[:3] + '.txt', 'r+')

                    for line in f:

                        list = line.split(',')
                        if len(list) > 5 and list[0].startswith(year_arg):

                            list[1] = int(list[1]) if list[1].strip() else 0
                            list[3] = int(list[3]) if list[3].strip() else 1000
                            list[7] = int(list[7]) if list[7].strip() else 0

                            if list[1] > HighestTemp:
                                HighestTemp = list[1]
                                HighestTempDay = list[0]
                            if list[3] < LowestTemp and list[3] != 1000:
                                LowestTemp = list[3]
                                LowestTempDay = list[0]
                            if list[7] > MHumidity:
                                MHumidity = list[7]
                                MostHumidDay = list[0]

                    f.close()
                else:
                    count += 1
                    if count >= 12:
                        print("invalid file path or file does not exist")

            if HighestTemp != 0:
                yr, mn, dt = HighestTempDay.split('-')
                print("Highest: " + format(HighestTemp, '02d') + "C on " + months[int(mn) - 1] + " " + dt)
            else:
                print("Highest Temp Not Found")
            if LowestTemp != 1000:
                yr, mn, dt = LowestTempDay.split('-')
                print("Lowest: " + format(LowestTemp, '02d') + "C on " + months[int(mn) - 1] + " " + dt)
            else:
                print("Lowest Temp Not Found")
            if MHumidity != 0:
                yr, mn, dt = MostHumidDay.split('-')
                print("Humid: " + format(MHumidity, '02d') + "% on " + months[int(mn) - 1] + " " + dt)
            else:
                print("Highest Humidity Not Found")
        else:
            print('invalid year')

    def part2(year_arg, pathtofile_arg):
        year_arg = str(year_arg).replace("/", '_')
        if 1996 <= int(year_arg[:4]) and 2011 >= int(year_arg[:4]):

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
            mn = months[int(year_arg[5:]) - 1]
            my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt')

            count = 0
            ltcount = 0
            htcount = 0
            ltsum = 0
            htsum = 0
            hcount = 0
            hsum = 0

            if my_file:
                f = open(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt', 'r+')

                for line in f:
                    list = line.split(',')
                    if list[0].startswith(year_arg[:4]):
                        if list[1] != '':
                            htcount += 1
                            htsum += int(list[1])

                        if list[3] != '':
                            ltcount += 1
                            ltsum += int(list[3])

                        if list[8] != '':
                            hcount += 1
                            hsum += int(list[8])

                f.close()
            else:
                print("invalid file path or file does not exist")

            if htcount != 0:
                print("Highest Average: " + str(round(htsum / htcount, 2)) + "C")
            else:
                print("Highest Average Not Found")

            if ltcount != 0:
                print("Lowest Average: " + str(round(ltsum / ltcount, 2)) + "C")
            else:
                print("Lowest Average Not Found")

            if hcount != 0:
                print("Average Mean Humidity: " + str(round(hsum / hcount, 2)) + "%")
            else:
                print("Humidity Not Found")

        else:
            print('invalid year')

    def part3(year_arg, pathtofile_arg):
        year_arg = str(year_arg).replace("/", '_')
        if 1996 <= int(year_arg[:4]) and 2011 >= int(year_arg[:4]):

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
            mn = months[int(year_arg[5:]) - 1]
            my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt')

            print(mn + ' ' + year_arg[:4])
            if my_file:
                f = open(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt', 'r+')
                count = 1
                for line in f:
                    list = line.split(',')
                    if list[0].startswith(year_arg[:4]):
                        maxTemp = 0 if list[1] == '' else int(list[1])
                        print(color.PURPLE + format(count, '02d') + ' ' + color.RED + (
                            '+' * abs(maxTemp)) + ' ' + color.PURPLE + ('0' if list[1] == '' else list[1]) + 'C')
                        minTemp = 0 if list[3] == '' else int(list[3])

                        print(format(count, '02d') + ' ' + color.BLUE + ('+' * abs(minTemp)) + ' ' + color.PURPLE + (
                            '0' if list[3] == '' else list[3]) + 'C')
                        count += 1

                f.close()
                print(color.END)

            else:
                print("invalid file path or file does not exist")

        else:
            print('invalid year')

    def part4(year_arg, pathtofile_arg):
        """

        :param year_arg: for year and month to show data of
        :param pathtofile_arg:  path of file containing weather data
        """
        year_arg = str(year_arg).replace("/", '_')
        if 1996 <= int(year_arg[:4]) and 2011 >= int(year_arg[:4]):
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
            mn = months[int(year_arg[5:]) - 1]
            print(mn + ' ' + year_arg[:4])
            my_file = os.path.isfile(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt')

            if my_file:
                f = open(pathtofile_arg + '/lahore_weather_' + year_arg[:4] + '_' + mn[:3] + '.txt', 'r+')
                count = 1
                for line in f:
                    list = line.split(',')
                    if list[0].startswith(year_arg[:4]):
                        print(color.PURPLE + format(count, '02d') + ' ' + color.BLUE + (
                            '+' * abs(0 if list[3] == '' else int(list[3]))) + color.RED + (
                                  '+' * abs(0 if list[1] == '' else int(list[1]))) + ' ' + color.PURPLE + (
                                  '0' if list[3] == '' else list[3]) + 'C - ' + (
                              '0' if list[1] == '' else list[1]) + 'C')
                        count += 1
                f.close()
                print(color.END)

            else:
                print("invalid file path or file does not exist")

        else:
            print('invalid year')

print('part 1, for year 2002')
weathermantask.part1('2002', '/root/PycharmProjects/weatherman/weatherdata')
print('\npart 2, for month 2002/6')
weathermantask.part2('2002/6', '/root/PycharmProjects/weatherman/weatherdata')
print('\npart 3, for month 2002/6')
weathermantask.part3('2002/6', '/root/PycharmProjects/weatherman/weatherdata')
print('part 4, for month 2002/6')
weathermantask.part4('2002/6', '/root/PycharmProjects/weatherman/weatherdata')