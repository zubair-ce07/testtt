import csv
import os
import collections
import argparse

Years = ('2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016')
YearsRecord = dict((key, [0, 100, 0, 1000, "Date"]) for key in Years)


def update_record(m_max_t, m_min_t, m_max_h, m_min_h, rec):
    """This function Updates the Yearly Record"""
    index = -1
    if rec[0] < int(max(m_max_t)):
        rec[0] = int(max(m_max_t))
        index = m_max_t.index(rec[0])
    if rec[1] > int(min(m_min_t)):
        rec[1] = int(min(m_min_t))
    if rec[2] < int(max(m_max_h)):
        rec[2] = int(max(m_max_h))
    if rec[3] > int(min(m_min_h)):
        rec[3] = int(min(m_min_h))
    return rec, index


def default_display():
    """Function to Display Help"""
    print("[Report #]\n1 for Annual Max/Min Temperature and Humidity\n2 for Hottest day of each year\n")
    print("[Data_dir]\nDirectory containing weather data files")


def process_data(month_data):
    """This function processes the available data"""
    next(month_data)
    monthly_max_temp = []
    monthly_min_temp = []
    monthly_max_hum = []
    monthly_min_hum = []
    date_max_temp = []
    for row in month_data:
        date = row[0]
        if row[1] != '':
            monthly_max_temp.append(int(row[1]))
            date_max_temp.append(date)
        else:
            monthly_max_temp.append(0)
        if row[3] != '':
            monthly_min_temp.append(int(row[3]))
        if row[7] != '':
            monthly_max_hum.append(int(row[7]))
        if row[9] != '':
            monthly_min_hum.append(int(row[9]))
    year = date[0:4]
    record = YearsRecord[year]
    record, index = update_record(monthly_max_temp, monthly_min_temp, monthly_max_hum, monthly_min_hum, record)
    if not index == -1:
        record[4] = date_max_temp[index]
    YearsRecord[year] = record


def display_yearly_records(years_record):
    """Function to display record of each year"""
    od = collections.OrderedDict(sorted(years_record.items()))
    print("Year\tMAX Temp\tMIN Temp\tMAX Humidity\tMIN "
          "Humidity\n--------------------------------------------------------------\n")
    for key in od:
        print("%s\t%d\t\t%d\t\t%d\t\t%d\n" % (key, od[key][0], od[key][1], od[key][2], od[key][3]))


def display_max_temp_yearly(years_record):
    """Function to display max temperatures of each year"""
    od = collections.OrderedDict(sorted(years_record.items()))
    print(
        "Year\t\tDate\t\tTemp\n--------------------------------------------\n"
    )
    for key in od:
        date = od[key][4].split("-")
        date = date[2] + "/" + date[1] + "/" + date[0]
        print("%s\t\t%s\t%d\n" % (key, date, od[key][0]))


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('report', nargs='?', const=1)
    parser.add_argument('dir', nargs='?', const=1)
    args = parser.parse_args()
    files = os.listdir(args.dir)
    if (args.report is not None) and args.dir is not None:
        for name in files:
            if name == '.DS_Store':
                continue
            else:
                with open(args.dir + name, 'r') as csvfile:
                    line = csv.reader(csvfile, delimiter=',')
                    process_data(line)
        if args.report == "1":
            display_yearly_records(YearsRecord)
        elif args.report == "2":
            display_max_temp_yearly(YearsRecord)
    else:
        default_display()


if __name__ == "__main__":
    main()
