import json


class ReportResult:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def __str__(self):
        return ("Report for : %s %s" % (self.year, self.month)).strip()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
