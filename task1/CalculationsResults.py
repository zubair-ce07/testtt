import calendar


class CalculationsResults:

    def lowest_temp_in_year(self, weather_data):
        try:
            min_temp = int(weather_data[0].min_temperature)
            min_temp_day = weather_data[0].pk
        except:
            min_temp = None
            min_temp_day = None
        for i in weather_data:
            try:
                if int(i.min_temperature) < min_temp or (not min_temp):
                    min_temp = int(i.min_temperature)
                    min_temp_day = i.pkt
            except:
                continue
        return min_temp, self.to_date(min_temp_day)

    def highest_temp_in_year(self, weather_data):
        try:
            max_temp = int(weather_data[0].max_temperature)
            max_temp_day = weather_data[0].pkt
        except:
            max_temp = None
            max_temp_day = None
        for i in weather_data:
            try:
                if int(i.max_temperature) > max_temp or (not max_temp):
                    max_temp = int(i.max_temperature)
                    max_temp_day = i.pkt
            except:
                continue
        return max_temp, self.to_date(max_temp_day)

    def most_humid_day_of_year(self, weather_data):
        try:
            humidity_level = int(weather_data[0].mean_humidity)
            most_humid_day = weather_data[0].pkt
        except:
            humidity_level = None
            most_humid_day = None
        for i in weather_data:
            try:
                if (int(i.mean_humidity) > humidity_level)or(not humidity_level):
                    humidity_level = int(i.mean_humidity)
                    most_humid_day = i.pkt
            except:
                continue
        return humidity_level, self.to_date(most_humid_day)

    def avg_lowest_temp(self, weather_data):
        sum_temp = 0
        count = 0
        for i in weather_data:
            try:
                sum_temp += int(i.min_temperature)
                count += 1
            except:
                continue
        return (sum_temp/count)

    def avg_highest_temp(self, weather_data):
        count = 0
        sum_temp = 0
        for i in weather_data:
            try:
                sum_temp += int(i.max_temperature)
                count += 1
            except:
                continue

        return sum_temp / count

    def avg_mean_humidity(self, weather_data):
        count = 0
        sum_humidity = 0

        for i in weather_data:
            try:
                sum_humidity += int(i.mean_humidity)
                count += 1
            except:
                continue
        return sum_humidity/count

    def to_date(self, pkt):
        if not pkt:
            return None
        if pkt[6] != "-":
            month = calendar.month_name[int(pkt[5:7])]
            day = pkt[8:]
        else:
            month = calendar.month_name[int(pkt[5])]
            day = pkt[7:]
        return month[:3] + " " + day
