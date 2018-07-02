class Results:
    def __init__(self, date_max_annual_temp=0, date_max_annual_hum=0,
                 date_min_annual_temp=0, max_annual_hum=0,
                 max_annual_temp=0, min_annual_temp=0,
                 mean_avg_hum=0, min_avg_temp=0, max_avg_temp=0):
        self.maxAnnualTemp = max_annual_temp
        self.minAnnualTemp = min_annual_temp
        self.maxAnnualHum = max_annual_hum
        self.dateMaxAnnualTemp = date_max_annual_temp
        self.dateMinAnnualTemp = date_min_annual_temp
        self.dateMaxAnnualHum = date_max_annual_hum
        self.maxAvgTempOfMonth = max_avg_temp
        self.minAvgTempOfMonth = min_avg_temp
        self.avgMeanHumOfMonth = mean_avg_hum
