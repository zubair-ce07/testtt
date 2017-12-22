import copy
from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .item import ItemSpider


class JosephSpider(CrawlSpider):
    name = 'joseph_spider'
    allowed_domains = ['joseph-fashion.com']
    start_urls = ["http://www.joseph-fashion.com/en-us/home"]

    rules = (
        Rule(LinkExtractor(
            restrict_css='a[class*="navigation__link"]'), callback='parse'),
        Rule(LinkExtractor(restrict_css='.search-result-content .thumb-link'),
             callback='parse_product'),
    )

    def parse(self, response):

        for request in super().parse(response):
            data = response.meta.get('data') or dict()
            data = copy.deepcopy(data)
            data['trail'] = data.get('trail') or list()
            data['trail'].append(request.url)
            request.meta['data'] = data
            yield request

    def parse_product(self, response):
        data = response.meta.get('data') or dict()
        data['trail'] = data.get('trail') or list()
        data["trail"].append(response.url)

        brand_xpath = "//meta[@itemprop='brand']/@content"
        name_xpath = "//h1[@itemprop='name']/text()"
        images_xpath = "//div[@id='thumbnails']//img/@src"
        retailer_sku = "//meta[@itemprop='SKU']/@content"
        care_xpath = "//div[./label[@for='tab-2']]/div[@class='tab-content']/text()"
        descriptions_xpath = "//div[./label[@for='tab-1']]/div[@class='tab-content']/text()"

        data["market"] = "US"
        data["retailer"] = "joseph-us"
        referrer = data['trail'][0]
        data["category"] = urlparse(referrer).path.split('/')[-2]
        data["brand"] = response.xpath(brand_xpath).extract_first()
        data["name"] = response.xpath(name_xpath).extract_first()
        data["care"] = response.xpath(care_xpath).extract()
        data["description"] = response.xpath(descriptions_xpath).extract()
        data["image_urls"] = response.xpath(images_xpath).extract()
        data["retailer_sku"] = response.xpath(retailer_sku).extract_first()
        data["gender"] = "women" if "women" in referrer else "men"

        return self.item_skus(response, data)

    def item_skus(self, response, data):
        item_spider = ItemSpider()
        data["skus"] = {}
        colors = response.xpath("//ul[contains(@class, 'color')]//a")
        for color in colors:
            request = response.follow(
                color, item_spider.parse)
            request.meta["product"] = data
            yield request
