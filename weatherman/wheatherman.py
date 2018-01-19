import populatedata
import calculationresult
import weatherreport
import datetime


obj = populatedata.Populatedata(year = '2004',month='Aug', filedir_path = '/home/husnain/Desktop/the-lab/weatherman/weatherfiles')
obj.populatedata()
# #obj.printdatalist()
rslt = calculationresult.Calculateresult(obj.datalist, "month")
rslt.calculate()
report = weatherreport.Weathereport(rslt.resultdict,"month")
report.generate_report()
report.print_report()