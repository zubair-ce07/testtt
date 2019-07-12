# coding: utf-8

# Write a procedure download_time which takes as inputs a file size, the
# units that file size is given in, bandwidth and the units for
# bandwidth (excluding per second) and returns the time taken to download
# the file.
# Your answer should be a string in the form
# "<number> hours, <number> minutes, <number> seconds"

# Some information you might find useful is the number of bits
# in kilobits (kb), kilobytes (kB), megabits (Mb), megabytes (MB),
# gigabits (Gb), gigabytes (GB) and terabits (Tb), terabytes (TB).

# print 2 ** 10      # one kilobit, kb
# print 2 ** 10 * 8  # one kilobyte, kB

# print 2 ** 20      # one megabit, Mb
# print 2 ** 20 * 8  # one megabyte, MB

# print 2 ** 30      # one gigabit, Gb
# print 2 ** 30 * 8  # one gigabyte, GB

# print 2 ** 40      # one terabit, Tb
# print 2 ** 40 * 8  # one terabyte, TB

# Often bandwidth is given in megabits (Mb) per second whereas file size
# is given in megabytes (MB).
from math import exp


def convert_seconds(number):
    secs = number % 60
    mins = int(number / 60) % 60
    hours = int(number / 3600) % 60
    hour_str = str(hours) + " hour"
    if hours > 1 or hours == 0:
        hour_str += 's'

    min_str = str(mins) + " minute"
    if mins > 1 or mins == 0:
        min_str += 's'

    sec_str = str(secs) + " second"
    if secs > 1 or secs == 0:
        sec_str += 's'
    return hour_str + ' ' + min_str + ' ' + sec_str


def download_time(file_size, file_unit, bandwidth, bandwidth_unit):
    units = {
        'kb': 2 ** 10,
        'kB': 2 ** 13,
        'Mb': 2 ** 20,
        'MB': 2 ** 23,
        'Gb': 2 ** 30,
        'GB': 2 ** 33,
        'Tb': 2 ** 40,
        'TB': 2 ** 43,
    }
    file_size *= units[file_unit]
    bandwidth *= units[bandwidth_unit]
    time = file_size / bandwidth
    return convert_seconds(time)


print(download_time(1024, 'kB', 1, 'MB'))
# >>> 0 hours, 0 minutes, 1 second

print(download_time(1024, 'kB', 1, 'Mb'))
# >>> 0 hours, 0 minutes, 8 seconds  # 8.0 seconds is also acceptable

print(download_time(13, 'GB', 5.6, 'MB'))
# >>> 0 hours, 39 minutes, 37.1428571429 seconds

print(download_time(13, 'GB', 5.6, 'Mb'))
# >>> 5 hours, 16 minutes, 57.1428571429 seconds

print(download_time(10, 'MB', 2, 'kB'))
# >>> 1 hour, 25 minutes, 20 seconds  # 20.0 seconds is also acceptable

print(download_time(10, 'MB', 2, 'kb'))
# >>> 11 hours, 22 minutes, 40 seconds  # 40.0 seconds is also acceptable
