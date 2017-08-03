import os
import threading
from multiprocessing import Process

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


def run_scrapy_project(path_to_settings, spiders):
    os.environ['SCRAPY_SETTINGS_MODULE'] = path_to_settings
    runner = CrawlerRunner(get_project_settings())
    runner_crawler = None
    for spider in spiders:
        runner_crawler = runner.crawl(spider["name"])
    runner_crawler.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=False)


class CrawlSpiderThread(threading.Thread):
    def __init__(self, spider_name, path_to_settings, crawl_function):
        threading.Thread.__init__(self)
        self.spider_name = spider_name
        self.path_to_settings = path_to_settings
        self.crawl_function = crawl_function
        self.process = None

    def stop(self):
        if self.process:
            self.process.terminate()

    def run(self):
        self.process = Process(target=self.crawl_function,
                               args=(self.path_to_settings, self.spider_name,))
        self.process.start()
        self.process.join()
