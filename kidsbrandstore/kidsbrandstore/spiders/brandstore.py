import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from kidsbrandstore.items import KidsbrandstoreItem


class BrandStoreSpider(CrawlSpider):
    name = 'brandstore'
    allowed_domains = ['kidsbrandstore.de']
    start_urls = ['http://kidsbrandstore.de/']

    rules = (
        Rule(LinkExtractor(allow="https://kidsbrandstore\.de/[\w-]*/", deny='\.html'), callback='parse'),
        Rule(LinkExtractor(allow="https://kidsbrandstore\.de/[\w-]*", deny='\.html'), callback='parse_item'),
        )

    def parse(self, response):
        product_urls = response.xpath("//div[@class='bottom-product-grid']/a/@href").getall()
        for url in product_urls:
            yield scrapy.Request(response.urljoin(url).replace(':443', ''), callback=self.parse_item)

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href).replace(':443', ''), self.parse)

    def parse_item(self, response):
        product = KidsbrandstoreItem()
        product['retailer_sku'] = response.css('span.product_id::text').extract_first()
        product['category'] = response.css('span.category::text').extract_first()
        product['brand'] = response.css('span.brand::text').extract_first()
        product['url'] = response.url
        product['name'] = response.css('span.name::text').extract_first()
        product['description'] = response.css('span.description::text').extract_first()
        product['care'] = (response.xpath('//div[@class="product-information-wrapper"]/p/text()').extract()[-1]
                           if response.xpath('//div[@class="product-information-wrapper"]/p/text()').extract()
                           else None)
        product['image_urls'] = response.xpath('//figure//a//img/@src').extract()
        product['skus'] = []
        product['price'] = response.css('span.price::text').extract_first()
        product['currency'] = response.css('span.price_currency_code::text').extract_first()

        product_list = "".join(response.xpath('//div[@id="product-list-also-check"]/p/a/text()').extract())
        if response.xpath('//svg').extract():
            product['gender'] = "boys/girls"
        elif "jungen" in product_list:
            product['gender'] = "boys"
        elif "mädchen" in product_list:
            product['gender'] = "girls"
        else:
            product['gender'] = "unisex-kids"

        color = (response.css('span.desktop-header::text').extract_first().split('-')[-1].replace('.', '').replace(' ', '')
                 if response.css('span.desktop-header::text').extract() else None)
        sizes = response.xpath('//label[@class="attribute-title"]/text()').extract()

        for size in sizes:
            product['skus'].append({
                "colour": color,
                "price": product['price'],
                "currency": product['currency'],
                "size": size,
                "sku_id": f'{color}_{size}'
                })
        yield product
