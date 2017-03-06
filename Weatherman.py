import sys
import getopt
import csv
import calendar
import glob


# reading the files needed for the user requirement and maintaining a record

def read_files(argument):

    if len(argument) == 4:
        data_list = []
        for name in glob.glob('weatherfiles/weatherfiles/Murree_weather_' + argument + '*.txt'):
            with open(name) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if 'PKST' in row.keys():
                        row['PKT'] = row['PKST']
                        del row['PKST']
                    data_list.append(row)


    elif len(argument) > 5:
        date_details = argument.split("/")
        temporary = calendar.month_abbr[int(date_details[1])]

        data_list = []
        with open('weatherfiles/weatherfiles/Murree_weather_' + date_details[0] + '_' + temporary + '.txt') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if 'PKST' in row.keys():
                    row['PKT'] = row['PKST']
                    del row['PKST']
                data_list.append(row)

    return data_list

# extracting the required fields e.g temperature and humidity from the records.

def extracting_required_fields(data):

    max_temp_seq = [x['Max TemperatureC'] for x in data]
    min_temp_seq = [x['Min TemperatureC'] for x in data]
    max_hum_seq = [x['Max Humidity'] for x in data]
    mean_humid_seq = [x[' Mean Humidity'] for x in data]
    day = [x['PKT'] for x in data]

    # ensuring all non numerical values are ignored

    max_temp_seq = [x for x in max_temp_seq if (x.isdigit())]
    min_temp_seq = [x for x in min_temp_seq if (x.isdigit())]
    mean_humid_seq = [x for x in mean_humid_seq if (x.isdigit())]
    max_hum_seq = [x for x in max_hum_seq if (x.isdigit())]

    # converting strings to inr for math operations

    max_temp_seq = list(map(int, max_temp_seq))
    min_temp_seq = list(map(int, min_temp_seq))
    mean_humid_seq = list(map(int, mean_humid_seq))
    max_hum_seq = list(map(int, max_hum_seq))

    # returning tuples

    return max_temp_seq, min_temp_seq, max_hum_seq, mean_humid_seq, day

# dividing date into separate values of day month and year

def dividing_date(date):

    date = date.split("-")
    day = date[2]
    year = date[0]
    month = calendar.month_abbr[int(date[1])]

    return day, month, year


# calculating yearly summary of max temp, min temp and max humidiity

def year_info(arg):

    # reading files needed
    data_list = read_files(arg)

    # extratcing information required
    max_temp_seq, min_temp_seq, max_hum_seq, mean_humid_seq, day = extracting_required_fields(data_list)

    # getting the result and converting to string for printing
    max_temp = str(max(max_temp_seq))
    min_temp = str(min(min_temp_seq))
    max_humid = str(max(max_hum_seq))

    #  initiailizing so that no exception is thrown in case if statement never goes true
    max_temp_date = "no date"
    max_humid_date = "no date"
    min_temp_date = "no date"

    # retrieving date for a max, min temp and max humid day
    for row in data_list:
        if row['Max TemperatureC'] == max_temp:
            max_temp_date = row['PKT']
        if row['Max Humidity'] == max_humid:
            max_humid_date = row['PKT']
        if row['Min TemperatureC'] == min_temp:
            min_temp_date = row['PKT']

    # dividing date and printing as required
    day, month, year = dividing_date(max_temp_date)
    print("Highest : " + max_temp + "C on " + month + " " + day)

    day, month, year = dividing_date(min_temp_date)
    print("Lowest : " + min_temp + "C on " + month + " " + day)

    day, month, year = dividing_date(max_humid_date)
    print("Humidity : " + max_humid + "% on " + month + " " + day)

    print("")
    print("")


def month_info(arg):

    # reading files needed
    data_list = read_files(arg)

    # extratcing information required
    max_temp_seq, min_temp_seq, max_hum_seq, mean_humid_seq, day = extracting_required_fields(data_list)

    # calculating averages
    ave_max_temp = int(sum(max_temp_seq) / len(max_temp_seq))
    ave_min_temp = int(sum(min_temp_seq) / len(min_temp_seq))
    ave_mean_humid = int(sum(mean_humid_seq) / len(mean_humid_seq))

    # printing as required
    print("Highest Temperature Average : " + str(ave_max_temp) + "C")
    print("Lowest Temperature Average : " + str(ave_min_temp) + "C")
    print("Average Mean humidity : " + str(ave_mean_humid) + "%")

    print("")
    print("")


def month_graph(arg):

    # reading files needed
    data_list = read_files(arg)

    # extratcing information required
    max_temp_seq, min_temp_seq, max_hum_seq, mean_humid_seq, day = extracting_required_fields(data_list)

    # extracting the day from the date for the whle list
    day = [d.rpartition('-')[2] for d in day]

    i = 0
    # string to be printed
    symbol_str = "+"

    #  colors for graphs
    red = '\033[91m'
    blue = '\033[94m'
    grey = '\033[37m'

    # printing bar for each day in the month
    for d in day:
        print(d + " " + blue + symbol_str * min_temp_seq[i] + red + symbol_str * (
            max_temp_seq[i] - min_temp_seq[i]) + grey + "  " + str(min_temp_seq[i]) + "-" + str(max_temp_seq[i]) + "C")
        i += 1
    print("")
    print("")


def main(argv):

    # for testing
    # year_info("2008")
    # month_graph("2008/7")
    # month_info("2008/7")

    try:
        # ensuring that each option is followed by a parameter
        options, args = getopt.getopt(argv, "e:a:c:")
    except getopt.GetoptError:
        print('error please follow this format test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    try:
        # loop for each partition
        for opt, arg in options:
            if opt == '-e':
                year_info(arg)
            elif opt == '-a':
                month_info(arg)
            elif opt == '-c':
                month_graph(arg)
    except:
        print('please ensure that the input format is correct')

if __name__ == "__main__":
    main(sys.argv[1:])
