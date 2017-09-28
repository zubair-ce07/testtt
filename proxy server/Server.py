import json
from http.server import BaseHTTPRequestHandler
from crawler_stats import CrawlerStatsProxy


class Server(BaseHTTPRequestHandler):
    crawler = CrawlerStatsProxy('ahmed.sufian@arbisoft.com', 'ahmed@arbisoft')

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        response = self.crawler._scrape_daily_stats()
        self.wfile.write(bytearray(json.dumps(response), 'utf8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write(b"hello")
