import os

import glob


class WeatherRecord:
    def __init__(self):
        self.weather_data = None


    def read_data_from_files(self,folder_path="/home/haseeb/Desktop/weatherfiles/weatherfiles"):
        txt_files = glob.glob(folder_path+"/*.txt")  #Read text files
        self.weather_data = []
        for txt_file in txt_files:
            opened_file = open(txt_file)
            month_name = self.parse_month_name(opened_file)
            keys = str(opened_file.readline())  #Read headings
            keys = keys.split(',')
            for line in opened_file.readlines()[1:]:
                line = line.replace('\n', '')
                line_content_list = line.split(',')
                year_month_date = line_content_list[0].split('-')
                self.weather_data.append(self.populate_data(keys,line_content_list,month_name,year_month_date))
            opened_file.close()
        # for data in self.weather_data:
        #     x  = data.get("2008",{}).get(('1','Jan'),{}).get("31",{}).get("MeanDew PointC")
        #     if x is not None:
        #         print x

         

    def parse_month_name(self,file_path):
        temp_month_name = str(os.path.basename(os.path.splitext(file_path.name)[0]))  #Strip path
        temp_month_name = temp_month_name.split('_')
        return temp_month_name[3]

    def populate_data(self,keys,line_content_list,month_name,year_month_date):
        temp_dictionary = {}
        sub_key_level_dictionary = {}
        for key, weather_data in zip(keys, line_content_list):
            key = key.replace('\n','')
            temp_dictionary[key] = weather_data
            sub_key_level_dictionary = {
                                str(year_month_date[0]):{
                                    (str(year_month_date[1]),month_name):{
                                        str(year_month_date[2]):
                                            temp_dictionary
                                        }
                                    }
                                }
        return sub_key_level_dictionary
    

weather_record = WeatherRecord()
weather_record.read_data_from_files()