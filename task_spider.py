from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ClothesItem
import re


class ClothesSpider(CrawlSpider):
    name = 'clothes'
    allowed_domains = ['descente.com']
    start_urls = [
        'https://athletic.descente.com'
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="row standard-product-list"]//a[@class="product-title"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths=['//div[@id="menu1Dropdown"]//a', '//div[@id="menu2Dropdown"]//a',
                                            '//div[@class="col-12 pagination"]/span[@class="next"]/a'])),
    )
    retailer_skus_all = set()

    def parse_item(self, response):
        items = ClothesItem()
        url_split = response.url.split('/')

        if self.check_if_parsed(url_split[-1]):
            return
        else:
            items['retailer_sku'] = url_split[-1]
            items['category'] = self.extract_category(response)
            items['brand'] = self.extract_brand(response)
            items['url'] = response.url
            items['name'] = self.extract_name(response)
            items['description'] = self.extract_description(response)
            items['care'] = self.extract_care(response)
            items['image_urls'] = self.extract_image_urls(response)
            items['skus'] = self.extract_skus(response)
            yield items

    def check_if_parsed(self, retailer_sku):
        if retailer_sku in self.retailer_skus_all:
            return True
        else:
            self.retailer_skus_all.add(retailer_sku)
            return False

    def extract_name(self, response):
        return response.css('h1::text').get()

    def extract_category(self, response):
        return response.xpath('//div[@class="breadcrumb-container"]/a[@title="Products"]/text()').getall()

    def extract_brand(self, response):
        brand = re.findall("var item = {(.+)};", response.body.decode("utf-8"), re.S)
        brand = re.findall("Brand: (.+?),", brand[0], re.S)
        return brand[0] if brand else "Athletic Descente"

    def extract_skus(self, response):
        skus = []
        skus_xpath = response.xpath('//form/select/option')
        for raw_sku in skus_xpath:
            sku_id = raw_sku.xpath('./@data-sku').get()
            size = raw_sku.xpath('./@data-option1').get()
            colour = raw_sku.xpath('./@data-option2').get()
            price = raw_sku.xpath('./@data-price').re_first('\d.*')
            currency = raw_sku.xpath('./text()').get()
            currency = currency.strip()
            currency = currency.split(' ')[-1]

            sku_dict = {
                "price": float(price) * 100,
                "currency": currency,
                "size": size,
                "colour": colour,
                "sku_id": sku_id
            }
            skus.append(sku_dict)
        return skus

    def extract_description(self, response):
        desc_all = response.xpath('//div[@class="product-description-internal"]/p/text() | '
                                  '//div[@class="specifics-inner"]/ul/li/ul/li/text()').getall()
        description = []
        for desc in desc_all:
            description += [d for d in desc.split('.') if d.strip()]
        return description

    def extract_care(self, response):
        care = []
        care_all = response.xpath('//div[@class="specifics-inner"]/ul/li/text()')
        if care_all:
            care_all = care_all[-1].getall()
            for care_element in care_all:
                care = [c for c in care_element.split('.') if c.strip()]
        return care

    def extract_image_urls(self, response):
        xpath = '//div[@class="slick-slider product-images-slider"]/div/img/@src'
        return [f"http:{i}" for i in response.xpath(xpath).getall()]
