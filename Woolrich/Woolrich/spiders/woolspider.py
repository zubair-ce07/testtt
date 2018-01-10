from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Woolrich.spiders.mixin import Mixin
from Woolrich.spiders.parser import Parser


class WoolRichSpider(CrawlSpider, Mixin):
    name = "WoolRich"
    parser = Parser()
    rules = (
        Rule(LinkExtractor(restrict_css='.nav.navbar-nav .upper'),
             ),
        Rule(LinkExtractor(restrict_css='.nav.nav-list.nav-'),
             ),
        Rule(LinkExtractor(restrict_css='.clear .addmore', tags=['div'], attrs=['nextpage'])
             ),
        Rule(
            LinkExtractor(restrict_css='.productCard'), callback=parser.parse_product
        )
    )
