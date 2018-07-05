import sys
from parse_file import ParseFile
from calculate import Calculate
from report import Report

path = sys.argv[1] + "/"
parser = ParseFile()

if __name__ == '__main__':
    for operation, report in zip(sys.argv[2::2], sys.argv[3::2]):  # Read multiple reports
        report = report.split("/")
        parser.parse(operation, report, path)
