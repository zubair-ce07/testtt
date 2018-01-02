import re

import scrapy

from SchwabSpider.spiders.mixin import Mixin
from SchwabSpider.spiders.sku import SkuSpider


class ProductSpider(scrapy.Spider, Mixin):
    name = 'product_spider'
    item_info_url = "https://www.schwab.de/request/itemservice.php?fnc=getItemInfos"

    def parse(self, response):
        sku_spider = SkuSpider()
        product = response.meta.get('product') or dict()
        product["category"] = self.category(response)
        product["description"] = [desc.strip()
                                  for desc in self.descriptions(response)]
        product["care"] = [care.strip() for care in self.cares(response)]
        product["retailer_sku"] = self.retailer(response)
        product["image_urls"] = self.images(response)
        product["name"] = self.item_name(response).strip()
        product["brand"] = self.brand(response)
        product["market"] = "DE"
        product["retailer"] = "schwab-de"
        product["url"] = response.url

        product["skus"] = dict()
        sub_requests = sku_spider.create_sku_requests(response)
        product["remaining_request"] = sub_requests
        request = self.create_info_request(response)
        request.meta["product"] = product

        yield request

    def category(self, response):
        return response.css('.breadcrumb [itemprop="name"]::text').extract()[-1].strip()

    def descriptions(self, response):
        descriptions_xpath = ".//div[@itemprop='description']/text()"
        return response.xpath(descriptions_xpath).extract()

    def cares(self, response):
        care_xpath = './/ul[@class="l-outsp-bot-5"]//li/text()'
        return response.xpath(care_xpath).extract()

    def retailer(self, response):
        return response.xpath('.//input[@name="parentid"]/@value').extract_first()

    def images(self, response):
        images_xpath = './/a[@id="magic"]/@href'
        return response.xpath(images_xpath).extract()

    def item_name(self, response):
        name_xpath = ".//span[@itemprop='name']/text()"
        return response.xpath(name_xpath).extract_first()

    def brand(self, response):
        brand_css = ".details__brand img::attr(alt)"
        return response.css(brand_css).extract_first()

    def create_info_request(self, response):
        sku_spider = SkuSpider()
        text = response.xpath(
            '//script[contains(text(),"articlesString")]/text()').extract_first()
        articles = re.findall(
            r"\$\.kalrequest.articlesString\((.+),1,w", text)
        form_data = {
            'items': articles
        }
        request = scrapy.FormRequest(
            url=self.item_info_url, formdata=form_data, callback=sku_spider.parse)
        return request
