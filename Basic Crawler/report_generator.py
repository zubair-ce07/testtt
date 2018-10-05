class ReportGenerator:
    """"
    Class for calculating and generating the report for the urls
    data which includes total number of bytes, average size and
    total requests
    """

    def __init__(self, data, urls, requests):
        self.data = data
        self.total_urls = urls
        self.total_requests = requests
        self.calculations = {"Total Bytes": 0,
                             "Average Size": 0.0,
                             "Total Requests": self.total_requests
                             }

    def calculate(self):
        """Calculating total bytes and average size"""
        for i in self.data:
            self.calculations["Total Bytes"] = (self.calculations[
                "Total Bytes"] + len(i.result().content))
        self.calculations["Average Size"] = self.calculations[
            "Total Bytes"] / self.total_urls

    def generate_report(self):
        """Printing the calculations"""
        print("Total bytes: {}".format(self.calculations["Total Bytes"]))
        print("Average size of page: {}".format(
            self.calculations["Average Size"]))
        print("Total Requests: {}".format(self.calculations["Total Requests"]))
