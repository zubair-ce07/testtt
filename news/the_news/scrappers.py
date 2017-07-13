__author__ = 'luqman'
import os
import threading
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process
from the_news.models import NewsPaper
import the_news.settings as crawler_settings


def run_scrapy_project(path_to_settings, spider_name, scrapy_settings):
    os.environ['SCRAPY_SETTINGS_MODULE'] = path_to_settings
    runner = CrawlerRunner(scrapy_settings)
    runner_crawler = runner.crawl(spider_name)
    runner_crawler.addBoth(lambda _: reactor.stop())
    # the script will block here until the crawling is finished
    reactor.run(installSignalHandlers=False)


def initialize_spiders(scrapy_settings, **scrapy_spiders_thread):
    spider_names = NewsPaper.objects.values('spider_name')
    for spider_name in spider_names:
        if spider_name:
            scrapy_spiders_thread[spider_name] = CrawlSpiderThread(spider_name,
                                                                    'news_scrappers.settings',
                                                                    scrapy_settings,
                                                                    run_scrapy_project)

class CrawlSpiderThread(threading.Thread):
    def __init__(self, spider_name, path_to_settings, scrapy_settings, crawl_function):
        threading.Thread.__init__(self)
        self.spider_name = spider_name
        self.path_to_settings = path_to_settings
        self.crawl_function = crawl_function
        self.scrapy_settings = scrapy_settings
        self.process = None

    def stop(self):
        crawler_settings.CRAWLER_STATE = False
        if self.process:
            self.process.terminate()

    def run(self):
        self.process = Process(target=self.crawl_function,
                               args=(self.path_to_settings, self.spider_name, self.scrapy_settings,))
        crawler_settings.CRAWLER_STATE = True
        crawler_settings.CRAWLER_NAME = self.spider_name
        crawler_settings.CRAWLER_THREAD = self
        self.process.start()
        self.process.join()
