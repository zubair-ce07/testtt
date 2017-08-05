import os
import datetime


class Filling:


     def __init__(self):

                 self.path=None
                 self.file_names = []
                 self.total_day = None 
                 self.datelist = []
                 self.max_temp_of_days = []
                 self.max_temp_of_months = []
                 self.date_max_temp_months = []
                 self.lowest_temp_of_months = []
                 self.lowest_temp_months_dates = []
                 self.min_temp = []
                 self.max_humidity = []
                 self.max_humidity_month = []
                 self.max_humidity_month_date = []
                 self.mean_humidity = []
     def parse_int(self, list):
         return map(int, list)

     def store_filenames(self, directory, year, mm):
          self.path = directory
          hasfile = False
          for root, dirs, files in os.walk(directory):
               for file in files:
                   if mm == None:
                       if file.endswith('.txt'):
                           if year in file:
                               self.file_names.append(file)
                               hasfile = True
                   elif mm != None:
                        mm = int(mm)
                        yyyy = int(year)
                        month = datetime.date(yyyy, mm, 1).strftime('%B')
                        if file.endswith(month[:3]+'.txt'):
                            if year in file:
                               self.file_names.append(file)
                               hasfile = True
          if hasfile == False:
             print("No File Found for this year")
             exit()
    
     def save_reading(self, daily_record):          
         daily_list = daily_record.split(',')
         if(daily_list[1]!=''):
             self.datelist.append(daily_list[0])
             self.max_temp_of_days.append(daily_list[1])
         if(daily_list[3]!=''):
             self.min_temp.append(daily_list[3])
         if(daily_list[8]!=''):
             self.mean_humidity.append(daily_list[8])
         if(daily_list[7]!=''):
             self.max_humidity.append(daily_list[7])

     def read_file(self, file_path):
               text_file =open(file_path, 'r')
               lines =text_file.readlines()
               count =0
               for line in lines:
                       if count==0:
                          count +=1
                          continue
                       else:
                          self.save_reading(line)

               self.max_temp_of_days = self.parse_int(self.max_temp_of_days)
               self.max_temp_of_months = self.parse_int(self.max_temp_of_months)
               self.min_temp = self.parse_int(self.min_temp)
               self.mean_humidity = self.parse_int(self.mean_humidity)
               self.max_humidity = self.parse_int(self.max_humidity)

class Computation:

     filling = None
     def __init__(self, filling):
             self.filling = filling
     def convert_date_format(self, datestr):
         datel = datestr.split('-')
         dateint =map(int, datel)
         month = datetime.date(dateint[0], dateint[1], dateint[1]).strftime('%B')
         return month +" " + str(dateint[2]) 

     def avg_max_temp(self):
         return sum(self.filling.max_temp_of_days)/len(self.filling.datelist)

     def avg_min_temp(self):
         return sum(self.filling.min_temp)/len(self.filling.datelist)

     def avg_mean_humidity(self):
         return sum(i for i in self.filling.mean_humidity)/len(self.filling.datelist)


     def find_max_temp_of_months(self):
         for i in range(0, len(self.filling.file_names)-1):
               abs_path = self.filling.path+'/'+self.filling.file_names[i]
               self.filling.read_file(abs_path)
               self.filling.max_temp_of_months.append(max(self.filling.max_temp_of_days))
               self.filling.date_max_temp_months.append(self.filling.datelist[self.filling.max_temp_of_days.index(
                                                                                                   max(self.filling.max_temp_of_days))])

               self.filling.lowest_temp_of_months.append(min(self.filling.min_temp))
               self.filling.lowest_temp_months_dates.append(self.filling.datelist[self.filling.min_temp.index(min(self.filling.min_temp))])
              
               self.filling.max_humidity_month.append(max(self.filling.max_humidity))
               self.filling.max_humidity_month_date.append(self.filling.datelist[self.filling.max_humidity.index(max
                                                                                                              (self.filling.max_humidity))])

               self.filling.max_temp_of_days = []
               self.filling.min_temp = []
               self.filling.max_humidity = []
               self.filling.datelist = []
     
     def highest_temp_bar(self, number):
         return '\033[1;31m'+'+'*number

     def lowest_temp_bar(self, number):
          return '\033[1;34m'+'+'*number


class Report:


     
     filling = Filling()
     computution =  Computation(filling)
     def show_monthly_avg(self):
          print("Average Highest Temperature::"
                +str(self.computution.avg_max_temp())
                +"C")
          print("Average Lowest  Temperature::"
                +str(self.computution.avg_max_temp())
                +"C")
          print("Average Mean Humidity::"
                +str(self.computution.avg_max_temp())
                +"%")

     def disjoin_horizontal_bar(self):
      
          for i in range(0, len(self.filling.max_temp_of_days)):
                print(self.filling.datelist[i]
                      +self.computution.highest_temp_bar(self.filling.max_temp_of_days[i]) 
                      +str(self.filling.max_temp_of_days[i])
                      +"C")
                print(self.filling.datelist[i]
                      +self.computution.lowest_temp_bar(self.filling.min_temp[i]) 
                      +str(self.filling.min_temp[i])
                      +"C")
     def single_horizontal_bar(self):

          for i in range(0, len(self.filling.max_temp_of_days)):
                print(self.filling.datelist[i]
                      +self.computution.lowest_temp_bar(self.filling.min_temp[i]) 
                      +self.computution.highest_temp_bar(self.filling.max_temp_of_days[i]) 
                      +str(self.filling.min_temp[i])
                      +"C - "
                      +str(self.filling.max_temp_of_days[i])
                      +"C")

     def find_year(self):
         print("Highest: " 
               + str(max(self.filling.max_temp_of_months))
               + "C on "
               +self.computution.convert_date_format(self.filling.date_max_temp_months[self.filling.max_temp_of_months.index
                                                                                         (max(self.filling.max_temp_of_months))])
               )
         print("Lowest: " 
               + str(min(self.filling.lowest_temp_of_months))
               + "C on "
               +self.computution.convert_date_format(self.filling.lowest_temp_months_dates[self.filling.lowest_temp_of_months.index(
                                                                               min(self.filling.lowest_temp_of_months))])
               )
         print("Humidity: " 
               + str(max(self.filling.max_humidity_month))
               + "% on "
               +self.computution.convert_date_format(
                                         self.filling.max_humidity_month_date[self.filling.max_humidity_month.index(max
                                                                                                    (self.filling.max_humidity_month))])
               )    


     def given_year(self, path, year, mm):
         self.filling.store_filenames(path, year, mm)
         self.computution.find_max_temp_of_months()
         self.find_year()
 
     def given_month(self, path, year, mm, cmd):
         self.filling.store_filenames(path, year, mm)
         abs_path = self.filling.path+'/'+self.filling.file_names[0]
         self.filling.read_file(abs_path)
         if cmd == "-c":
             self.disjoin_horizontal_bar()
             self.single_horizontal_bar()
         elif cmd == "-a":
              self.show_monthly_avg()





path = input("Enter the Relative Path of file:: ")
commond = input("Enter Commond:: ")
report = Report();
cmd = commond.split(' ')
if(len(cmd) <3):
  if cmd[0] == "-e":
     report.given_year(path, cmd[1], None)
  elif cmd[0] == "-a" or cmd[0] == "-c" :
     yyyymm = cmd[1].split('/')
     report.given_month(path, yyyymm[0], yyyymm[1],cmd[0])
else:   
    if cmd[0] == "-c":
      yyyymm = cmd[1].split('/')
      report.given_month(path, yyyymm[0], yyyymm[1],cmd[0])
      yyyymm = cmd[3].split('/')
      report.given_month(path, yyyymm[0], yyyymm[1],cmd[2])      
      report.given_year(path, cmd[5], None)
    else:
       print("No such commond Found")
       

