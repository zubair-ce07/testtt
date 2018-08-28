import json
import re
from urllib.parse import urlparse, urljoin

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
        'DOWNLOAD_DELAY': 6,
    }

    def parse_product(self, response):

        product_item = Product()

        product_item['retailer_sku'] = self.extract_retailer_sku(response)
        product_item['image_urls'] = self.extract_image_urls(response)
        product_item['description'] = self.extract_description(response)
        product_item['name'] = self.extract_product_name(response)
        product_item['gender'] = self.extract_gender(response)
        product_item['category'] = self.extract_categories(response)
        product_item['url'] = self.extract_product_url(response)
        product_item['brand'] = self.extract_brand(response)
        product_item['care'] = self.extract_product_care(response)
        product_item['skus'] = self.extract_skus(response)
        product_item['requests_queue'] = self.extract_colors_request(response)

        return self.requests_to_follow(product_item)

    def requests_to_follow(self, product_item):
        next_requests = product_item.get("requests_queue")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product_item
            return request

        del product_item["requests_queue"]

        return product_item

    def extract_colors_request(self, response):
        css = '.colorswatches_inner li:not(.selected) a::attr(href)'
        color_urls = [url for url in response.css(css).extract()
                      if re.match('.*\/Product-ShowProductDetails\?.*', url)]
        return [response.follow(url, callback=self.parse_colors) for url in color_urls]

    def parse_colors(self, response):
        product_item = response.meta.get('item')
        product_item['skus'] = product_item.get('skus', []) + self.extract_skus(response)
        return self.requests_to_follow(product_item)

    def extract_product_name(self, response):
        prod_name_css = '.product_name::text'
        return response.css(prod_name_css).extract_first()

    def extract_product_care(self, response):
        care_css = '#product_care .care .careimage>div::attr(title)'
        return response.css(care_css).extract()

    def extract_description(self, response):
        desc_css = '#product_information_features .description ::text'
        prod_desc = [raw_desc.strip() for raw_desc in response.css(desc_css).extract()]
        return list(filter(None, prod_desc))

    def extract_retailer_sku(self, response):
        prod_sku_css = '#product_information_features span.productid::text'
        return response.css(prod_sku_css).extract_first()

    def extract_image_urls(self, response):
        image_urls_css = '#product_images .mainimage::attr(src)'
        return response.css(image_urls_css).extract()

    def extract_gender(self, response):
        if 'men' in ' '.join(self.extract_categories(response)).lower():
            return "Men"
        return "Women"

    def extract_brand(self, response):
        css = '.product_addtocart #form_addtocartbutton::attr(data-gtm-brand)'
        return response.css(css).extract_first()

    def extract_product_url(self, response):
        return response.url

    def extract_categories(self, response):
        xpath = '//script[contains(.,"var dataParam")]'
        raw_product = response.xpath(xpath).re_first('\s*var\s*dataParam\s*=(.+?);')

        if not raw_product:
            return []

        raw_product = json.loads(raw_product)
        return raw_product['googletagmanager']['data']['productCategory']

    def extract_skus(self, response):
        color_css = '.colorswatches_inner li.selected a::attr(title)'
        color = response.css(color_css).extract_first()

        price_css = '.pricing .price-box div:not(.disabled) span[itemprop="price"]::text'
        price = response.css(price_css).extract_first(default='')

        currency_css = '.pricing .price-box span[itemprop="priceCurrency"]::text'
        currency = response.css(currency_css).extract_first()

        prev_price_css = '.pricing .price-box> div.disabled span[itemprop="price"]::text'
        previous_prices = response.css(prev_price_css).extract_first(default='')

        size_css = '#product_variant_details .colorsizes_inner > .overlaysizes li'
        size_selectors = response.css(size_css)

        product_skus = []
        for sel in size_selectors:
            size = sel.css('a::text').extract_first(default='').strip()

            if not any(size in sku.get('size') for sku in product_skus):
                sku = {"colour": color, "price": price.strip(),
                       "currency": currency, "size": size,
                       "sku_id": "{}_{}".format(color, size)}

                if previous_prices:
                    sku["previous_prices"] = [previous_prices.strip()]

                if sel.css('::attr(class)').extract_first() == 'disabletile':
                    sku["out_of_stock"] = True

                product_skus.append(sku)

        return product_skus
