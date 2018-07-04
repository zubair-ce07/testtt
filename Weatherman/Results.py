class Results:
    def __init__(self, result_dict):
        self.max_annual_temp = result_dict.get('max_annual_temp')
        self.min_annual_temp = result_dict.get('min_annual_temp')
        self.max_annual_hum = result_dict.get('max_annual_hum')
        self.date_max_annual_temp = result_dict.get('date_max_annual_temp')
        self.date_min_annual_temp = result_dict.get('date_min_annual_temp')
        self.date_max_annual_hum = result_dict.get('date_max_annual_hum')
        self.max_avg_temp_of_month = result_dict.get('max_avg_temp')
        self.min_avg_temp_of_month = result_dict.get('min_avg_temp')
        self.avg_mean_hum_of_month = result_dict.get('mean_avg_hum')
