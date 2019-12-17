from My_ArgParser import *
from ReportGenerator import *

# --------------------------------Main-----------------------------------
arguments = My_ArgParser()


if(arguments.args.a):
    file_name = arguments.args.path+"/Murree_weather_" + \
        str(arguments.args.a.year)+"_"+arguments.args.a.strftime("%b")
    obj = ReportGenerator(file_name)
    obj.report_A()


if(arguments.args.c):
    file_name = arguments.args.path+"/Murree_weather_" + \
        str(arguments.args.c.year)+"_"+arguments.args.c.strftime("%b")
    obj = ReportGenerator(file_name)
    obj.report_C()


if(arguments.args.e):
    file_name = arguments.args.path + str(arguments.args.e.year)
    obj = ReportGenerator(file_name)
    obj.report_E()

#  weatherman.py /home/waleed/Desktop/final/the-lab/weatherfiles
# -c 2005/04 -a 2005/10 -e 2006
