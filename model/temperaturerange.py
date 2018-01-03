import helper.common as common


class TemperatureRange:


    def stats(self, Year, CSVData):
        
        StatsData = {
            'highest': {
                'temp': False,
                'date': False
            },
            'lowest': {
                'temp': False,
                'date': False
            },
            'humid': {
                'humidity': False,
                'date': False
            }
        }
        if (len(CSVData) > 0):
            for Row in CSVData:
                if (Year == common.format_date(Row[0], '%Y')):
                    MaxTemp = common.filter_int_val(Row[1])
                    if (MaxTemp and (StatsData['highest']['temp'] == False or StatsData['highest']['temp'] < MaxTemp)):
                        StatsData['highest']['temp'] = MaxTemp
                        StatsData['highest']['date'] = Row[0]

                    min_temp = common.filter_int_val(Row[3])
                    if (min_temp and (StatsData['lowest']['temp'] == False or StatsData['lowest']['temp'] > MaxTemp)):
                        StatsData['lowest']['temp'] = min_temp
                        StatsData['lowest']['date'] = Row[0]
                    
                    MaxHumid = common.filter_int_val(Row[8])
                    if (MaxTemp and (StatsData['humid']['humidity'] == False or StatsData['humid']['humidity'] < MaxHumid)):
                        StatsData['humid']['humidity'] = MaxHumid
                        StatsData['humid']['date'] = Row[0]

        return StatsData

