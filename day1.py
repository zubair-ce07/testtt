#                   First week Monday
#                      Topic Covered
#   List
#   Tuple
#   Dictionary
#   String Formation
#   File Output
#   For each Loop etc

dates = list()
days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')       # Tuple
working_days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')     # Tuple

for date in range(1, 31):       # assuming i have 30days in month
    dates.append(date)

data_file = open("days.txt", "w")
day = 0
for date in dates:
    if day in working_days:
        info = dict({'Date': date, 'Day': days[day], 'Status': 'Working Day'})
        data_file.write(str(info) + "\n")
    else:
        info = dict({'Date': date, 'Day': days[day], 'Status': 'HoliDay'})
        data_file.write(str(info) + "\n")
    day += 1
    if day > 6:
        day = 0
data_file.close()
