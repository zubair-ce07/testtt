import csv
import glob
import os.path

from weather_container import RecordHolder


class FileParser:

    def record_validity(self, single_record):
        maximum = single_record["Max TemperatureC"]
        minimum = single_record["Min TemperatureC"]
        humidity = single_record[" Mean Humidity"]
        if maximum and minimum and humidity:
            return True
        else:
            return False

    def data_extractor(self, directory_file):

        compiled_records = []

        if os.path.exists(directory_file) == False:
            exit("Path not valid")

        file_path = directory_file + 'Murree_weather_' + '*'
        for files in glob.glob(file_path):
            with open(files, "r") as single_file:
                read_record = csv.DictReader(single_file)
                for records in read_record:

                    if self.record_validity(self, records) == False:
                        continue
                    else:
                        compiled_records.append((RecordHolder(records)))

        return compiled_records
