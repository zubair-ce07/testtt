import sys

path = sys.argv[1]
for operation, report in zip(sys.argv[2::2], sys.argv[3::2]):
    print(operation, report)
