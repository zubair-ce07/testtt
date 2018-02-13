from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from gluespider.spiders.mixin import Mixin
from gluespider.spiders.parse import ParseSpider


class GlueSpider(CrawlSpider, Mixin):
    name = 'glue_spider'
    parseSpider = ParseSpider()

    rules = (
        Rule(LinkExtractor(
            restrict_css=['.level-3', '.pageselectorlink']), callback='parse'),
        Rule(LinkExtractor(
            restrict_xpaths='//*[contains(@class,"sli_grid_product")]/a'),
            callback=parseSpider.parse)
        )

    def parse(self, response):
        current_url = response.url
        for request in super().parse(response):
            trail = response.meta.get('trail', list())
            trail.append(response.url)
            request.meta['trail'] = trail
            yield request
