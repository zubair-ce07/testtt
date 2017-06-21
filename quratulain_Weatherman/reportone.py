import fnmatch


class ReportOne:
    def __init__(self, files_dict, year):
        self.year = year
        self.found = False

        self.records = []
        self.separate_report_data(files_dict)

    def separate_report_data(self, files_dict):
        file_pattern = 'Murree_weather_' + self.year + '_*.txt'

        for file_name, records in files_dict.items():
            if fnmatch.fnmatch(file_name, file_pattern):
                self.found = True
                self.records.extend(records)

    def generate_report(self):
        """
        The function performs the required calculation i.e. max temprature, min temprature and max humidity
        on previously filtered list of dictionaries.
        """

        self.max_temp_record = max(self.records, key=lambda x: x['maxTemprature'])
        self.min_temp_record = min(self.records, key=lambda x: x['minTemprature'])
        self.max_humid_record = max(self.records, key=lambda x: x['maxHumidity'])

    def print_report(self):
        if self.found:
            print("Report1")
            print("Highest: {}C on {} {}".format(self.max_temp_record['maxTemprature'],
                                                 self.max_temp_record['month'],
                                                 self.max_temp_record['day']))
            print("Lowest: {}C on {} {}".format(self.min_temp_record['minTemprature'],
                                                self.min_temp_record['month'],
                                                self.min_temp_record['day']))
            print("Humidity: {}% on {} {} \n".format(self.max_humid_record['maxHumidity'],
                                                     self.max_humid_record['month'],
                                                     self.max_humid_record['day']))
        else:
            output = "For report1: Record for the year %s doesn't exists \n" % (self.year)
            print(output)
