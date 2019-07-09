from csv import DictReader
from glob import glob

from weather_container import RecordHolder


class FileParser:

    def record_validity(self, record):
        valid_record = [record["Max TemperatureC"], record["Min TemperatureC"],
                        record[" Mean Humidity"], record.get("PKT", record.get("PKST"))]
        if all(valid_record):
            return True

    def data_extractor(self, files_path):
        compiled_records = []
        files_path += f"Murree_weather_*"
        for files in glob(files_path):

            with open(files, "r") as single_file:
                read_record = DictReader(single_file)
                compiled_records += [RecordHolder(record) for record in read_record if
                                     self.record_validity(record) is True]
        return compiled_records
