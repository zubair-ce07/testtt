class Calculations:
    def __init__(self):
        pass

    def cal_yearly(self, record):
        max_temp, min_temp, max_hum = -1, 9999, -1
        max_t, min_t, max_h = record[0], record[0], record[0]
        for row in record:
            if row.max_temp > max_temp:
                max_temp = row.max_temp
                max_t = row
            if row.min_temp < min_temp:
                min_temp = row.min_temp
                min_t = row
            if row.max_humidity > max_hum:
                max_hum = row.max_humidity
                max_h = row
        return max_t, min_t, max_h

    def cal_monthly(self, record):
        max_temp, min_temp, mean_hum = 0, 0, 0
        for row in record:
            max_temp += row.max_temp
            min_temp += row.min_temp
            mean_hum += row.mean_humidity
        max_temp = max_temp // len(record)
        min_temp = min_temp // len(record)
        mean_hum = mean_hum // len(record)
        return max_temp, min_temp, mean_hum
