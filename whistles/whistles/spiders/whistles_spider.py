# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider


class WhistlesSpiderSpider(CrawlSpider):
    name = 'whistles'
    allowed_domains = ['www.whistles.com']
    start_urls = ['http://www.whistles.com/']

    rules = (
        # Rule(LinkExtractor(allow=r'women/\w+(?=\/[a-zA-Z]){3}/\w'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'(\w+\/){2}'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(deny='inspiration/')),
        # Rule(LinkExtractor(deny='account/')),
        # Rule(LinkExtractor(allow=r"/*", restrict_xpaths=["//a[contains(@class,'name-link')]"]), follow=True),
    )

    def parse(self, response):
        for href in response.xpath("//li[contains(@class, 'meganav-link')]/a/@href"):
            yield response.follow(href, callback=self.parse)

        next_page_href = response.xpath("//a[contains(@class,'page-next')]/@href").extract_first()
        if next_page_href:
            yield response.follow(next_page_href, callback=self.parse)

        for href in response.xpath("//a[contains(@class,'name-link')]/@href"):
            yield response.follow(href, callback=self.parse_item)

    def parse_item(self, response):

        item = dict()
        item['url'] = response.url
        item['product_name'] = response.xpath("//h1[contains(@class,'product-name')]/text()").extract_first()
        item['EAN'] = response.xpath("//p[contains(., 'EAN:')]/text()").extract_first()
        item['product_key'] = response.xpath("//p[contains(., 'Product Key:')]/text()").extract_first()
        item['composition'] = response.xpath("//p[contains(., 'Composition:')]/text()").extract_first()
        item['wash_care'] = response.xpath("//p[contains(., 'Wash care:')]/text()").extract_first()
        item['color'] = response.xpath("//p[contains(., 'Colour:')]/text()").extract_first()
        item['price'] = {
            'sale_price': response.xpath("//span[contains(@title, 'Sale Price')]/text()").extract_first(),
            'regular_price': response.xpath("//span[contains(@title, 'Regular Price')]/text()").extract_first()
        }
        description = response.xpath("(//div[contains(@class,'product-tabs')]/ul/li)")[0]
        item['description'] = list(filter((lambda x: len(x)), map(
            str.strip, description.xpath("./div/div/p/text()").extract())))  # Eliminating \n, \r and empty strings.
        item['sizes'] = list()
        for size in response.xpath("//li[contains(@class, 'emptyswatch')]"):
            item['sizes'].append({
                'size': size.xpath("./a/span/text()").extract_first(),
                'status': size.xpath("./a/@title").extract_first()
            })
        yield item
