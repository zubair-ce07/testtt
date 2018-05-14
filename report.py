class Report:
    
    def show_report (self, report):
        for k,v in report.items():
            print(k, v)

    def show_chart_report(self, readings):
        for reading in readings:
            if (reading.max_temprature is not ''):
                print(reading.day.split('-')[2]+' ' , end="")
                for i in range(reading.max_temprature):
                    print("\x1b[91m+\x1b[00m", end="")
                print(' ' + str(reading.max_temprature) + "C")

            if (reading.min_temprature is not ''):
                print(reading.day.split('-')[2]+' ' , end="")
                for i in range(reading.min_temprature):
                    print("\x1b[34m+\x1b[00m", end="")
                print(' ' + str(reading.min_temprature) + "C")
    
    def show_one_liner_chart_report(self, readings):
        for reading in readings:
            if (reading.min_temprature is not '' and reading.min_temprature is not ''):
                print(reading.day.split('-')[2] + " " , end="")
                for i in range (reading.min_temprature):
                    print("\x1b[34m+\x1b[00m", end="")
                for i in range (reading.max_temprature):
                    print("\x1b[91m+\x1b[00m", end="")
                print(" " + str(reading.min_temprature) + "C - " + str(reading.max_temprature) + "C")