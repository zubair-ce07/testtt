# TASK 1
# Weather Man
# the lab repo contains weather files for Murree.
# Write an application that generates the following reports.

# 1. For a given year display the highest temperature and day,
# lowest temperature and day,
# most humid day and humidity.

# weatherman.py /path/to/files-dir -e 2002
# Highest: 45C on June 23
# Lowest: 01C on December 22
# Humidity: 95% on August 14

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

highest_data = {
    "max_temperature": 1,
    "date": None
}

lowest_data = {
    "min_temperature": 100,
    "date": None
}

humidity_data = {
    "max_humidity": 1,
    "date": None
}

for line in f:
    line = line.strip()
    columns = line.split(",")

    highest_current = int(columns[1]) if columns[1] != "" else None

    if highest_current and highest_current >= highest_data["max_temperature"]:
        highest_data["max_temperature"] = highest_current
        highest_data["date"] = columns[0]

    lowest_current = int(columns[3]) if columns[3] != "" else None

    if lowest_current and lowest_current <= lowest_data["min_temperature"]:
        lowest_data["min_temperature"] = lowest_current
        lowest_data["date"] = columns[0]

    humidity_current = int(columns[7]) if columns[7] != "" else None

    if humidity_current and humidity_current >= humidity_data["max_humidity"]:
        humidity_data["max_humidity"] = humidity_current
        humidity_data["date"] = columns[0]

print()

print("Highest: {}C on {}".format(highest_data["max_temperature"], highest_data["date"]))
print("=====================")
print("Lowest: {}C on {}".format(lowest_data["min_temperature"], lowest_data["date"]))
print("=====================")
print("Humidity: {}% on {}".format(humidity_data["max_humidity"], humidity_data["date"]))

f.close()
