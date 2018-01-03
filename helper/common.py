import os
from datetime import datetime


def format_date(Date, Format = '%B %d'):
    DateTimeObject = datetime.strptime(Date,'%Y-%m-%d')
    return DateTimeObject.strftime(Format)


def read_file_data(DirectoryPath):
    if(os.path.isdir(DirectoryPath)):
        InputFiles = os.listdir(DirectoryPath)
        data = []
        if (len(InputFiles) > 0):
            for FileName in InputFiles:
                index = 0
                FileName = DirectoryPath + FileName
                with open(FileName, 'r') as f:
                    for line in f.readlines():
                        index += 1
                        row = line.strip().split(',')
                        if (len(row) > 1 and index > 2):
                            data.append(row)
        return data
    else:
        print ("Invalid Directory Path")


def filter_int_val(Value):
    try:
        Value = int(Value)
    except ValueError:
        Value = False
    return Value


def font_blue(Content): 
    return "\033[94m {}\033[00m" .format(Content)


def font_red(Content):
    return "\033[91m {}\033[00m" .format(Content)


def create_bars(Count, Color='blue'):
    Content = ''
    for i in range(Count):
        if (Color == 'red'):
            ColoredTxt = font_red('+')
        else:
            ColoredTxt = font_blue('+')
        
        Content = Content + ColoredTxt

    return Content

