import helper.common as common

class TempChart:


    def stats(self, Date, CSVData):
        
        StatsData = []
        Content = ''
        if (len(CSVData) > 0):
            for Row in CSVData:
                if (Date == common.format_date(Row[0], '%Y/%m')):
                    MaxTemp = common.filter_int_val(Row[1])
                    if (MaxTemp):
                        Content = common.format_date(Row[0], "%d") + " " + common.create_bars(MaxTemp, 'red') + " " + Row[1] + "C"
                        StatsData.append(Content)
                    
                    MinTemp = common.filter_int_val(Row[3])
                    if (MinTemp):
                        Content = common.format_date(Row[0], "%d") + " " + common.create_bars(MinTemp, 'blue') + " " + Row[3] + "C"
                        StatsData.append(Content)
        return StatsData



    def combine_stats(self, Date, CSVData):
        
        StatsData = []
        Content = ''
        if (len(CSVData) > 0):
            for Row in CSVData:
                if (Date == common.format_date(Row[0], '%Y/%-m')):
                    Content = common.format_date(Row[0], "%d")
                    Temperature = ''
                    Flag = False

                    MinTemp = common.filter_int_val(Row[3])
                    if (MinTemp):
                        Content = Content + common.create_bars(MinTemp, 'blue')
                        Temperature = Row[3]+ 'C'
                        Flag = True
                    else:
                        Temperature = "**"

                    MaxTemp = common.filter_int_val(Row[1])
                    if (MaxTemp):
                        Content = Content + common.create_bars(MaxTemp, 'red')
                        Temperature = Temperature + ' - ' + Row[1] + 'C'
                        Flag = True
                    else:
                        Temperature = Temperature + "**"

                    if (Flag):    
                        Content = Content + " " + Temperature
                        StatsData.append(Content)
        
        return StatsData

    