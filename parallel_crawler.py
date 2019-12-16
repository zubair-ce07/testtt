import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from statistics import mean
from types import SimpleNamespace

import requests

from utils import find_urls_from_content, get_logger


def send_request(current_url, shared_object, logger):
    try:
        logger.info(f'Sending request to {current_url}')

        if shared_object.download_delay > 0:
            time.sleep(shared_object.download_delay)

        response = requests.get(current_url)

        if response.status_code != 200:
            return None, current_url

        return response, current_url
    except Exception:
        logger.error(f'Error Occurred when sending request {current_url}')
        return None, current_url


class ParallelCrawler:
    def __init__(self, params):
        manager = Manager()

        shared_object = SimpleNamespace()
        shared_object.download_delay = params['delay']
        shared_object.page_sizes = manager.list([])
        shared_object.urls_to_crawl = manager.list([params['url']])
        shared_object.running_tasks_count = manager.Value(int, 0)
        self.__shared_object = shared_object

        self.__requests_to_made = params['count']
        self.__total_requests_made = 0
        self.__crawled_urls = set([])

        self.__pool = ProcessPoolExecutor(params['workers'])

        self.__logger = get_logger('ParallelCrawler')

    def crawl(self):
        average_page_size = 0

        self.__crawl_website()

        self.__pool.shutdown()

        if len(self.__shared_object.page_sizes) > 0:
            average_page_size = mean(self.__shared_object.page_sizes)

        return type("CrawlStats", (object,), dict(requests_made=self.__total_requests_made,
                                                  bytes_downloaded=sum(self.__shared_object.page_sizes),
                                                  average_page_size=average_page_size))

    def __crawl_website(self):

        while True:
            for url in self.__shared_object.urls_to_crawl:
                if url not in self.__crawled_urls:
                    if self.__total_requests_made >= self.__requests_to_made:
                        return

                    self.__total_requests_made += 1

                    task = self.__pool.submit(send_request, url, self.__shared_object, self.__logger)
                    task.add_done_callback(self.__update_statistics)

                    self.__shared_object.running_tasks_count.value += 1
                    self.__shared_object.urls_to_crawl.remove(url)

                    self.__crawled_urls.add(url)

            if self.__shared_object.running_tasks_count.value == 0 and len(self.__shared_object.urls_to_crawl) == 0:
                return

    def __update_statistics(self, result):
        response, current_url = result.result()
        if response is not None:
            urls = find_urls_from_content(response.text, current_url)

            self.__shared_object.urls_to_crawl = list(set(self.__shared_object.urls_to_crawl) | urls)

            self.__shared_object.page_sizes.append(len(response.content))

        self.__shared_object.running_tasks_count.value -= 1
