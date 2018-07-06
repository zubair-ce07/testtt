class CrawlingSummaryReport:
    def __init__(self, t_requests=0, b_downloaded=0, a_page_size=0):
        self.total_requests = t_requests
        self.bytes_downloaded = b_downloaded
        self.avg_page_size = a_page_size
