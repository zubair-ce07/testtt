import json
import re

import scrapy

from SchwabSpider.items import SchwabProduct
from SchwabSpider.spiders.mixin import Mixin


class ProductSpider(scrapy.Spider, Mixin):
    name = 'schwab-parse'
    item_info_url = "https://www.schwab.de/request/itemservice.php?fnc=getItemInfos"
    product_api_url = "https://www.schwab.de/index.php?"
    seen_ids = list()

    def parse(self, response):
        retailer_id = self.product_retailer(response)
        if [product_id for product_id in self.seen_ids if retailer_id == product_id]:
            return self.next_action(response)

        self.seen_ids.append(retailer_id)
        product = SchwabProduct()
        product["category"] = self.product_category(response)
        product["description"] = self.product_descriptions(response)
        product["care"] = self.product_cares(response)
        product["retailer_sku"] = retailer_id
        product["image_urls"] = self.product_images(response)
        product["name"] = self.product_name(response).strip()
        product["brand"] = self.product_brand(response)
        product["market"] = "DE"
        product["retailer"] = "schwab-de"
        product["url"] = response.url

        product["skus"] = dict()
        sub_requests = self.create_sku_requests(response)
        sub_requests.append(self.create_info_request(response))
        response.meta["product"] = product
        response.meta["remaining_request"] = sub_requests
        return self.next_action(response)

    def parse_info(self, response):
        jsonresponse = json.loads(response.text)
        response.meta["information"] = jsonresponse
        return self.next_action(response)

    def parse_skus(self, response):
        product = response.meta.get("product")
        skus = product.get("skus")
        key, current_sku = self.sku(response)
        skus[key] = current_sku
        response.meta["remaining_request"].append(
            self.create_image_request(response))
        return self.next_action(response)

    def sku(self, response):
        sku = dict()
        sku["price"] = self.product_price(response)
        sku["currency"] = self.product_currency(response)
        sku["colour"] = self.product_current_colour_name(response)
        sku["size"] = self.product_current_size_name(response)
        if not self.product_available(response):
            sku["out_of_stock"] = True
        key = f'{sku["colour"]}_{sku["size"]}_{self.current_variant_name(response)}'
        return key, sku

    def parse_images(self, response):
        product = response.meta.get("product")
        product["image_urls"] = list(set().union(product[
            "image_urls"], self.product_images(response)))
        return self.next_action(response)

    def create_info_request(self, response):
        request_body = 'items='+self.article_string(response)[0]
        request = scrapy.Request(self.item_info_url,
                                 method="POST",
                                 body=request_body,
                                 headers={
                                     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                                 callback=self.parse_info)
        return request

    def create_sku_requests(self, response):
        multiple_requests = []
        for article in self.product_articles(response):
            form_data = {
                'cl': self.product_form_data_cl(response),
                'anid': article.get('number'),
                'ajaxdetails': 'ajaxdetailsPage',
            }
            request = scrapy.FormRequest(
                url=self.product_api_url, formdata=form_data, callback=self.parse_skus)
            multiple_requests.append(request)
        return multiple_requests

    def create_image_request(self, response):
        field = self.product_current_colour_field(response)
        colour_id = self.product_current_colour_id(response)
        form_data = {
            'cl': 'oxwarticledetails',
            'anid': self.product_current_article_id(response),
            'ajaxdetails': 'adsColorChange',
            'varselid[2]': colour_id,
            'varselid[1]': '',
            'varselid[0]': ''
        }
        request = scrapy.FormRequest(
            url=self.product_api_url, method="GET", formdata=form_data, callback=self.parse_images)
        return request

    def product_category(self, response):
        catogories = response.css(
            '.breadcrumb [itemprop="name"]::text').extract()
        return [category.strip() for category in catogories]

    def product_descriptions(self, response):
        descriptions_xpath = ".//div[@itemprop='description']/text()"
        descriptions = response.xpath(descriptions_xpath).extract()
        return [description.strip() for description in descriptions]

    def product_cares(self, response):
        care_xpath = './/ul[@class="l-outsp-bot-5"]//li/text()'
        cares = response.xpath(care_xpath).extract()
        return [care.strip() for care in cares]

    def product_retailer(self, response):
        return response.xpath('.//input[@name="parentid"]/@value').extract_first()

    def product_images(self, response):
        images_xpath = './/a[@id="magic"]/@href'
        return ["http:" + url for url in response.xpath(images_xpath).extract()]

    def product_name(self, response):
        name_xpath = ".//span[@itemprop='name']/text()"
        return response.xpath(name_xpath).extract_first()

    def product_brand(self, response):
        brand_css = ".details__brand img::attr(alt)"
        return response.css(brand_css).extract_first()

    def product_price(self, response):
        xpath = './/span[@class="js-detail-price"]/text()'
        price_text = response.xpath(xpath).extract_first()
        price_text = price_text.strip().replace(',', '')
        return int(price_text)

    def product_currency(self, response):
        return response.xpath('.//meta[@itemprop="priceCurrency"]/@content').extract_first()

    def product_form_data_cl(self, response):
        return response.css('#detailsMain input[name="cl"]::attr(value)').extract_first()

    def product_id(self, response):
        return response.xpath('.//input[@name="parentid"]/@value').extract_first()

    def article_string(self, response):
        text = response.xpath(
            '//script[contains(text(),"articlesString")]/text()').extract_first()
        articles_string = re.findall(
            r"\$\.kalrequest.articlesString\('(.+)',1,w", text)
        return articles_string

    def product_articles(self, response):
        articles_string = self.article_string(response)[0]
        article_ids = articles_string.split(';')
        parent_id = self.product_id(response)
        articles = []
        for _id in article_ids:
            item = dict()
            item["colour"], item["version"], item["size"] = _id.split('|')[
                1:]
            item_number = f'{parent_id}-{item["colour"]}-{item["size"]}-{item["version"]}'
            item["number"] = item_number
            articles.append(item)
        return articles

    def product_available(self, response):
        information = response.meta.get("information")
        avalability_info = information.get(
            self.product_current_article_number(response))
        available = avalability_info.get(
            self.product_current_size(response), "ausverkauft")
        if "ausverkauft" == available:
            return False
        return True

    def product_current_article_number(self, response):
        return response.xpath('.//input[@name="artNr"]/@value').extract_first()

    def product_current_article_id(self, response):
        return response.xpath('.//input[@name="anid"]/@value').extract_first()

    def product_current_colour_field(self, response):
        selector = ".js-varselid-COLOR::attr(name)"
        current_colour_field = response.css(selector).extract_first()
        return current_colour_field

    def product_current_colour_id(self, response):
        selector = ".js-varselid-COLOR::attr(value)"
        current_colour_id = response.css(selector).extract_first()
        return current_colour_id

    def product_current_colour_name(self, response):
        selector = ".js-current-color-name::attr(value)"
        current_colour = response.css(selector).extract_first()
        return current_colour

    def current_variant_name(self, response):
        selector = ".js-current-variant-name::attr(value)"
        variant = response.css(selector).extract_first()
        return variant

    def product_current_size(self, response):
        return self.product_current_size_name(response).split(' ')[0].split('/')[0]

    def product_current_size_name(self, response):
        selector = ".js-current-size-name::attr(value)"
        current_size = response.css(selector).extract_first()
        return current_size

    def next_action(self, response):
        sub_requests = response.meta.get("remaining_request")
        if not sub_requests:
            return response.meta.get("product")

        request = sub_requests.pop()
        request.meta["product"] = response.meta.get("product")
        request.meta["information"] = response.meta.get("information")
        request.meta["remaining_request"] = response.meta.get(
            "remaining_request")
        return request
