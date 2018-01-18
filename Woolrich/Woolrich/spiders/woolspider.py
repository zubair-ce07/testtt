from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule

from Woolrich.spiders.mixin import Mixin

from Woolrich.spiders.parser import Parser


class WoolRichSpider(CrawlSpider, Mixin):
    name = "WoolRich"
    parser = Parser()
    css_classes = [
        '.nav.navbar-nav .upper',
        '.nav.nav-list.nav-',
        '.clear.addMore'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=css_classes, tags=['a', 'div'], attrs=['href', 'nextpage'])
             ),
        Rule(
            LinkExtractor(restrict_css='.productCard'), callback=parser.parse_product
        )
    )
