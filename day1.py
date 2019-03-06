#                   First week Monday
#                      Topic Covered
#   List
#   Tuple
#   Dictionary
#   String Formation
#   File Output
#   For each Loop etc

dates = list()
data = list()
days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')  # Tuple
working_days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')  # Tuple

for date in range(1, 31):  # assuming i have 30days in month
    dates.append(date)

day = 0
for date in dates:
    if day in working_days:
        info = dict({'Date': date, 'Day': days[day], 'Status': 'Working Day'})
    else:
        info = dict({'Date': date, 'Day': days[day], 'Status': 'HoliDay'})
    data.append(info)
    day += 1
    if day > 6:
        day = 0

with open("days.txt", "wb") as data_file:
    data_file.write(str(data))
