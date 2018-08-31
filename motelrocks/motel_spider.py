import re

from motelrocks.items import MotelItem
from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MotelRocksSpider(CrawlSpider):
    name = 'motelrocksSpider'
    start_urls = ['http://www.motelrocks.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@id="nav-menu"]/li'), callback='parse_pages'),
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class, "xProductDetails")]'), callback='parse_product_item'),
    )

    def parse_pages(self, response):
        last_page_number = self.parse_last_page_number(response)
        category_href = response.xpath('/html/head/link[14]/@href').extract_first()
        if category_href:
            category_id = re.search('categoryid=(.+?)&', category_href).group(1)
        for index in range(1, last_page_number):
            yield FormRequest(url="http://www.motelrocks.com/categories_ajax.php",
                              method='POST',
                              formdata={'page': str(index), 'invocation': 'page', 'categoryid': category_id})

    def parse_product_item(self, response):
        item = MotelItem()
        item['name'] = self.parse_name(response)
        item['category'] = self.parse_category(response)
        item['retailer_sku'] = self.parse_retailer_sku(response)
        item['description'] = self.parse_description(response)
        item['img_urls'] = self.parse_imgurls(response)
        item['url'] = self.parse_url(response)
        item['brand'] = self.parse_brand()
        item['gender'] = self.parse_gender()
        item['sku'] = self.parse_sku(response)
        yield item

    def parse_last_page_number(self, response):
        return int(response.xpath('//div[contains(@class, "pageitem")]/text()').extract()[-2])

    def parse_name(self, response):
        return response.xpath('//h1[contains(@class,"text-center")]/text()').extract_first()

    def parse_brand(self):
        return "Motelrocks"

    def parse_category(self, response):
        return response.xpath('//ul[contains(@class,"breadcrumbs")]/li[2]/a/span/text()').extract_first()

    def parse_description(self, response):
        return response.xpath('//div[contains(@class,"content active" )]/p[2]/span/text()').extract()

    def parse_url(self, response):
        return response.url

    def parse_imgurls(self, response):
        return response.xpath('//li[contains(@class, "prodpicsidethumb")]/img/@src').extract()

    def parse_gender(self):
        return "F"

    def parse_retailer_sku(self, response):
        return response.xpath('//form[@id="productDetailsAddToCartForm"]/input/@value').extract()[1]

    def parse_currency_price(self, response):
        currency_price = response.xpath('//em[contains(@class, "ProductPrice VariationProductPrice")]/text()').extract_first()
        if currency_price:
            currency = currency_price[:1]
            price = currency_price[1:]
            return currency, price
        else:
            currency_price = response.xpath('//span[contains(@class, "SalePrice")]/text()').extract_first()
            currency = currency_price[:1]
            price = currency_price[1:]
            return currency, price

    def parse_colour(self, response):
        return response.xpath('//a[contains(@class, "colswatch")]/@title').extract()

    def parse_sizes(self, response):
        sizes = response.xpath('//li[contains(@class, "sizeli sizeli-unselected")]/text()').extract()
        for index in range(len(sizes)):
            sizes[index] = sizes[index].replace('\r', '')
            sizes[index] = sizes[index].replace('\t', '')
            sizes[index] = sizes[index].replace('\n', '')
        sizes = list(filter(None, sizes))
        return sizes

    def parse_sku(self, response):
        size_codes = response.xpath('//li[contains(@class, "sizeli sizeli-unselected")]/@rel').extract()
        sizes = self.parse_sizes(response)
        product_id = self.parse_retailer_sku(response)
        currency, price = self.parse_currency_price(response)
        for index in range(len(size_codes)):
            product_code = "{}_{}".format(product_id, sizes[index])
            if index == 0:
                sku = {
                    product_code: {
                        "price": price,
                        "currency": currency,
                        "colour": self.parse_colour(response),
                        "size_code": size_codes[index]
                    }
                }
            else:
                sku[product_code] = {
                    "price": price,
                    "currency": currency,
                    "colour": self.parse_colour(response),
                    "size_code": size_codes[index]
                }
        return sku
