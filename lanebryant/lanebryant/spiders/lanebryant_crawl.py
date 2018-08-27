from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from lanebryant.lanebryant_parser import ProductParser


class LanebryantCrawlSpider(CrawlSpider):
    name = 'lanebryant-crawl'
    allowed_domains = ['www.lanebryant.com']
    lanebryant_parser = ProductParser()
    start_urls = [
        # 'http://www.lanebryant.com/'
        'https://www.lanebryant.com/apparel/dresses/view-all/P-11072'
    ]

    rules = (
        # Rule(LinkExtractor(restrict_css="[role='navigation']"), callback='parse_category'),
        Rule(LinkExtractor(restrict_css='.mar-prd-item-image '), callback='parse_item'),
    )

    # def parse(self, response):
    #     title = response.css('.refinement-header::text').extract_first(default='').strip()
    #     trail = response.meta.get('trail', [])
    #     trail.append([title, response.url])
    #     for request in super().parse(response):
    #         request.meta['trail'] = trail.copy()
    #         yield request

    def parse_item(self, response):
        # print(f"ITEM IS: {response.css('.mar-product-title::text').extract_first()}")
        print(self.lanebryant_parser.doit(response))
        # print(f"processing {response.url}")
