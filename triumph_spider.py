import json
import re
from urllib.parse import urlparse
from urllib.parse import urljoin

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from triumph.items import ProductItem


class ProductsSpider(CrawlSpider):
    name = 'triumph'

    start_urls = ['http://uk.triumph.com/']

    deny_urls = ['my-account', 'on/demandware.store\w*', 'sale', 'collections', 'new',
                 '\w*findtheone\w*', '\w*format=ajax']

    def process_product_url(url):
        parsed_url = urlparse(url)
        return urljoin(ProductsSpider.start_urls[0], parsed_url.path)

    listing_css = ['.mainLink', '.pagination-wrapper .paginationlink:not(.disabled)']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_urls), callback='parse'),
        Rule(LinkExtractor(restrict_css='.listItem>.product>.productname>.name>.productClick'
                           , process_value=process_product_url), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):
        print(response.url)

        product_item = ProductItem()
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

        if self.get_color_urls(response):
            return self.extract_colors(self.get_color_urls(response), product_item)

        return product_item

    def get_color_urls(self, response):
        css = '.colorswatches_inner li:not(.selected) a::attr(href)'
        return [url for url in response.css(css).extract()
                if re.match('.*\/Product-ShowProductDetails\?.*', url)]

    def get_product_name(self, response):
        return response.css('.product_name::text').extract_first()

    def get_product_care(self, response):
        return response.css('#product_care .care .careimage>div::attr(title)').extract()

    def get_description(self, response):
        css = '#product_information_features .description ::text'
        return list(filter(None, list(map(str.strip, response.css(css).extract()))))

    def get_retailer_sku(self, response):
        return response.css('#product_information_features span.productid::text').extract_first()

    def get_image_urls(self, response):
        return response.css('#product_images .mainimage::attr(src)').extract()

    def get_gender(self, response):
        if any("Men" in s for s in self.get_categories(response)):
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
        product_skus = []

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
        product_sizes = response.css(size_css + ' a::text').extract()
        product_sizes = set(zip((True if 'disabletile' == sel.css('::attr(class)').extract_first()
                                 else False for sel in size_selectors), product_sizes))

        for out_of_stock, size in product_sizes:
            sku = {"colour": color, "price": price.extract_first().strip(),
                   "currency": currency.extract_first(), "size": size.strip()}

            if previous_prices:
                sku["previous_prices"] = [previous_prices.extract_first().strip()]

            if out_of_stock:
                sku["out_of_stock"] = True

            sku["sku_id"] = "{}_{}".format(color, size.strip())

            product_skus.append(sku)

        return product_skus

    def extract_colors(self, color_urls, product_item):
        if color_urls:
            url = urljoin('http://uk.triumph.com/', color_urls.pop())
            return Request(url, callback=self.parse_colors, meta={'item': product_item,
                                                                  'color_urls': color_urls})

        return product_item

    def parse_colors(self, response):
        product_item = response.meta.get('item')
        color_urls = response.meta.get('color_urls')
        product_item['skus'] = product_item.get('skus', []) + self.get_skus(response)
        return self.extract_colors(color_urls, product_item)
