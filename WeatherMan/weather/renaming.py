import csv
import os
from calendar import month_abbr

'''splitting the text filenames and assigning numbers to months'''
'''Conversion to csv files and renaming'''

def rename (path):
    directory = path + '/weathercsv'

    for wt in os.listdir("{0}".format(path)):

        w_cym, w_ext = os.path.splitext(wt)

        w_city, w_wthr, w_year, w_month = w_cym.split('_')
        month = w_month
        for k, v in enumerate(month_abbr):
            if v == month:
                month = k
                break

        with open("{0}/{1}".format(path,wt),'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open( "{0}/{1}-{2}.csv".format(directory,w_year, month), 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(())
                writer.writerows(lines)

  # print('{}/{}.csv'.format(w_year,month))