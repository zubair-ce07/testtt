from CalculateReadings import *


class ReportGenerator:

    def __init__(self, file_name):
        self.file_name = file_name

    def report_A(self):
        obj = CalculateReadings(self.file_name)
        obj.cal_report_A()
        obj.results.display_report_A()

    def report_C(self):
        obj = CalculateReadings(self.file_name)
        obj.cal_report_C()
        obj.results.display_report_C()

    def report_E(self):

        monthly_data = []
        index = 0
        f_name = self.file_name[-4:]
        path = self.file_name[:-4]

        for f in os.listdir(path):

            if (f.find(str(f_name)) != -1):
                file_path = path+"/"+f
                monthly_data.append(CalculateReadings(file_path))

                monthly_data[index].set_highest_temperature()
                monthly_data[index].set_lowest_temperature()
                monthly_data[index].set_highest_humidity()

                index = index+1

        monthly_data[-1] = max(
            monthly_data, key=lambda item: item.results.highest_temperature)
        monthly_data[-1] = min(
            monthly_data, key=lambda item: item.results.lowest_temperature)
        monthly_data[-1] = max(
            monthly_data, key=lambda item: item.results.highest_humidity)

        monthly_data[-1].results.display_report_E()
