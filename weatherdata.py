import datetime


class WeatherData:
    """This is a data structure for holding all the weather data
    it contains data from all the files present in directory.
    """
    def __init__(self):
        self.data = []                      # The list that will hold all the data
        self.current = 0                    # Iterator for using the object in for loops

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.data):
            raise StopIteration
        else:
            self.current += 1
            return self.data[self.current-1]

    def reset_iter(self):
        self.current = 0

    def add(self, day_report, header):
        """This function adds new elements to the data structure
        on each operation a dictionary with whole data for one
        day is added to the list"""
        daily_report = self._get_daily_report(day_report, header)
        self.data.append(daily_report)

    def get(self, index):
        return self.data[index]

    def remove(self):
        del self.data[len(self.data) - 1]
        return self

    def size(self):
        return len(self.data)

    @staticmethod
    def _get_daily_report(day_report, header):
        """This function gets the raw data and populates the
        data structure with proper formatted data types and values"""
        daily_report = dict()

        for idx, value in enumerate(day_report.split(",")):
            if idx == 0:
                date = value.split("-")
                # Storing date in proper datetime format
                value = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            else:
                # Converting int/float values to their respective data types
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        value = "NA"
            # Keeping the key for date consistent
            daily_report["PKT" if header[idx].strip() == "PKST" else header[idx].strip()] = value
        return daily_report
