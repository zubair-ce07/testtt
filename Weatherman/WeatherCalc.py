class WeatherCalc:

    @staticmethod
    def highest_avg_temp_of_month(year, month, data):
        total = 0
        counter = 0
        for dataSegmen in data:
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.year == year and dataSegment.month == month:
                        if dataSegment.highestT != -100:
                            total += dataSegment.highestT

                            counter += 1
                except:
                    continue
        return total / counter

    @staticmethod
    def lowest_avg_temp_of_month(year, month, data):
        total = 0
        counter = 0
        for dataSegmen in data:
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.year == year and dataSegment.month == month:
                        if dataSegment.lowestT != -100:
                            total += dataSegment.lowestT
                            counter += 1
                except:
                    continue
        return total / counter

    @staticmethod
    def average_mean_humidity_of_month(year, month, data):
        total = 0
        counter = 0
        for dataSegmen in data:
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.year == year and dataSegment.month == month:
                        if dataSegment.meanH != -100:
                            total += dataSegment.meanH
                            counter += 1
                except:
                    continue
        return total/counter

    @staticmethod
    def highest_temp_of_year(year, data):
        highest = 0
        index = 0
        index1 = 0
        counter = 0
        counter1 = 0
        for dataSegmen in data:
            counter1 = 0
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.year == year:
                        if dataSegment.highestT > highest:
                            highest = dataSegment.highestT
                            index = counter
                            index1 = counter1
                    counter1 += 1
                except:
                    counter1 += 1
            counter += 1
        return [index, index1]

    @staticmethod
    def lowest_temp_of_year(year, data):
        lowest = 100
        index = 0
        index1 = 0
        counter = 0
        counter1 = 0
        for dataSegmen in data:
            counter1 = 0
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.lowestT != -100 and dataSegment.year == year:
                        if dataSegment.lowestT < lowest:
                            lowest = dataSegment.lowestT
                            index = counter
                            index1 = counter1
                    counter1 += 1
                except:
                    counter1 += 1
            counter += 1
        return [index, index1]

    @staticmethod
    def highest_hum_of_year(year, data):
        highest = 0
        index = 0
        index1 = 0
        counter = 0
        counter1 = 0
        for dataSegmen in data:
            counter1 = 0
            for dataSegment in dataSegmen:
                try:
                    if (dataSegment.year == year):
                        if dataSegment.highestH > highest:
                            highest = dataSegment.highestH
                            index = counter
                            index1 = counter1
                    counter1 += 1
                except:
                    counter1 += 1
            counter += 1
        return [index, index1]
