import scrapy
from scrapy.loader import ItemLoader

from amazon_scrapper.items import Product


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/most-wished-for/']

    def parse(self, response):
        department_urls = response.xpath('//ul[@id="zg_browseRoot"]//ul//li//a/@href').extract()
        for url in department_urls:
            yield scrapy.Request(url, self.parse_products)

    def parse_products(self, response):
        products = response.xpath('//div[@id="zg_centerListWrapper"]//div[@class="a-section a-spacing-none p13n-asin"]')
        sle_name = './/div[re:test(@class, "p13n-sc-truncate p13n-sc-truncated-hyphen p13n-sc-line-clamp-\d$")]/text()'

        for product in products:
            url = product.xpath('./a/@href').extract_first().split('?')[0]
            loader = ItemLoader(item=Product(), selector=product)
            loader.add_xpath('name', sle_name)
            loader.add_xpath('price', './/span[@class="p13n-sc-price"]/text()')
            loader.add_xpath('rating', './/div[@class="a-icon-row a-spacing-none"]/a/i/span/text()')
            loader.add_value('ASIN', url.split('/')[-1])
            loader.add_value('department', response.request.url.split('/')[-1])
            loader.add_value('source_url', response.urljoin(url))
            loader.add_xpath('image_url', './/img/@src')
            yield loader.load_item()

        next_page = response.xpath('//li[@class="zg_page zg_selected"]/following-sibling::li[1]/a/@href').extract_first()

        if next_page is not None and next_page != '':
            yield scrapy.Request(next_page, self.parse_products)
