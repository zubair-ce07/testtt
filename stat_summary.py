__author__ = 'root'


class StatSummary(object):

    #: Initialize all the variables
    def __init__(self):
        self.no_of_requests = 0
        self.total_bytes_downloaded = 0
        self.avg_page_size = 0

    #: Increment for each request
    def increment_request(self):
        self.no_of_requests += 1

    #: Calculating total downloaded bytes
    def add_bytes(self, no_of_bytes):
        self.total_bytes_downloaded += no_of_bytes

    def calculate_average_size(self):
        self.avg_page_size = self.total_bytes_downloaded / self.no_of_requests
        return self.avg_page_size