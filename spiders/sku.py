import json
import re

import scrapy

from SchwabSpider.spiders.mixin import Mixin


class SkuSpider(scrapy.Spider, Mixin):
    name = 'sku_spider'
    product_api_url = "https://www.schwab.de/index.php?"

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        product = response.meta.get("product")
        product["information"] = jsonresponse
        return self.next_action(response)

    def parse_product(self, response):
        product = response.meta.get("product")
        skus = product.get("skus")

        sku = dict()
        sku["price"] = self.price(response)
        sku["currency"] = self.currency(response)
        sku["colour"] = self.current_colour_name(response)
        sku["size"] = self.current_size_name(response)
        if not self.available(response):
            sku["out_of_stock"] = True
        item_key = f'{sku["colour"]}_{sku["size"]}'
        skus[item_key] = sku
        return self.next_action(response)

    def price(self, response):
        return response.xpath('.//span[@class="js-detail-price"]/text()').extract_first().strip()

    def currency(self, response):
        return response.xpath('.//meta[@itemprop="priceCurrency"]/@content').extract_first()

    def form_data_cl(self, response):
        return response.xpath('.//input[@name="cl"]/@value').extract()[3]

    def product_id(self, response):
        return response.xpath('.//input[@name="parentid"]/@value').extract_first()

    def articles(self, response):
        text = response.xpath(
            '//script[contains(text(),"articlesString")]/text()').extract_first()
        articles_ids = re.findall(
            r'\b\d+\b.\b\d+\b.[A-Za-z0-9]+\S[A-Za-z0-9,]+', text)
        parent_id = self.product_id(response)
        articles = []
        for i in articles_ids:
            codes = i.split('|')
            article = dict()
            article.update({"colour": codes[1]})
            article.update({"version": codes[2]})

            article.update({"size": codes[3]})
            article_number = (parent_id + "-" +
                              codes[1]) + "-" + codes[3] + "-" + codes[2]
            article.update({"number": article_number})
            articles.append(article)
        return articles

    def available(self, response):
        product = response.meta.get("product")
        information = product.get("information")
        avalability_info = information.get(
            self.current_article_number(response))
        available = avalability_info.get(
            self.current_size(response)[0], "ausverkauft")
        if "ausverkauft" == available:
            return False
        return True

    def current_article_number(self, response):
        return response.xpath('.//input[@name="artNr"]/@value').extract_first()

    def current_colour_name(self, response):
        selector = ".js-current-color-name::attr(value)"
        current_colour = response.css(selector).extract_first()
        return current_colour

    def current_size(self, response):
        return self.current_size_name(response).split(' ')

    def current_size_name(self, response):
        selector = ".js-current-size-name::attr(value)"
        current_size = response.css(selector).extract_first()
        return current_size

    def create_sku_requests(self, response):
        multiple_requests = []
        for article in self.articles(response):
            form_data = {
                'cl': self.form_data_cl(response),
                'anid': article.get('number'),
                'ajaxdetails': 'ajaxdetailsPage',
            }
            request = scrapy.FormRequest(
                url=self.product_api_url, formdata=form_data, callback=self.parse_product)
            multiple_requests.append(request)
        return multiple_requests

    def next_action(self, response):
        product = response.meta.get("product")
        sub_requests = product.get("remaining_request")
        if not sub_requests:
            return product

        request = sub_requests.pop()
        request.meta["product"] = product
        return request
