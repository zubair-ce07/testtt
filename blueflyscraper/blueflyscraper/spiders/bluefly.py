import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from scrapy import Request
import json


class BlueflySpider(CrawlSpider):
    name = "bluefly"
    allowed_domains = ['bluefly.com']
    start_urls = ['http://www.bluefly.com/']
    rules = [Rule(LinkExtractor(allow=['/[A-Za-z]+\/index']), process_links='link_filtering',
                  callback="parse_category")]

    custom_settings = {
        "DOWNLOAD_DELAY": 10
    }

    def link_filtering(self, links):
        for link in links:
            link.url = link.url.replace('/index', '?pageSize=96')
        return links

    def parse_category(self, response):
        if response.meta.get('redirect_urls', [response.url])[0] == response.url:
            item_links = response.css('.mz-productlisting-title').xpath('@href').extract()
            for link in item_links:
                temp = urljoin(response.url, link.strip())
                yield Request(temp, callback=self.parse_blurefly_item)
            extracted_link = response.css('.mz-pagenumbers-next').xpath('@href').extract()
            for link in extracted_link:
                temp = urljoin(response.url, link.strip())
                yield Request(temp, callback=self.parse_category)

    def parse_blurefly_item(self, response):
        item = BlueflyItem()
        item['brand'] = self.get_brand(response)
        item['category'] = self.get_category(response)
        item['merch_info'] = self.get_merch_info(response)
        item['url_original'] = response.url
        item['product_id'] = self.get_product_id(response.url)
        item['image_urls'] = self.get_image_urls(response)
        item['product_title'] = self.get_product_title(response)
        item['description'] = self.get_description(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        arbitrary_item = ArbitraryItem()
        arbitrary_item['colour'] = self.get_colour(response)
        arbitrary_item['price'] = self.get_price(response)
        arbitrary_item['previous_prices'] = self.get_prev_prices(response)
        arbitrary_item['size'] = self.get_size(response)
        skus = SkusItem()
        skus.__setitem__(self.get_numeric_size(response), arbitrary_item)
        item['skus'] = skus
        return item

    def get_price(self, response):
        return response.css('div.mz-price::text').extract()[0].strip()

    def get_size(self, response):
        return response.css('.mz-productoptions-sizebox::text').extract()

    def get_prev_prices(self, response):
        return "".join(response.css(".mz-price.is-crossedout::text").extract()).strip()

    def get_colour(self, response):
        return response.css('.mz-productoptions-optionvalue::text').extract()[0]

    def get_product_id(self, url):
        url_pats = url.split("/")
        return url_pats[-1]

    def get_brand(self, response):
        return response.css('.mz-productbrand >a::text').extract()[0]

    def get_description(self, response):
        return response.css('.mz-productdetail-description::text').extract()+self.get_details(response)

    def get_details(self, response):
        return response.css('.mz-productdetail-props > li::text').extract()

    def get_care(self, response):
        return response.css('.mz-productdetail-props').xpath('li[contains(text(),"%")]/text()').extract()

    def get_category(self, response):
        return response.css('.mz-breadcrumb-link:not(.is-first)::text').extract()

    def get_merch_info(self, response):
        merch_info = response.css('.mz-price-message::text').extract()
        return merch_info[0] if merch_info else ""

    def get_image_urls(self, response):
        return response.css('.mz-productimages-thumbimage').xpath('@src').extract()

    def get_numeric_size(self, response):
        return response.css('.mz-productoptions-sizebox').xpath('@data-value').extract()[0]

    def get_product_title(self, response):
        temp = response.xpath('//script[@id="data-mz-preload-product"]/text()').extract()[0]
        product = Payload(temp)
        return product.content['productName']

    def get_gender(self, response):
        gender_val = response.css('.mz-breadcrumb-link:not(.is-first)::text').extract()[0]
        return gender_val if gender_val == "Men" or gender_val == "Women" or gender_val == "Kids" else "Undefined"


class BlueflyItem(scrapy.Item):
    product_id = scrapy.Field()
    merch_info = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    product_title = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()


class SkusItem(scrapy.Item):
    def __setitem__(self, key, value):
        self._values[key] = value


class ArbitraryItem(scrapy.Item):
    colour = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    size = scrapy.Field()


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
