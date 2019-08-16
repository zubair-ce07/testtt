import sys

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def find_extremes(args):
    count = 0
    for month in months:
        abs_file_path = ("%s/lahore_weather_%s_%s.txt" % (args[3], args[2], month))
        try:
            input_file = open(abs_file_path, 'r')
            lines = input_file.readlines()
            input_file.close()
            lines = lines[2:len(lines)-1]
            if count < 1:
                first_day_data = lines[0].split(",")
                high_temp = first_day_data[1]
                high_temp_day = first_day_data[0]
                low_temp = first_day_data[3]
                low_temp_day = first_day_data[0]
                humidity = first_day_data[7]
                most_humid_day = first_day_data[0]
                count += 1
            for line in lines:
                day_data = line.split(",")
                if day_data[1] > high_temp:
                    high_temp = day_data[1]
                    high_temp_day = day_data[0]

                if day_data[3] != '':
                    if low_temp == '' or day_data[3] < low_temp:
                        low_temp = day_data[3]
                        low_temp_day = day_data[0]

                if day_data[7] > humidity:
                    humidity = day_data[7]
                    most_humid_day = day_data[0]
        except:
            print("%s File not found" % abs_file_path)
    if count == 0:
        print("No files found for this year in given location")
    else:
        print("\n\nHighest: %sC on %s %s"
              % (high_temp, months[int(high_temp_day.split("-")[1])], high_temp_day.split("-")[2]))
        print("Lowest: %sC on %s %s" % (low_temp, months[int(low_temp_day.split("-")[1])], low_temp_day.split("-")[2]))
        print("Humid: %sC on %s %s"
              % (humidity, months[int(most_humid_day.split("-")[1])], most_humid_day.split("-")[2]))


def calculate_averages(args):
    abs_file_path = ("%s/lahore_weather_%s_%s.txt"
                     % (args[3], args[2].split("/")[0], months[int(args[2].split("/")[1]) - 1]))
    try:
        input_file = open(abs_file_path, 'r')
        lines = input_file.readlines()
        input_file.close()
        lines = lines[2:len(lines) - 1]
        sum_high_temp = 0
        sum_low_temp = 0
        sum_humidity = 0
        for line in lines:
            day_data = line.split(",")
            sum_high_temp += int(day_data[1])
            sum_low_temp += int(day_data[3])
            sum_humidity += int(day_data[8])
        print("\n\nHighest Average: %dC" % (sum_high_temp / len(lines)))
        print("Lowest Average: %dC" % (sum_low_temp / len(lines)))
        print("Average Humidity: %dC" % (sum_humidity / len(lines)))
    except:
        print("File not found")


def display_bars(args):
    abs_file_path = ("%s/lahore_weather_%s_%s.txt" % (args[3], args[2].split("/")[0], months[int(args[2].split("/")[1]) - 1]))
    try:
        input_file = open(abs_file_path, 'r')
        lines = input_file.readlines()
        input_file.close()
        lines = lines[2:len(lines) - 1]
        print("\n\n%s %s" % (months[int(args[2].split("/")[1]) - 1], args[2].split("/")[0]))
        for line in lines:
            day_data = line.split(",")
            low_temp_str = ''
            high_temp_str = ''
            for x in range(int(day_data[3])):
                low_temp_str += '+'
            for x in range(int(day_data[1])):
                high_temp_str += '+'
            print("%s\033[0;32;40m %s\033[0;31;40m%s \033[0;37;40m%sC / %sC \n"
                  % (day_data[0], low_temp_str, high_temp_str, day_data[3], day_data[1]))
    except:
        print("File not found")


def main():
    args = sys.argv
    print(args)
    if args[1] == "-e":
        find_extremes(args)
    elif args[1] == "-a":
        calculate_averages(args)
    elif args[1] == "-c":
        display_bars(args)
    else:
        print("Operation unknown")


if __name__ == '__main__':
    main()
