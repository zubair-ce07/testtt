
class CalculateResults:

    def yearly_highest_temp(self, highest_temp_yearly_days, highest_temp_year):

        sorted_highest_temps=sorted(highest_temp_yearly_days.items(), key=lambda kv: kv[1])

        highest_temp_year[sorted_highest_temps[len(sorted_highest_temps)-1][0]]=\
                    sorted_highest_temps[len(sorted_highest_temps)-1][1]

    def yearly_lowest_temp(self, lowest_temp_yearly_days, lowest_temp_year):
        sorted_lowest_temps = sorted(lowest_temp_yearly_days.items(), key=lambda kv: kv[1])
        lowest_temp_year[sorted_lowest_temps[0][0]]=sorted_lowest_temps[0][1]

    def yearly_most_humid_day(self, highest_humid_yearly_days, most_humid_day_year):

        sorted_humid_days = sorted(highest_humid_yearly_days.items(), key=lambda kv: kv[1])

        most_humid_day_year[sorted_humid_days[len(sorted_humid_days)-1][0]]=\
            sorted_humid_days[len(sorted_humid_days)-1][1]


    def avg(self, temps):
        average=sum(temps.values()) / float(len(temps))
        return int(average)