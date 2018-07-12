class CrawlingSummaryReport:
    def __init__(self, total_requests=0, bytes_downloaded=0, avg_page_size=0):
        self.total_requests = total_requests
        self.bytes_downloaded = bytes_downloaded
        self.avg_page_size = avg_page_size
