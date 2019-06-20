import Task as t
import sys

def main():
    if(len(sys.argv)) != 2:
        print("Invalid no of arguments")
        return
    year = sys.argv[1]
    year = "2004"
    data = t.parser()
    year_result = t.YearCalculation()
    t.task_1(data, year_result, year)

if __name__ == '__main__':
    main()