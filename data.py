import copy
import csv
import sys
import os

class data:

    def __init__(self):

        self.dic = {
        "PKT": None,
        "Max TemperatureC": None,
        "Min TemperatureC": None,
        "Max Humidity": None,
        "Mean Humidity": None,
        }
        self.day = []
        self.list_month = []
        self.list_year = []
        self.month_check = ["Jan", "Feb",
                "Mar", "Apr",
                "May", "jun",
                "Jul", "Aug",
                "Sep", "Oct",
                "nov", "Dec"]
        self.year_check = [2004, 2005, 2006, 2007, 2008, 2009,
                2010, 2011, 2012, 2013, 2014, 2015, 2016]
