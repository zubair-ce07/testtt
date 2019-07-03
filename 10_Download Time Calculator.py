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


def download_time(filesize, fileUnit, BandWidth, BandWiddthUnit):
    if fileUnit is 'kb':
        filesize *= 2 ** 10
    elif fileUnit is 'kB':
        filesize *= 2 ** 13
    elif fileUnit is 'Mb':
        filesize *= 2 ** 20
    elif fileUnit is 'MB':
        filesize *= 2 ** 23
    elif fileUnit is 'Gb':
        filesize *= 2 ** 30
    elif fileUnit is 'GB':
        filesize *= 2 ** 33
    elif fileUnit is 'Tb':
        filesize *= 2 ** 40
    elif fileUnit is 'TB':
        filesize *= 2 ** 43

    if BandWiddthUnit is 'kb':
        BandWidth *= 2 ** 10
    elif BandWiddthUnit is 'kB':
        BandWidth *= 2 ** 13
    elif BandWiddthUnit is 'Mb':
        BandWidth *= 2 ** 20
    elif BandWiddthUnit is 'MB':
        BandWidth *= 2 ** 23
    elif fileUnit is 'Gb':
        filesize *= 2 ** 30
    elif fileUnit is 'GB':
        filesize *= 2 ** 33
    elif fileUnit is 'Tb':
        filesize *= 2 ** 40
    elif fileUnit is 'TB':
        filesize *= 2 ** 43

    print(filesize, BandWidth)
    print(fileUnit, BandWiddthUnit)
    time = filesize / BandWidth
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
