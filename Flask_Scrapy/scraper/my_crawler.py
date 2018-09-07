from klein import route
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from scraper.scraper.deBijenkorfScraper import DeBijenkorfSpider
from scraper.database import db_session
from scraper.models import Item


class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """

    def __init__(self, settings=None):
        super().__init__(settings=settings)
        self.items = []

    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all items scraped

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        for item in self.items:
            db_item = Item(item)
            db_session.add(db_item)
        db_session.commit()
        reactor.stop()


@route('/forward/')
def schedule():
    if not reactor.running:
        runner = MyCrawlerRunner()
        spider = DeBijenkorfSpider()
        runner.crawl(spider)
        reactor.run(installSignalHandlers=False)
