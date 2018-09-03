"""class to import data from files into data structure"""

import os


class DataParser:
    @staticmethod
    def parsefile(directory, data):
        """
        Read data from giles in directory one by one and place it in dictionary data
        :param directory: is path of the folder containing data files
        :param data: empty dictionary to be filled by method
        :return data: A dictionary with feature_names in "feature" and data in "values"
        """
        for file_name in os.listdir(directory):
            if '.txt' in file_name:
                file_path = os.path.join(directory, file_name)
                datafile = open(file_path, 'r')
                line = datafile.readline()
                while line:
                    if not data['features']:
                        data['features'] = line.split('\n')[0]
                        data['features'] = data['features'].split(',')
                    elif data['features'][-1] not in line:
                        data['values'].append(line.split('\n')[0].split(','))
                    line = datafile.readline()

                datafile.close()

        # convert string values into relative data type on number
        for d in data['values']:
            for i in range(len(d)):
                try:
                    if '.' in d[i]:
                        d[i] = float(d[i])
                    else:
                        d[i] = int(d[i])
                except ValueError:
                    d[i] = d[i]

        return data
