import json
import re
from urllib.parse import urlparse
from urllib.parse import urljoin

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from triumph.items import Product


class TriumphSpider(CrawlSpider):
    name = 'triumph'
    listing_css = ['.mainLink', '.pagination-wrapper .paginationlink:not(.disabled)']
    product_css = '.productimage .productClick'

    start_urls = ['http://uk.triumph.com/']
    allowed_domains = ['uk.triumph.com']

    deny_urls = ['my-account', 'on/demandware.store\w*', 'sale', 'collections', 'new',
                 '\w*findtheone\w*', '\w*format=ajax']

    def process_product_url(url):
        parsed_url = urlparse(url)
        return urljoin(TriumphSpider.start_urls[0], parsed_url.path)

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_urls), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css, process_value=process_product_url),
             callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):

        product_item = Product()

        product_item['retailer_sku'] = self.get_retailer_sku(response)
        product_item['image_urls'] = self.get_image_urls(response)
        product_item['description'] = self.get_description(response)
        product_item['name'] = self.get_product_name(response)
        product_item['gender'] = self.get_gender(response)
        product_item['category'] = self.get_categories(response)
        product_item['url'] = self.get_product_url(response)
        product_item['brand'] = self.get_brand(response)
        product_item['care'] = self.get_product_care(response)
        product_item['skus'] = self.get_skus(response)
        product_item['colors_request'] = self.get_colors_request(response)

        return self.requests_to_follow(product_item)

    def requests_to_follow(self, product_item):
        next_requests = product_item.get("colors_request")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product_item
            return request

        del product_item["colors_request"]

        return product_item

    def get_colors_request(self, response):
        css = '.colorswatches_inner li:not(.selected) a::attr(href)'
        color_urls = [url for url in response.css(css).extract()
                      if re.match('.*\/Product-ShowProductDetails\?.*', url)]
        return [response.follow(url, callback=self.parse_colors) for url in color_urls]

    def parse_colors(self, response):
        product_item = response.meta.get('item')
        product_item['skus'] = product_item.get('skus', []) + self.get_skus(response)
        return self.requests_to_follow(product_item)

    def get_product_name(self, response):
        prod_name_css = '.product_name::text'
        return response.css(prod_name_css).extract_first()

    def get_product_care(self, response):
        care_css = '#product_care .care .careimage>div::attr(title)'
        return response.css(care_css).extract()

    def get_description(self, response):
        desc_css = '#product_information_features .description ::text'
        return list(filter(None, list(map(str.strip, response.css(desc_css).extract()))))

    def get_retailer_sku(self, response):
        prod_sku_css = '#product_information_features span.productid::text'
        return response.css(prod_sku_css).extract_first()

    def get_image_urls(self, response):
        image_urls_css = '#product_images .mainimage::attr(src)'
        return response.css(image_urls_css).extract()

    def get_gender(self, response):
        if 'men' in ' '.join(self.get_categories(response)).lower():
            return "Men"
        return "Women"

    def get_brand(self, response):
        css = '.product_addtocart #form_addtocartbutton::attr(data-gtm-brand)'
        return response.css(css).extract_first()

    def get_product_url(self, response):
        return response.url

    def get_categories(self, response):
        xpath = '//script[contains(.,"var dataParam")]'
        product_details = response.xpath(xpath).re_first('\s*var\s*dataParam\s*=(.+?);')

        if not product_details:
            return []

        product_details = json.loads(product_details)
        return product_details['googletagmanager']['data']['productCategory']

    def get_skus(self, response):
        color_css = '.colorswatches_inner li.selected a::attr(title)'
        color = response.css(color_css).extract_first()

        price_css = '.pricing .price-box div:not(.disabled) span[itemprop="price"]::text'
        price = response.css(price_css)

        currency_css = '.pricing .price-box span[itemprop="priceCurrency"]::text'
        currency = response.css(currency_css)

        prev_price_css = '.pricing .price-box> div.disabled span[itemprop="price"]::text'
        previous_prices = response.css(prev_price_css)

        size_css = '#product_variant_details .colorsizes_inner > .overlaysizes li'
        size_selectors = response.css(size_css)

        product_skus = []
        for sel in size_selectors:
            size = sel.css('a::text').extract_first().strip()

            if not any(size in sku.get('size') for sku in product_skus):
                sku = {"colour": color, "price": price.extract_first().strip(),
                       "currency": currency.extract_first(), "size": size,
                       "sku_id": "{}_{}".format(color, size.strip())}

                if previous_prices:
                    sku["previous_prices"] = [previous_prices.extract_first().strip()]

                if sel.css('::attr(class)').extract_first() == 'disabletile':
                    sku["out_of_stock"] = True

                product_skus.append(sku)

        return product_skus
