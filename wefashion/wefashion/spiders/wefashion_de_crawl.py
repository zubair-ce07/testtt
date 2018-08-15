from urllib.parse import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from wefashion.wefashion_de_parse import ProductParser


class WefashionDeCrawlSpider(CrawlSpider):
    name = 'wefashion-de-crawl'
    wefashion_parser = ProductParser()
    allowed_domains = ['www.wefashion.de']
    start_urls = [
        'http://www.wefashion.de/'
    ]
    category_css = [
        '.header-top-level-menu',
        '#category-level-0'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse'),
        Rule(LinkExtractor(restrict_css='.product-image'),
             callback='parse_item',
             process_links='filter_product_links'),
    )

    def parse(self, response):
        title = response.css('.refinement-header::text').extract_first(default='').strip()
        trail = response.meta.get('trail', [])
        trail.append([title, response.url])

        for request in super().parse(response):
            request.meta['trail'] = trail.copy()
            yield request

    def filter_product_links(self, links):                  # Remove query string from url
        for link in links:
            new_link = urlparse(link.url)
            link.url = f"{new_link.scheme}://{new_link.netloc + new_link.path}"
        return links

    def parse_item(self, response):
        return self.wefashion_parser.parse(response)
