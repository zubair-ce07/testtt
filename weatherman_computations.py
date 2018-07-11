from weatherman_data_structure import calculation_holder
from datetime import date
from statistics import mean


def calculate(readings, report_type, year, month):
    if report_type == 'e':
        highest_temp = max(row.max_temp for row in readings
                           if row.pkt.split("-")[0] == year)
        lowest_temp = min(row.min_temp for row in readings
                          if row.pkt.split("-")[0] == year)
        max_humid = max(row.max_humidity for row in readings
                        if row.pkt.split("-")[0] == year)
        highest_temp_day = ""
        lowest_temp_day = ""
        max_humid_day = ""
        for row in readings:
            if row.max_temp == highest_temp:
                date_ = row.pkt.split("-")
                highest_temp_day = date(int(date_[0]), int(date_[1]),
                                        int(date_[2])).ctime()[:-14]
            if row.min_temp == lowest_temp:
                date_ = row.pkt.split("-")
                lowest_temp_day = date(int(date_[0]), int(date_[1]),
                                       int(date_[2])).ctime()[:-14]
            if row.max_humidity == max_humid:
                date_ = row.pkt.split("-")
                max_humid_day = date(int(date_[0]), int(date_[1]),
                                     int(date_[2])).ctime()[:-14]
        return calculation_holder([highest_temp, lowest_temp, max_humid,
                                   highest_temp_day, lowest_temp_day,
                                   max_humid_day, 0, 0, 0])

    if report_type == 'a':
        highest_mean_temp = max(row.mean_temp for row in readings
                                if row.pkt.split("-")[0] == year and
                                row.pkt.split("-")[1] == month)
        lowest_mean_temp = min(row.mean_temp for row in readings
                               if row.pkt.split("-")[0] == year and
                               row.pkt.split("-")[1] == month)
        avg_mean_humid = mean(row.mean_humidity for row in readings
                              if row.pkt.split("-")[0] == year and
                              row.pkt.split("-")[1] == month)
        return calculation_holder([0, 0, 0, '', '', '', highest_mean_temp,
                                   lowest_mean_temp, avg_mean_humid])
