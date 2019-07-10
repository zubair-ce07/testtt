from csv import DictReader
from glob import glob

from weather_container import RecordHolder


class FileParser:

    def is_valid_record(self, record):
        valid_record = [record["Max TemperatureC"], record["Min TemperatureC"],
                        record[" Mean Humidity"], record.get("PKT", record.get("PKST"))]
        if all(valid_record):
            return True

    def data_extractor(self, files_path):
        compiled_records = []
        files_path += f"Murree_weather_*"
        for files in glob(files_path):

            with open(files, "r") as single_file:
                record_reader = DictReader(single_file)
                compiled_records += [RecordHolder(record) for record in record_reader if
                                     self.is_valid_record(self, record)]
        return compiled_records
