import re
import copy

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from schutzcrawler.items import ProductItem
from schutzcrawler.PriceExtractor import PriceExtractor
from schutzcrawler.spiders.schutz_parse import ParseSpider
from schutzcrawler.mixins import Mixin


class SchutzSpider(CrawlSpider, Mixin):
    name = f"{Mixin.name}crawl"

    default_xpaths = ['//div[@class="sch-main-menu-sub-links-left"]',
                      '//div[@class="sch-main-menu-sub-links-right"]',
                      '//ul[@class="pagination"]/li[@class="next"]']
    product_xpath = '//a[@class="sch-category-products-item-link"]'
    parser = ParseSpider()
    
    # Follow any link scrapy finds (that is allowed and matches the patterns).
    rules = [Rule(LinkExtractor(restrict_xpaths=default_xpaths), callback='parse'),
             Rule(LinkExtractor(restrict_xpaths=product_xpath
             ), callback=parser.parse, follow=True)]
 
    def parse(self, response):
        requests = super(SchutzSpider, self).parse(response)
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        for request in requests:
            trail = copy.deepcopy(trail)
            request.meta['trail'] = trail
            yield request
