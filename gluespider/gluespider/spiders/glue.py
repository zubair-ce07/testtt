from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from gluespider.spiders.mixin import Mixin
from gluespider.spiders.parse import ParseSpider


class GlueSpider(CrawlSpider, Mixin):
    name = 'glue_spider'
    parseSpider = ParseSpider()

    rules = (
        Rule(LinkExtractor(
            restrict_css='.level-3'), callback='parse'),
        Rule(LinkExtractor(
            restrict_xpaths='//*[contains(@class,"sli_grid_product")]/a'),
            callback=parseSpider.parse),
        Rule(LinkExtractor(
            restrict_css='.pageselectorlink'),
            callback='parse'),
    )

    def parse(self, response):
        current_url = response.url
        for request in super().parse(response):
            trail = response.meta.get('trail', list())
            exist = [url for url in trail if url == current_url]
            if not exist:
                trail.append(response.url)
            request.meta['trail'] = trail
            yield request
