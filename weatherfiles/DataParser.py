"""class to import data from files into data structure"""

import os


class DataParser:
    @staticmethod
    def parsefile(directory,data):

        for file in os.listdir(directory):
            if '.txt' in file:
                datafile = open(directory+'/'+file, 'r')
                line = datafile.readline()
                while line:
                    if not data['Features']:
                        data['Features'] = line.split('\n')[0]
                        data['Features'] = data['Features'].split(',')
                    elif data['Features'][-1] not in line:
                        data['values'].append(line.split('\n')[0].split(','))
                    line = datafile.readline()

                datafile.close()

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

    # @staticmethod
    # def setdatatype(data):
    #
    #
    #     return data