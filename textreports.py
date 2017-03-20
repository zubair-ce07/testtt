

class TextReports:
    @staticmethod
    def yearly_report(highest_temperature, lowest_temperature, max_humidity):
        print 'Highest: {temp}C on {month} {day}'.format(
            temp=highest_temperature['key'], month=highest_temperature['month'],
            day=highest_temperature['day'])
        print 'Lowest: {temp}C on {month} {day}'.format(
            temp=lowest_temperature['key'], month=lowest_temperature['month'],
            day=lowest_temperature['day'])
        print "Humid: {humidity}% on {month} {day}".format(
            humidity=max_humidity['key'], month=max_humidity['month'],
            day=max_humidity['day'])

    @staticmethod
    def monthly_report(
            avg_max_temperature, avg_min_temperature, avg_mean_humidity):
        print 'Highest Average: {avg_max_temperature}C'.format(
            avg_max_temperature=avg_max_temperature)
        print 'Lowest Average: {avg_min_temperature}C'.format(
            avg_min_temperature=avg_min_temperature)
        print 'Average Humidity: {avg_mean_humidity}%'.format(
            avg_mean_humidity=avg_mean_humidity)
