import os
import fnmatch


class WeatherFilesReader(object):

    retrieved_records = None

    def __init__(self, dir):
        self.dir = dir

    def get_filenames_by_year(self, year):
        all_files = os.listdir(self.dir)
        output_files = []
        for file in all_files:
           if fnmatch.fnmatch(file, '*_' + year + '*'):
               output_files.append(file)
        return output_files

    def read_by_year(self, year):
        if not any(key.startswith(year) for key in self.retrieved_records):
            filenames = self.get_filenames_by_year(year)
            with open(os.path.join(self.dir, filenames)) as csvfile:
                pass

    def read_by_years(self, years):
        pass