import os
import datetime
import sys
import argparse

def short_to_long_date(arg):
    """ Takes date (as str) in "Year/Month" format
        and returns date (as tuple) in (year, month_abbrivation_in_3_letters)
     """
    date = arg.split("/")
    year, month = date[0], datetime.date(int(date[0]), int(date[1]), 1).strftime('%B')[:3]
    return year, month

class WeathermanEntries:
    def __init__(self):
        self.entries = {}


    def set_entries(self, key, entries):
        self.entries[key] = entries


    def highest_temp(self, by = None):
        _highest_temp = 0.0
        _highest_temp_pkt = ''
        found = False

        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                max_temp = d.get('Max TemperatureC')
                if max_temp is not None and max_temp.isalnum() \
                and float(max_temp) > _highest_temp:
                    _highest_temp = float(max_temp)
                    _highest_temp_pkt = d.get('PKT') or d.get('PKST')
                    found = True
        if found:
            return (_highest_temp, _highest_temp_pkt)
        else:
            return (None, None)


    def lowest_temp(self, by = None):
        _lowest_temp = 100
        _lowest_temp_pkt = ''
        found = False

        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                min_temp = d.get('Min TemperatureC')
                if min_temp is not None and min_temp.isalnum() \
                and float(min_temp) < _lowest_temp:
                    _lowest_temp = float(min_temp)
                    _lowest_temp_pkt = d.get('PKT') or d.get('PKST')
                    found = True
        if found:
            return (_lowest_temp, _lowest_temp_pkt)
        else:
            return (None, None)


    def most_humid(self, by = None):
        _most_humid = 0
        _most_humid_pkt = ''
        found = False
        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                most_humid = d.get('Max Humidity')
                if most_humid is not None and most_humid.isalnum() \
                and float(most_humid) > _most_humid:
                    _most_humid = float(most_humid)
                    _most_humid_pkt = d.get('PKT') or d.get('PKST')
                    found = True

        if found:
            return (_most_humid, _most_humid_pkt)
        else:
            return (None, None)

    def highest_avg_temp(self, by = None):
        _highest_temp = 0.0
        _highest_temp_pkt = ''
        found = False

        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                max_temp = d.get('Max TemperatureC')
                if max_temp is not None and max_temp.isalnum() \
                and float(max_temp) > _highest_temp:
                    _highest_temp = float(max_temp)
                    _highest_temp_pkt = d.get('PKT') or d.get('PKST')
                    found = True
        if found:
            return (_highest_temp, _highest_temp_pkt)
        else:
            return (None, None)


    def lowest_avg_temp(self, by = None):
        _lowest_temp = 100
        _lowest_temp_pkt = ''
        found = False

        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                min_temp = d.get('Min TemperatureC')
                if min_temp is not None and min_temp.isalnum() \
                and float(min_temp) < _lowest_temp:
                    _lowest_temp = float(min_temp)
                    _lowest_temp_pkt = d.get('PKT') or d.get('PKST')
                    found = True
        if found:
            return (_lowest_temp, _lowest_temp_pkt)
        else:
            return (None, None)


    def avg_mean_humid(self, by = None):
        _most_humid = 0
        _most_humid_pkt = ''
        found = False
        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                most_humid = d.get('Max Humidity')
                if most_humid is not None and most_humid.isalnum() \
                and float(most_humid) > _most_humid:
                    _most_humid = float(most_humid)
                    _most_humid_pkt = d.get('PKT') or d.get('PKST')
                    found = True

        if found:
            return (_most_humid, _most_humid_pkt)
        else:
            return (None, None)
    
wmentries = WeathermanEntries()
    

class WeathermanEntry:

    def __init__(self, entry):
        self.entry = entry

    def get(self, key):
        return self.entry.get(key, None)

    def __str__(self):
        return str(self.entry)


def read_to_weatherman_entry(meta, line):
    return WeathermanEntry(dict(zip(meta, line)))


def read_file(file):
    f = open(file, "r")
    blank = f.readline().strip("\n")
    meta = f.readline().strip("\n").replace(", ", ",").split(",")
    entries = []
    for line in f.readlines():
        l = line.strip("\n").split(",");
        entries.append(read_to_weatherman_entry(meta, l))
    wmentries.set_entries(file, entries)


def main():

    parser = argparse.ArgumentParser()
    #parser.add_argument('directory')
    #parser.add_argument('dataset_folder_name', type=)
    #parser.add_argument('--input', help='input directory', required=True)
    #parser.add_argument('--path', type=dir())
    #parser.add_argument('path')

    # parser.add_argument('path', action='store', help='path of directory', type=str)
    # parser.add_argument('mode', help='path of directory', type=str)
    # parser.add_argument('yearstr', type=int, help='path of directory')
    # args = parser.parse_args()

    parser.add_argument('-p', '--path', help='path of directory', type=str)
    parser.add_argument('-m', '--mode', help='path of directory', type=str)
    parser.add_argument('-y', '--yearstr', type=str, help='path of directory')
    args = parser.parse_args()

    weatherfiles = os.listdir(args.path)

    for file in weatherfiles:
        read_file(os.path.join(args.path, file))

    if args.mode == '1':
        highest_temp = wmentries.highest_temp(args.yearstr)
        lowest_temp = wmentries.lowest_temp(args.yearstr)
        most_humid = wmentries.most_humid(args.yearstr)
        print("Highest: {}C on {}".format(highest_temp[0], highest_temp[1]))
        print("Lowest: {}C on {}".format(lowest_temp[0], lowest_temp[1]))
        print("Humidity: {} on {}".format(most_humid[0], most_humid[1]))


'''
    # #path = sys.argv[1]
    # #mode = sys.argv[2]
    #
    weatherfiles = os.listdir(args.path)
    # #weatherfiles = os.listdir(directory)
    # year = int(args.yearstr)
    #
    #
    #
    for file in weatherfiles:
    # #for file in directory:
         read_file(os.path.join(args.path, file))
    #
    if args.mode == 'a':
    #     #year = sys.argv[3]
         highest_temp = wmentries.highest_temp(args.year)
         lowest_temp = wmentries.lowest_temp(args.year)
         most_humid = wmentries.most_humid(args.year)
    #     #print("Highest:", highest_temp[0], "on", highest_temp[1])
         print("Highest: {}C on {}".format(highest_temp[0], highest_temp[1]))
         print("Lowest: {}C on {}".format(lowest_temp[0], lowest_temp[1]))
         print("Humidity: {} on {}".format(most_humid[0], most_humid[1]))
    #     #print("Lowest:", lowest_temp[0], "on", lowest_temp[1])
    #     #print("Humidity:", most_humid[0], "on", most_humid[1])
    #
    #
    '''
main()
