import calendar
import result_container


class WeatherSummary:
    date_key = "PKT"

    @staticmethod
    def get_result_for_e(year, data):
        result = result_container.ResultContainer(
            "NA", "NA", "NA", "NA", "NA", "NA"
        )
        for daily_data in data:
            if daily_data.date.year == year:
                if (daily_data.highest_temperature != "NA"
                    and result.highest_temperature == "NA") \
                        or (daily_data.highest_temperature != "NA"
                            and daily_data.highest_temperature
                            > result.highest_temperature):
                    # If the above condition is true
                    result.highest_temperature \
                        = daily_data.highest_temperature

                    result.highest_temperature_day \
                        = str(calendar.month_name[daily_data.date.month]) \
                        + " " + str(daily_data.date.day)

                if (daily_data.lowest_temperature != "NA"
                    and result.lowest_temperature == "NA") \
                        or (daily_data.lowest_temperature != "NA"
                            and daily_data.lowest_temperature
                            < result.lowest_temperature):
                    # If the above condition is true
                    result.lowest_temperature \
                        = daily_data.lowest_temperature

                    result.lowest_temperature_day \
                        = str(calendar.month_name[daily_data.date.month]) \
                        + " " + str(daily_data.date.day)

                if (daily_data.max_humidity != "NA"
                    and result.highest_humidity == "NA") \
                        or (daily_data.max_humidity != "NA"
                            and daily_data.max_humidity
                            > result.highest_humidity):
                    # If the above condition is true
                    result.highest_humidity = daily_data.max_humidity

                    result.most_humid_day = \
                        str(calendar.month_name[daily_data.date.month]) \
                        + " " + str(daily_data.date.day)

        return result

    @staticmethod
    def get_result_for_a(year, month, data):
        result = result_container.ResultContainer(
            "NA", "NA", "NA", "NA", "NA", "NA"
        )
        total_avg_humidity_entries = 0
        sum_avg_humidity_entries = 0

        for daily_data in data:
            if daily_data.date.year == year \
                    and daily_data.date.month == month:
                if (daily_data.mean_temperature != "NA"
                    and result.highest_temperature == "NA") \
                        or (daily_data.mean_temperature != "NA"
                            and daily_data.mean_temperature
                            > result.highest_temperature):
                    # If the above condition is true
                    result.highest_temperature \
                        = daily_data.mean_temperature

                if (daily_data.mean_temperature != "NA"
                    and result.lowest_temperature == "NA") \
                        or (daily_data.mean_temperature != "NA"
                            and daily_data.mean_temperature
                            < result.lowest_temperature):
                    # If the above condition is true
                    result.lowest_temperature \
                        = daily_data.mean_temperature

                if daily_data.mean_humidity != "NA":
                    # If the above condition is true
                    sum_avg_humidity_entries = sum_avg_humidity_entries \
                                               + daily_data.mean_humidity
                    total_avg_humidity_entries += 1

        # The condition checks for the case where all the entries were 'NA'
        if total_avg_humidity_entries > 0:
            # If the above condition is true
            result.highest_humidity = \
                int(sum_avg_humidity_entries/total_avg_humidity_entries)

        else:
            result.highest_humidity = "NA"

        return result

    @staticmethod
    def get_result_for_c(year, month, data):
        result = result_container.ResultContainer(
            "NA", "NA", "NA", "NA", "NA", "NA"
        )
        for daily_data in data:
            if daily_data.date.year == year \
                    and daily_data.date.month == month:
                # If the above condition is true
                result.temperature_list.\
                    append((daily_data.highest_temperature,
                            daily_data.lowest_temperature))

        return result
