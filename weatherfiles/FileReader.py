import fnmatch
import os


class FileReader:
    def get_filenames_from_dir(self, dir, year):
        filenames = []
        for file in os.listdir(dir):
            if fnmatch.fnmatch(file, 'Murree_weather_' + year + '_*.txt'):
                filename = os.path.join(dir, file)
                filenames.append(filename)
        return filenames

    def read_files(self, filenames):
        filesdata = {}
        for filename in filenames:
            filedata = open(filename, 'rU').readlines()
            filesdata[filename] = filedata
        return filesdata

    def read_files_from_path(self, dir, year):
        filenames = self.get_filenames_from_dir(dir, year)
        filesdata = self.read_files(filenames)
        return filesdata
