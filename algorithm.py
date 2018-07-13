
import concurrent
import urllib.request


class Algorithm:
    def __init__(self, urls, workers=1, download_delay=1, max_urls=5):
        self._total_urls = 0
        self._total_data = 0
        self._urls = urls
        self._workers = workers
        self.download_delay = download_delay
        self.max_urls = max_urls

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._workers) as executor:
            future_to_url = dict()
            while True:
                if self._total_urls <= self.max_urls:
                    for url in self._urls:
                        future_to_url.update({executor.submit(self._load_url, url, 60): url})
                        self._total_urls = self._total_urls + 1
                        self._urls.pop(0)
                    for future in concurrent.futures.as_completed(future_to_url):
                        url = future_to_url.get(future)
                        try:
                            data = future.result()
                        except Exception as exc:
                            print('%r generated an exception: %s' % (url, exc))
                        else:
                            self._total_data = self._total_data + len(data)
                            print('%r page is %d bytes' % (url, len(data)))

    @staticmethod
    def _load_url(url, timeout):
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return conn.read()
