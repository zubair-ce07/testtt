# Weatherman

Python program to genrate different reports.

## Problem Statement

Write a python script to generate following reports:

### 1. 
For a given year display the highest temperature and day, lowest temperature and day, most humid day and humidity.

$ weatherman.py /path/to/files-dir -e 2002 </br>
Highest: 45C on June 23 </br>
Lowest: 01C on December 22 </br>
Humidity: 95% on August 14 </br>

### 2. 
For a given month display the average highest temperature, average lowest temperature, average mean humidity.

$ weatherman.py /path/to/files-dir -a 2005/6 </br>
Highest Average: 39C </br>
Lowest Average: 18C </br>
Average Mean Humidity: 71% </br>

### 3. 
For a given month draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

$ weatherman.py /path/to/files-dir -c 2011/03 </br>
March 2011 </br>
01 +++++++++++++++++++++++++ 25C </br>
01 +++++++++++ 11C </br>
02 ++++++++++++++++++++++ 22C </br>
02 ++++++++ 08C </br>

### 4. 
Multiple Reports

$ weatherman.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011

### 5.
BONUS TASK. For a given month draw one horizontal bar chart on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

$ weatherman.py /path/to/files-dir -c 2011/3 </br>
March 2011 </br>
01 ++++++++++++++++++++++++++++++++++++ 11C - 25C </br>
02 ++++++++++++++++++++++++++++++ 08C - 22C </br>
