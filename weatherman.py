import sys
import os


class Parser():
    def __init__(self):
        pass

    def read(self, files):
        collection = []

        for file in files:
            f = open(file, 'r')
            data = f.readlines()

            # Remove the headers of the files

            for line in data:
                collection.append(line)
            pass

        return collection

    def clean(self, collection):
        cleanData = [x for x in collection if not x[0].isalpha()
                     and self.includesRelevantData(x)]
        return cleanData
        pass

    def includesRelevantData(self, tuple):
        data = tuple.split(',')
        relevantIndices = [1, 2, 3, 7, 8, 9]

        for r in relevantIndices:
            if data[r] != '':
                return True
                pass
            pass

        return False

    def organizeData(self, cleanData):
        organized = []

        for tuple in cleanData:
            data = tuple.split(',')
            organized.append(data[0])

        return organized


# Get all contents of the directory passed as the first argument

contents = os.listdir(sys.argv[1])
contents = [os.path.join(sys.argv[1], x) for x in contents]

# Remove nested directories and only pickup non hidden files

files = [x for x in contents if os.path.isfile(x) and not x.startswith('.')]

# Read all files and extract data

# file = open(files[0])
# data = file.read()
# print(data)

parser = Parser()

weatherData = parser.read(files)

cleanData = parser.clean(weatherData)

organizedData = parser.organizeData(cleanData)

for x in organizedData:
    print(x)
