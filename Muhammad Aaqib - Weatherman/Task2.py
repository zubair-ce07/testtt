import Task as t
import sys

def main():
    if(len(sys.argv)) != 2:
        print("Invalid no of arguments")
        return
    month = sys.argv[1]
    data = t.parser()
    month_result = t.MonthCalculation()
    t.task_2(data, month_result, month)

if __name__ == '__main__':
    main()