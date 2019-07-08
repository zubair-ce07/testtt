from statistics import mean


class DataCalculator:

    def monthly_analysis(self, weather_files, date):
        matched_records = []
        matched_records += (records for records in weather_files if
                            records.date.year == date.year and
                            records.date.month == date.month)
        average_high_temp = mean(records.maximum_temp for
                                 records in matched_records)
        average_min_temp = mean(records.minimum_temp for
                                records in matched_records)
        average_mean_humidity = mean(records.average_humidity for
                                     records in matched_records)

        return average_high_temp, average_min_temp, average_mean_humidity

    def yearly_analysis(self, weatherfiles, date):
        yearly_records = [record for record in weatherfiles if
                          record.date.year == date.year]
        yearly_maximum_temp = max(yearly_records, key=lambda
            single_record: single_record.maximum_temp)
        yearly_minimum_temp = max(yearly_records, key=lambda
            single_record: single_record.minimum_temp)
        yearly_maximum_humidity = max(yearly_records, key=lambda
            single_record: single_record.maximum_humidity)

        yearly_list = [yearly_maximum_temp, yearly_minimum_temp,
                       yearly_maximum_humidity]
        return yearly_list

    def bonus_analysis(self, weatherfiles, date):
        bonus_records = [record for record in weatherfiles if
                         record.date.year == date.year and
                         record.date.month == date.month]
        return bonus_records

    def chart_analysis(self, weatherfiles, date):
        chart_records = [record for record in weatherfiles if
                         record.date.year == date.year and
                         record.date.month == date.month]
        return chart_records
