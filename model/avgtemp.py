import helper.common as common


class AvgTemp:


    def stats(self, Date, CSVData):
        
        StatsData = {
            'highest': {
                'sum': 0,
                'count': 0,
                'avg': 0
            },
            'lowest': {
                'sum': 0,
                'count': 0,
                'avg': 0
            },
            'humidity': {
                'sum': 0,
                'count': 0,
                'avg': 0
            }
        }
        if (len(CSVData) > 0):
            for row in CSVData:
                if (Date == common.format_date(row[0], '%Y/%-m')):
                    MaxTemp = common.filter_int_val(row[1])
                    if (MaxTemp):
                        StatsData['highest']['sum'] += MaxTemp
                        StatsData['highest']['count'] += 1

                    MinTemp = common.filter_int_val(row[3])
                    if (MinTemp):
                        StatsData['lowest']['sum'] += MinTemp
                        StatsData['lowest']['count'] += 1
                    
                    Humidity = common.filter_int_val(row[8])
                    if (MinTemp):
                        StatsData['humidity']['sum'] += Humidity
                        StatsData['humidity']['count'] += 1

            if(StatsData['highest']['count'] > 0):
                StatsData['highest']['avg'] = int(StatsData['highest']['sum']/StatsData['highest']['count'])
            
            if(StatsData['lowest']['count'] > 0):
                StatsData['lowest']['avg'] = int(StatsData['lowest']['sum']/StatsData['lowest']['count'])
            
            if(StatsData['humidity']['count'] > 0):
                StatsData['humidity']['avg'] = int(StatsData['humidity']['sum']/StatsData['humidity']['count'])

        return StatsData

