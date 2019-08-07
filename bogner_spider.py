from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BognerItem


class BognerSpider(CrawlSpider):
    name = "bogner"
    allowed_domains = ['bogner.com']
    start_urls = [
        'https://www.bogner.com/en-gb/women.html'
    ]
    rules = (
        Rule(LinkExtractor(allow=("/women", "/men",), restrict_xpaths='//nav[@id="nav"]//li[@class="level2   "]//a')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="toolbar-bottom"]//a[@class="next i-next"]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="product-image is-visible-default"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        items = BognerItem()

        items['url'] = response.url
        items['retailer_sku'] = self.extract_retailer_sku(response)
        items['category'] = self.extract_category(response)
        items['gender'] = items['category'][0]
        items['brand'] = self.extract_brand(response)
        items['name'] = self.extract_name(response)
        items['description'] = self.extract_description(response)
        items['care'] = self.extract_care(response)
        items['image_urls'] = self.extract_image_urls(response)
        items['price'] = self.extract_price(response)
        items['currency'] = "GBP"
        items['retailer'] = self.extract_retailer(response)
        items['market'] = items['retailer'].split(' ')[-1]
        items['skus'] = self.extract_skus(response, items['price'])

        yield items

    def extract_retailer_sku(self, response):
        return response.xpath('//p[@class="sku"]/text()').re_first('\d+')

    def extract_category(self, response):
        return response.xpath('//div[@class="breadcrumbs"]/ul/li/a/span/text()')[1:].getall()

    def extract_brand(self, response):
        return response.xpath('//h2[@class="collection-name"]/text()').get()

    def extract_name(self, response):
        return response.xpath('//h1[@class="product-name-text"]/text()').get().strip()

    def extract_retailer(self, response):
        return response.xpath('//title/text()').re_first('\|.*').split('|')[-1].strip()

    def extract_description(self, response):
        desc1 = response.css('.std p::text').get()
        desc2 = response.xpath('//div[@class="accordion-content-container"]/'
                               'div[@class="product-features"]/ul/li/text()').getall()
        description = [d for d in desc1.split('.') if d.strip() != ''] + desc2
        return description

    def extract_care(self, response):
        care1 = response.xpath('//div[@class="accordion-content-container"]/div[@class="material-care-container"]'
                               '/div[@class="material-composition-container"]/p/text()').getall()

        care2 = response.xpath('//div[@class="accordion-content-container"]/div[@class="material-care-container"]'
                               '/div[@class="material-care-tip"]/ul/li/p/text()').getall()
        return care1 + care2

    def extract_image_urls(self, response):
        return response.xpath('//div[@class="view-gallery-slider is-unified-slider"]/div/div/img/@data-src').getall()

    def extract_price(self, response):
        price_xpath = response.xpath('//div[@class="price-container"]')[1]
        price = price_xpath.xpath('./div[@class="price-box"]//span[@class="price"]/text()').re_first('\d+\.?\d*')
        return float(price) * 100

    def extract_skus(self, response, price):
        colours_xpath = response.xpath('//ul[@id="colorswatch-select"]')[1]
        colours = colours_xpath.xpath('.//span/text()').getall()

        sizes_xpath = response.xpath('//div[@id="product-options-wrapper"]//ul[@class="product-sizes"]')
        sizes = []
        if sizes_xpath:
            sizes_xpath = sizes_xpath[1]
            sizes = sizes_xpath.xpath('.//li/@data-size-label').getall()

        availability_xpath = response.xpath('//div[@id="product-options-wrapper"]//ul[@class="product-sizes"]')
        availability = []
        if availability_xpath:
            availability_xpath = availability_xpath[1]
            availability = availability_xpath.xpath('.//li/@data-size-availability').getall()

        skus = []
        if len(sizes) != 0:
            skus = self.skus_with_size(colours, sizes, availability, price)
        else:
            skus = self.skus_without_sizes(colours, price)
        return skus

    def skus_with_size(self, colours, sizes, availability, price):
        skus = []
        for colour in colours:
            for size, stock in zip(sizes, availability):
                if stock == 'sold out':
                    sku = {
                        'sku_id': f"{colour}_{size}",
                        'price': price,
                        'currency': "GBP",
                        'size': size,
                        'colour': colour,
                        'out-of-stock': True
                    }
                else:
                    sku = {
                        'sku_id': f"{colour}_{size}",
                        'price': price,
                        'currency': "GBP",
                        'size': size,
                        'colour': colour
                    }
                skus.append(sku)
        return skus

    def skus_without_sizes(self, colours, price):
        skus = []
        for colour in colours:
            sku = {
                'sku_id': colour,
                'price': price,
                'currency': "GBP",
                'colour': colour
            }
            skus.append(sku)
        return skus
