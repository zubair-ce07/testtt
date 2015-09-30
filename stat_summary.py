class StatSummary(object):

    #: Initialize all the variables
    def __init__(self, total_requests=0, total_bytes_downloaded=0, avg_page_size=0):
        self.total_requests = total_requests
        self.total_bytes_downloaded = total_bytes_downloaded
        self.avg_page_size = avg_page_size

    def calculate_average_size(self):
        self.avg_page_size = float(self.total_bytes_downloaded) / float(self.total_requests)

    def display_summary(self):
        self.calculate_average_size()
        print "Average Page Size     :  " + str(self.avg_page_size)
        print "Total Requests        :  " + str(self.total_requests)
        print "Total bytes downloaded:  " + str(self.total_bytes_downloaded)