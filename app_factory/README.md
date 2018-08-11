Application
=======

The purpose of App factory is to register as many applications as wanted and run in respective flow required.

## Getting Started

### Major Requirement(s):
    Python3.7

### First of all for virtual environment use following commands:
    cd app_factory
    virtualenv -p python3.7 ~/.virtualenvs/app_factory
    source ~/.virtualenvs/app_factory/bin/activate
    pip install -r requirements.txt

 Run the file run_app.py by passing required arguments 1. app_name, 2 and plus all app specific arguments. For example to run weather man application use like:

#### Arguments example for weather man application:
#####  For a given year display the highest temperature and day, lowest temperature and day, most humid day and humidity.

	run-app.py weather-man /path/to/files-dir -e 2002
##### For a given month display the average highest temperature, average lowest temperature, average mean humidity.

	run-app.py weather-man /path/to/files-dir -a 2005/6
##### For a given month draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

	run-app.py weather-man weatherman.py /path/to/files-dir -c 2011/03
##### Multiple Reports

	run-app.py weather-man /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011

##### For a given month draw one horizontal bar chart on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

	run-app.py weather-man /path/to/files-dir -c 2011/3

#### Want some fun?
    run-app.py weather-man /path/to/files-dir -m 2010/1 -e 2015 -a 2011/3 -c 2012/5

### To clean environment following commands can be used:
    deactivate
    rm -rf ~/.virtualenvs/app_factory
    find . -name "*.pyc" -exec rm -f {} \;
