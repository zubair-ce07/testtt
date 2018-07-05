"""Convert Seconds to hour(s),minute(s),second(s)
Write a procedure, convert_seconds, which takes as input a non-negative number of seconds and
returns a string of the form '<integer> hours, <integer> minutes, <number> seconds' but where
if <integer> is 1 for the number of hours or minutes, then it should be hour/minute
"""

import datetime


def convert_seconds(number):
    h, m, s = str(datetime.timedelta(seconds=number)).split(":")
    result = h
    result += [" hours ", " hour "][int(h) == 1]
    result += m
    result += [" minutes ", " minute "][int(m) == 1]
    result += s
    result += [" seconds ", " second "][int(float(s)) == 1]
    return result


print convert_seconds(3661)
#>>> 1 hour, 1 minute, 1 second

print convert_seconds(7325)
#>>> 2 hours, 2 minutes, 5 seconds

print convert_seconds(7261.7)
#>>> 2 hours, 1 minute, 1.7 seconds
