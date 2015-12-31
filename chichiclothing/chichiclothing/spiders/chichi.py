import re
import json
import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from chichiclothing.items import ChichiClothingItem


class ChichiSpider(CrawlSpider):
    name = 'chichi_spider'
    allowed_domains = ['chichiclothing.com']
    start_urls = ('http://www.chichiclothing.com/',)
    next_page_url_template = 'http://www.chichiclothing.com/categories_ajax.php?catid={0}&fromwhichrefine=&' \
                             'price_min=&price_max=&page={1}&sort=etailpreferred&search_query='

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=".//div[@id='Menu']"),
             callback='request_next_product_page'),
        Rule(SgmlLinkExtractor(restrict_xpaths=".//div[@class='xProductDetails']"), callback='parse_product'))

    def request_next_product_page(self, response):
        for request in self.parse(response):
            yield request

        if not response.xpath(".//li[@class='ActivePage']/following-sibling::a"):
            return

        page = int(self.get_line_from_node(response.xpath("(.//li[@class='ActivePage'])[1]"))) + 1
        category_id = response.meta.get('category_id')

        if not category_id:
            category_id = self.get_attribute_value_from_node(
                response.xpath("(.//*[contains(@href,'categoryid')]/@href)[1]"))
            params = urlparse.parse_qs(urlparse.urlparse(category_id).query)
            category_id = params['categoryid'][0]

        next_page_url = self.next_page_url_template.format(category_id, page)
        yield Request(next_page_url, self.request_next_product_page, meta={"category_id": category_id})

    def parse_product(self, response):
        product = ChichiClothingItem()
        product['url_original'] = response.url
        product['brand'] = 'Chi Chi'
        product['gender'] = 'women'
        product['name'] = self.product_name(response)
        product['category'] = self.product_categories(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['price'] = self.get_price_digits(self.product_price(response))
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = self.product_images_urls(response)
        product['skus'] = {}
        variations_details = self.get_variations_details(response, product)
        return self.get_next_variation(product, variations_details)

    def get_next_variation(self, product, product_variations_details):
        if product_variations_details:
            size_details, url = product_variations_details.pop()
            return Request(url, callback=self.parse_product_variation,
                           meta={'product': product,'product_variations_details': product_variations_details,
                                 'size_details': size_details})
        return product

    def parse_product_variation(self, response):
        product = response.meta['product']
        product_variations_details = response.meta['product_variations_details']
        product['skus'].update(self.product_size_details(response))
        return self.get_next_variation(product, product_variations_details)

    def get_variations_details(self, response, product):
        variations_details = []
        previous_prices = self.product_previous_prices(response)
        color = self.product_color(response)

        size_detail_template = {}

        if previous_prices:
            size_detail_template['previous_prices'] = previous_prices

        if color:
            size_detail_template['color'] = color

        variations = response.xpath(".//div[@class='Value']//li[contains(@class,'sizeli')] | "
                                    "(.//div[@class='miniprod'])[1]//li[contains(@class,'sizeli')]")
        variation_url_template = 'http://www.chichiclothing.com/remote.php?w=GetVariationOptions&productId={0}&options={1}'

        for variation in variations:
            size_details = {}
            size_details.update(size_detail_template)
            size_details['size'] = self.get_line_from_node(variation)
            variation_url = variation_url_template.format(product['retailer_sku'], self.get_attribute_value_from_node(variation.xpath('@rel')))
            variations_details.append((size_details, variation_url))

        if not variations_details:
            key = '{0}_One Size'.format(color)
            size_detail = size_detail_template
            size_detail['size'] = "One Size"

            if previous_prices and previous_prices[0] == product['price']:
                del size_detail['previous_prices']

            size_detail['price'] = product['price']
            size_detail['currency'] = self.get_currency_code(self.product_price(response))
            product['skus'][key] = size_detail

        return variations_details

    def product_size_details(self, response):
        size_details = response.meta['size_details']
        json_response = json.loads(response.body)
        size_details['out_of_stock'] = not json_response['instock']
        size_details['price'] = self.get_price_digits(json_response['unformattedPrice'])

        if 'strike' in json_response['price']:
            size_details['currency'] = self.get_currency_code(json_response['saveAmount'])
        else:
            size_details['currency'] = self.get_currency_code(json_response['price'])

        if size_details.get('previous_prices') and size_details['price'] == size_details['previous_prices'][0]:
            del size_details['previous_prices']

        color = size_details.get('color','')
        key = '{0}_{1}'.format(color, size_details['size'])
        return {key: size_details}

    def product_categories(self, node):
        return self.get_text_from_node(node.xpath(".//*[@id='ProductBreadcrumb']/ul/li/*[text() !=  'Home']"))

    def product_name(self, node):
        return self.get_attribute_value_from_node(node.xpath(".//*[@name='prodname']/@value"))

    def product_description(self, node):
        return self.get_text_from_node(node.xpath(
            ".//*[contains(@class,'acpdcontent')] | .//div[@class='miniprod'][1]/textarea"))

    def product_care(self, node):
        return self.normaliz_string_list(self.get_text_from_node(node.xpath(
            ".//h2[contains(@class,'accordion-header') and contains(text(),'CARE')]/following-sibling::div")))

    def product_retailer_sku(self, node):
        return self.get_attribute_value_from_node(node.xpath("(.//input[@name='product_id'])[1]/@value"))

    def product_images_urls(self, node):
        return node.xpath(".//*[@class='prodpicsidethumb']//img/@zoom").extract()

    def product_color(self, node):
        return self.get_line_from_node(node.xpath(".//div[@id='buyablediv']/following-sibling::div//span"))

    def product_price(self, node):
        if node.xpath(".//div[contains(@class,'has-sale-price')]"):
            return self.get_line_from_node(node.xpath(".//span[@class='saleprice']"), deep=False).split(':')[-1]

        return self.get_line_from_node(node.xpath(
            ".//div[@id='productprice']/span | (.//*[@class='miniprod'])[1]/div[1]"), deep=False)

    def product_previous_prices(self, node):
        previous_price = self.get_line_from_node(node.xpath(
            ".//span[@class='rrp'] | (.//*[@class='miniprod'])[1]/div[1]/*"), deep=False)
        return [self.get_price_digits(previous_price)] if previous_price else []

    def get_currency_code(self, price):
        symbol = re.sub('[\\d,.\\s]', '', price)
        if symbol == '$':
            return 'USD'
        else:
            return 'GBP'

    def get_price_digits(self, price):
        return int(re.sub('\\D', '', price))

    def normaliz_string_list(self, s_list):
        return [s.strip(' -') for s in s_list if s.strip(' -')]

    def get_text_from_node(self, node, deep=True):
        if not node:
            return []
        _text = './/text()'
        if not deep:
            _text = './text()'
        str_list = [x.strip() for x in node.xpath(_text).extract() if len(x.strip()) > 0 ]
        return str_list

    def get_line_from_node(self, node, deep = True, sep=' '):
        lines = self.get_text_from_node(node, deep)
        if not lines:
            return ''
        return sep.join(lines).strip()

    def get_attribute_value_from_node(self, node):
        value = node.extract()
        if value:
            return value[0].strip()
        return ''
