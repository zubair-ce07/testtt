# coding: utf-8

# Write a procedure, convert_seconds, which takes as input a non-negative
# number of seconds and returns a string of the form
# '<integer> hours, <integer> minutes, <number> seconds' but
# where if <integer> is 1 for the number of hours or minutes,
# then it should be hour/minute. Further, <number> may be an integer
# or decimal, and if it is 1, then it should be followed by second.
# You might need to use int() to turn a decimal into a float depending
# on how you code this. int(3.0) gives 3
#
# Note that English uses the plural when talking about 0 items, so
# it should be "0 minutes".
#
import time


def convert_seconds(number):
    t = time.gmtime(number)
    hour_str = time.strftime("%H", t) + " hour"
    if t.tm_hour > 1:
        hour_str += 's'

    min_str = time.strftime("%M", t) + " minute"
    if t.tm_min > 1:
        min_str += 's'

    if type(number) is float:
        sec_str = str(number % 60) + " second"
    else:
        sec_str = time.strftime("%S", t) + " second"
    if t.tm_sec > 1:
        sec_str += 's'
    return hour_str + ' ' + min_str + ' ' + sec_str


print(convert_seconds(3661))
# >>> 1 hour, 1 minute, 1 second

print(convert_seconds(7325))
# >>> 2 hours, 2 minutes, 5 seconds

print(convert_seconds(7261.7))
# >>> 2 hours, 1 minute, 1.7 seconds
