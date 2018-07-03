class Results:
    def __init__(self, date_max_annual_temp=0, date_max_annual_hum=0,
                 date_min_annual_temp=0, max_annual_hum=0,
                 max_annual_temp=0, min_annual_temp=0,
                 mean_avg_hum=0, min_avg_temp=0, max_avg_temp=0):
        self.max_annual_temp = max_annual_temp
        self.min_annual_temp = min_annual_temp
        self.max_annual_hum = max_annual_hum
        self.date_max_annual_temp = date_max_annual_temp
        self.date_min_annual_temp = date_min_annual_temp
        self.date_max_annual_hum = date_max_annual_hum
        self.max_avg_temp_of_month = max_avg_temp
        self.min_avg_temp_of_month = min_avg_temp
        self.avg_mean_hum_of_month = mean_avg_hum
