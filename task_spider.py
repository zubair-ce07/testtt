from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ClothesItem


class ClothesSpider(CrawlSpider):
    name = 'clothes'
    allowed_domains = ['descente.com']
    start_urls = [
        'https://athletic.descente.com'
    ]
    rules = (
        Rule(LinkExtractor(allow=("/products/dmmnja72u",)), callback='parse_item'),
        Rule(LinkExtractor(allow=("/collections/best-sellers", ))),
    )

    def parse_item(self, response):
        items = ClothesItem()
        url_split = response.url.split('/')

        items['retailer_sku'] = url_split[-1]
        items['category'] = self.extract_category(response)
        items['brand'] = 'Athletic Descente'
        items['url'] = response.url
        items['name'] = self.extract_name(response)
        items['description'] = self.extract_description(response)
        items['care'] = self.extract_care(response)
        items['image_urls'] = self.extract_image_urls(response)
        items['skus'] = self.extract_skus(response)

        yield items

    def extract_name(self, response):
        return response.css('h1::text').get()

    def extract_category(self, response):
        return response.xpath('//div[@class="breadcrumb-container"]/a[@title="Products"]/text()').getall()

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
            description += [d for d in desc.split('.') if d.strip() != '']
        return description

    def extract_care(self, response):
        care = []
        care_all = response.xpath('//div[@class="specifics-inner"]/ul/li/text()')[-1].getall()
        for care_element in care_all:
            care = [c for c in care_element.split('.') if c.strip() != '']
        return care

    def extract_image_urls(self, response):
        xpath = '//div[@class="slick-slider product-images-slider"]/div/img/@src'
        return [f"http:{i}" for i in response.xpath(xpath).getall()]
