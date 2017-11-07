import calendar
import os
import re
import sys


def avg(temp_list):
    return float(sum(temp_list))/len(temp_list)


def convert_date(date):
    match = re.search(r'\d+-(\d+)-(\d+)', date)
    month = calendar.month_name[int(match.group(1))]
    day = match.group(2)
    return month+" "+day


def report_a(data, year):
    all_names = os.listdir(data)
    file_names = re.findall(r'\S+'+year+'\S+', ' '.join(all_names))
    data = ''

    for text_file in file_names:
        f = open(text_file, 'rU')
        data += f.read()

    parameters1 = re.findall(r'(\d\d\d\d-\d+-\d+),(\d+),\S+,(\S+),\S+,\S+,\S+,'
                             r'(\S+),\S+,\S+,,,,\S+\s', data)
    parameters2 = re.findall(r'(\d\d\d\d-\d+-\d+),(\d+),,(\S+),\S+,\S+,\S+,'
                             r'(\S+),\S+,\S+,,,,\S+\s', data)
    dates, max_temp, min_temp, humidity = zip(*(parameters1+parameters2))
    max_temp, min_temp, = map(int, max_temp), map(int, min_temp)
    humidity = map(int, humidity)
    high_temp = max(max_temp)
    high_temp_day = dates[max_temp.index(high_temp)]
    low_temp = min(min_temp)
    low_temp_day = dates[min_temp.index(low_temp)]
    most_humid = max(humidity)
    most_humid_day = dates[humidity.index(most_humid)]

    print "Highest: "+str(high_temp)+"C on "+convert_date(high_temp_day)
    print "Lowest: "+str(low_temp)+"C on "+convert_date(low_temp_day)
    print "Humidity: "+str(most_humid)+"% on "+convert_date(most_humid_day)


def report_b(data, date):
    all_names = os.listdir(data)
    text_file = re.search(r'\S+'+date[:4]+'_'
                          + calendar.month_name[int(date[-1])][:3]
                          + '\S+', ' '.join(all_names)).group()
    f = open(text_file, 'rU')
    text = f.read()
    parameters1 = re.findall(r'\d\d\d\d-\d+-\d+,(\d+),\S+,(\S+),\S+,\S+,\S+,'
                             r'\S+,(\S+),\S+,,,,\S+\s', text)
    parameters2 = re.findall(r'\d\d\d\d-\d+-\d+,(\d+),,(\S+),\S+,\S+,\S+,\S+,'
                             r'(\S+),\S+,,,,\S+\s', text)
    max_temp, min_temp, mean_humidity = zip(*(parameters1+parameters2))
    max_temp, min_temp = map(int, max_temp), map(int, min_temp)
    mean_humidity = map(int, mean_humidity)

    print "Highest Average: " + str(avg(max_temp))+"C"
    print "Lowest Average: " + str(avg(min_temp))+"C"
    print "Average Mean Humidity: " + str(avg(mean_humidity))+"%"


def report_c(data, date):
    print calendar.month_name[int(date[-1])]+" "+date[:4]

    all_names = os.listdir(data)
    text_file = re.search(r'\S+' + date[:4]+'_'
                          + calendar.month_name[int(date[-1])][:3]
                          + '\S+', ' '.join(all_names)).group()
    f = open(text_file, 'rU')
    text = f.read()
    parameters1 = re.findall(r'\d\d\d\d-\d+-(\d+),(\d+),\S+,(\S+),\S+,\S+,\S+,'
                             r'\S+,\S+,\S+,,,,\S+\s', text)
    parameters2 = re.findall(r'\d\d\d\d-\d+-(\d+),(\d+),,(\S+),\S+,\S+,\S+,'
                             r'\S+,\S+,\S+,,,,\S+\s', text)
    parameters = sorted(parameters1+parameters2, key=lambda x: int(x[0]))

    r = "\033[31m"
    b = "\033[34m"
    w = "\033[0m"
    for day in parameters:
        if len(day[0])<2:
            date = "0"+day[0]
        else:
            date = day[0]
        print date+" "+r+("+"*int(day[1]))+b+("+"*int(day[2]))+w, day[1]+"C",\
            "-", day[2]+"C"


def main():
    path = sys.argv[1]
    for i in xrange(2, len(sys.argv), 2):
        report = sys.argv[i]
        time = sys.argv[i+1]

        if report == "-e":
            report_a(path, time)
            print ""
        elif report == "-a":
            report_b(path, time)
            print ""
        else:
            report_c(path, time)
            print ""


if __name__ == '__main__':
    main()