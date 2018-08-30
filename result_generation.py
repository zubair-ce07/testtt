#!/usr/bin/python3.6
def display_results(result, operation):
    if len(result) > 2:
        if operation is 'e':
            print(
                result[3], \
                '\nHighest: ', result[0][0], 'C on ', result[0][1], result[0][2], \
                '\nLowest: ', result[1][0], 'C on ', result[1][1], result[1][2], \
                '\nHumidity: ', result[2][0], '% on ', result[2][1], result[2][2], \
                '\n-------------------------------------\n' \
            )
        elif operation is 'a':
            print(
                result[3], \
                '\nHighest Average: ', round(result[0]), 'C', \
                '\nLowest Average: ', round(result[1]),'C', \
                '\nAverage Mean Humidity: ', round(result[2]),'%', \
                '\n-------------------------------------\n' \
            )
        elif operation is 'c':
            high_temperature_list = result.get('high_temprature')
            low_temperature_list = result.get('low_temprature')
            count = 1
            for high, low in zip(high_temperature_list, low_temperature_list):
                if low is None and high is None:
                    print(count)
                elif low is None or high is None:
                    if low is None:
                        print(count, "\033[0;31;48m+"*high + "\033[0m  ", str(high) + "C")
                    if high is None:
                        print(count, "\033[0;34;48m+"*low + "\033[0m", str(low) + "C")
                else:
                    print(count, "\033[0;34;48m+"*low + "\033[0;31;48m+"*high + "\033[0m", str(low) + 'C', str(high) + 'C')
                count += 1

    else:
        print('***No such file/files***')
