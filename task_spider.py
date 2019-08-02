import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ClothesItem


class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    allowed_domains = ['descente.com']
    start_urls = [
        'https://athletic.descente.com'
    ]

    def parse(self, response):
        link_extractor = LinkExtractor(allow=r"/collections/best-sellers")
        link_extractor = link_extractor.extract_links(response)

        if len(link_extractor) != 0:
            for link in link_extractor:
                yield scrapy.Request(str(link.url), callback=self.parse_product_page)

    def parse_product_page(self, response):
        link_extractor = LinkExtractor(allow=r"/products/dmmnja72u")
        link_extractor = link_extractor.extract_links(response)

        if len(link_extractor) != 0:
            for link in link_extractor:
                yield scrapy.Request(str(link.url), callback=self.parse_item)

    def parse_item(self, response):
        items = ClothesItem()

        url_split = response.url.split('/')
        category = []
        for i in range(3, len(url_split) - 1):
            category.append(url_split[i])

        items['retailer_sku'] = url_split[-1]
        items['category'] = category
        items['brand'] = 'Athletic Descente'
        items['url'] = response.url
        items['name'] = response.css('h1::text').get()
        items['description'] = self.extract_description(response)
        items['care'] = self.extract_care(response)
        items['image_urls'] = self.extract_image_urls(response)
        items['skus'] = self.extract_skus(response)

        yield items

    def extract_skus(self, response):
        sku_ids = response.xpath('//form/select/option/@data-sku').getall()
        sizes = response.xpath('//form/select/option/@data-option1').getall()
        colours = response.xpath('//form/select/option/@data-option2').getall()
        prices = response.xpath('//form/select/option/@data-price').re('\d.*')
        currencies = response.xpath('//form/select/option/text()').getall()
        for i in range(len(currencies)):
            currencies[i] = currencies[i].strip()
            currencies[i] = currencies[i].split(' ')[-1]

        skus = []
        for i in range(len(sku_ids)):
            sku_dict = {
                "price": float(prices[i]) * 100,
                "currency": currencies[i],
                "size": sizes[i],
                "colour": colours[i],
                "sku_id": sku_ids[i]
            }
            skus.append(sku_dict)
        return skus

    def extract_description(self, response):
        desc = response.xpath('//div[@class="product-description-internal"]/p/text()').getall() \
               + response.xpath('//div[@class="specifics-inner"]/ul/li/ul/li/text()').getall()
        description = []
        for i in range(len(desc)):
            description += [d for d in desc[i].split('.') if d.strip() != '']
        return description

    def extract_care(self, response):
        care__ = []
        care = response.xpath('//div[@class="specifics-inner"]/ul/li/text()')[-1].getall()
        for i in range(len(care)):
            care__ = [c for c in care[i].split('.') if c != '']
        return care__

    def extract_image_urls(self, response):
        image_urls = response.xpath('//div[@class="slick-slider product-images-slider"]/div/img/@src').getall()
        for i in range(len(image_urls)):
            image_urls[i] = "http:" + image_urls[i]
        return image_urls
