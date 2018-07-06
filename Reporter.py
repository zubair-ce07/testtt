
def report_e(result):
    print("Highest: {}C on {}".format(
        result["max_temperature"]["temperature"],
        result["max_temperature"]["date"].strftime("%B %d")))
    print("Lowest: {}C on {}".format(
        result["min_temperature"]["temperature"],
        result["min_temperature"]["date"].strftime("%B %d")))
    print("Humidity: {}% on {}".format(
        result["max_humidity"]["humidity"],
        result["max_humidity"]["date"].strftime("%B %d")))


def report_a(result):
    print("Highest Average: {}C".format(result["max_avg_temperature"]))
    print("Lowest Average: {}C".format(result["min_avg_temperature"]))
    print("Average Mean Humidity: {}%".format(result["max_avg_humidity"]))


def report_c(result):
    red = "\033[1;31m"
    blue = "\033[1;34m"
    normal = "\033[0;0m"
    print(result['month'], result['year'])
    for day in range(len(result['max_temperatures'])):
        print("%02d" % (day+1),
              blue + "+" * result['min_temperatures'][day] + red + "+" * result['max_temperatures'][day],
              normal + "%02dC - %02dC" % (result['min_temperatures'][day], result['max_temperatures'][day]))

