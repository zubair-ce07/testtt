import csv
import glob

from weather_container import RecordHolder


class FileParser:

    def record_validity(self, single_record):
        valid_record = [single_record["Max TemperatureC"],
                       single_record["Min TemperatureC"],
                       single_record[" Mean Humidity"]]
        valid_record.append(single_record.get("PKT",
                                              single_record.get("PKST")))
        if all(valid_record):
            return True
        else:
            return False

    def data_extractor(self, directory_file):
        compiled_records = []
        file_path = directory_file + 'Murree_weather_' + '*'
        for files in glob.glob(file_path):
            with open(files, "r") as single_file:
                read_record = csv.DictReader(single_file)
                compiled_records += [RecordHolder(record) for
                record in read_record if self.record_validity(
                        self, record) is True]
        return compiled_records
