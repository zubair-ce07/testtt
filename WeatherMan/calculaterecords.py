class CalculateRecords:
    @staticmethod
    def cal_yearly_report(data):
        return (max([record for record in data if record.max_temp is not None], key=lambda x: x.max_temp),
                min([record for record in data if record.min_temp is not None], key=lambda x: x.min_temp),
                max([record for record in data if record.max_humid is not None], key=lambda x: x.max_humid))


    @staticmethod
    def cal_monthly_report(data):
        max_temperature = [record.max_temp for record in data if record.max_temp is not None]
        min_temperature = [record.min_temp for record in data if record.min_temp is not None]
        mean_humidity = [record.mean_humid for record in data if record.mean_humid is not None]
        return (int(sum(max_temperature) / len(max_temperature)),
                int(sum(min_temperature) / len(min_temperature)),
                int(sum(mean_humidity) / len(mean_humidity)))
