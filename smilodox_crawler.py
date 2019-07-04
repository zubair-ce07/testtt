from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from smilodox_parser import SmiloDoxParser


class SmiloDoxCrawler(CrawlSpider, SmiloDoxParser):
    name = 'smilodox'
    allowed_domains = ['smilodox.com']
    start_urls = ['https://www.smilodox.com/']

    category_css = '.dropdown-menu .menu-level3'
    product_css = '.thumb'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css, attrs='data-href', tags='article'),
             callback='parse_item')
    )
