Application
=======

The purpose of weather man is to give weather reports.

## Getting Started

### Major Requirement(s):
    Python3.7

### First of all for virtual environment use following commands:
    cd weather_man
    virtualenv -p python3.7 ~/.virtualenvs/weather_man
    source ~/.virtualenvs/weather_man/bin/activate
    pip install -r requirements.txt

 Run the file run_app.py by passing required arguments

#### Arguments example for weather man application:
#####  For a given year display the highest temperature and day, lowest temperature and day, most humid day and humidity.

	run-app.py /path/to/files-dir -e 2002
##### For a given month display the average highest temperature, average lowest temperature, average mean humidity.

	run-app.py /path/to/files-dir -a 2005/6
##### For a given month draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

	run-app.py weatherman.py /path/to/files-dir -c 2011/03
##### Multiple Reports

	run-app.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011

##### For a given month draw one horizontal bar chart on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

	run-app.py /path/to/files-dir -c 2011/3

#### Want some fun?
    run-app.py /path/to/files-dir -m 2010/1 -e 2015 -a 2011/3 -c 2012/5

### To clean environment following commands can be used:
    deactivate
    rm -rf ~/.virtualenvs/weather_man
    find . -name "*.pyc" -exec rm -f {} \;
