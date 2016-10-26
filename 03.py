# TASK 1
# Weather Man
# the lab repo contains weather files for Murree.
# Write an application that generates the following reports.

# 5. BONUS TASK. For a given month draw one horizontal bar chart on the console
# for the highest and lowest temperature on each day.
# Highest in red and lowest in blue.

# weatherman.py /path/to/files-dir -c 2011/3
# March 2011
# 01 ++++++++++++++++++++++++++++++++++++ 11C - 25C
# 02 ++++++++++++++++++++++++++++++ 08C - 22C

# Purple = \033[95m
# Red = \033[91m
# End = \033[0m

year = 0
while True:
    try:
        year = int(input("year "))
        break
    except ValueError:
        print("Not an integer.")
        continue

month = input("month ")
month = month[:3].capitalize()

f = open("weatherfiles/Murree_weather_{}_{}.txt".format(year, month))

header1 = f.readline()

for index, line in enumerate(f, start=1):
    line = line.strip()
    columns = line.split(",")
    highest_temperature = int(columns[1]) if columns[1] != "" else None
    lowest_temperature = int(columns[3]) if columns[3] != "" else None
    if highest_temperature and lowest_temperature is not None:
        print("\033[95m{}\033[0m \033[94m{}\033[0m\033[91m{}\033[0m \033[95m{}C - {}C\033[0m"
              .format(index, "+" * lowest_temperature, "+" * highest_temperature, lowest_temperature,
                      highest_temperature))
    else:
        print("\033[95m{}\033[0m \033[91mDon't have any data to show on\033[0m \033[95m{}".format(index, columns[0]))

f.close()
