import sys
import os
import shutil
from weather import renaming, Task_1, Task_2, Task_3, Bonus_Task

if os.path.exists(sys.argv[3] +'/weathercsv'):
    shutil.rmtree(sys.argv[3] +'/weathercsv')

renaming.rename(sys.argv[3])
#print("'" + sys.argv[3] +'/' + sys.argv[2]+'*.csv' +"'")
if sys.argv[1] == '-e':
    Task_1.task1(sys.argv[2],sys.argv[3])


elif sys.argv[1] == '-a':
    Task_2.task2(sys.argv[2], sys.argv[3])

elif sys.argv[1] == '-c':
    Task_3.task3(sys.argv[2], sys.argv[3])
    print("BONUS TASK")
    Bonus_Task.bonustask(sys.argv[2], sys.argv[3])

shutil.rmtree(sys.argv[3] +'/weathercsv')

