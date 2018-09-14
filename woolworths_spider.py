"""
This module extracts products data from woolworths website
"""
import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class WoolworthsSpider(CrawlSpider):
    raw_data = {}
    name = 'woolworths'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['https://www.woolworths.co.za/']
    navigation = ['.main-nav__link.main-nav__link--primary.link--parent-has-descendant']
    allows = ('/Women', '/Men', '/Kids', '/Baby')
    rules = (
        Rule(LinkExtractor(restrict_css=navigation, allow=allows)),
        Rule(LinkExtractor(restrict_css=['.landing__link'])),
        Rule(LinkExtractor(restrict_css=['.product-card__visual']), callback='parse_product'),
    )
    def parse_product(self, response):
        product = {}
        self.raw_data = self.retrieve_data(response)
        product['name'] = response.css('.font-graphic.heading--400::text').extract_first()
        product['description'] = response.css('.accordion__content--chrome p::text').extract_first()
        product['currency'] = self.raw_data['currency']
        product['composition'] = response.css(
            '.accordion__content--chrome li::text').extract_first().strip()
        product['bread-crumb'] = response.css('.breadcrumb__crumb a::attr(title)').extract()
        product['product_url'] = response.url
        product['brand'] = self.raw_data['pdp']['productInfo']['brandLogo']
        product['image_url'] = self.capture_image_urls()
        product['skus'] = self.skus_formation()
        return product


    def retrieve_data(self, response):
        """
        This method extracts data in raw json format from script tag. Data is then to be
        purified by regex and hence load it into pure json format
        :param response:
        :return:
        """
        script = response.css('script::text').extract()[4]
        raw_json_list = re.findall(r"(\"pdp\":{\"productInfo\":.*})", script)
        currency = re.findall(r"currency-label\":\"(.)", script)[0]
        raw_json = '{' + raw_json_list[0]
        pure_json = json.loads(raw_json)
        pure_json['currency'] = currency
        return pure_json


    def skus_formation(self):
        dict_list = []
        sku = {}
        sku_ids = []
        active_sku_ids = self.raw_data['pdp']['productInfo']['activeSkuIds']
        product_id = self.raw_data['pdp']['productInfo']['productId']
        price_dict = self.raw_data['pdp']['productPrices'][product_id]['plist3620006']['skuPrices']
        for item in self.raw_data['pdp']['productInfo']['colourSKUs']:
            sku_ids.append(item['styleId'])
        color_size_dict = self.raw_data['pdp']['productInfo']['styleIdSizeSKUsMap']
        for _id in sku_ids:
            color_size_list = color_size_dict[_id]
            for entity, active_sku_id, in zip(color_size_list, active_sku_ids):
                temp_dict = {
                    'color': entity['colour'],
                    'size': entity['size'],
                    'price': price_dict[active_sku_id]['SalePrice']
                }
                dict_list.append(temp_dict)
            sku[_id] = dict_list
            dict_list = []
        return sku


    def capture_image_urls(self):
        url_list = []
        for item in self.raw_data['pdp']['productInfo']['colourSKUs']:
            url_list.append(item['internalSwatchImage'])
        return url_list

