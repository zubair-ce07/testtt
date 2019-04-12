from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from smartwool_crawler.items import SmartwoolCrawlerItem, ProductLoader
import scrapy
import json
import re


class SmartWoolSpider(CrawlSpider):
    name = 'smart_wool_spider'
    start_urls = ['https://www.smartwool.com/homepage.html']
    category_css = '.topnav-accordion-l3-dropdown'
    product_css = '.product-block-name-link'

    gender = ("womens", "mens", "kids")
    allow_links = ('/shop')
    page_size = ['24', '48', '72', '96']
    store_id = ''
    category_id = ''
    product_id = ''

    rules = (
        Rule(LinkExtractor(allow=allow_links, restrict_css=category_css), callback='parse_product_page'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        product = self.parse_info(response)
        product['size_key'] = response.css('.attr-size::attr(data-attribute-id)').get()
        product['color_key'] = response.css('.attr-color-js::attr(data-attribute-id)').get()
        product['prices_detail'] = self.product_price_detail(response)
        product['size'] = self.product_size(response)

        request_url = (f"https://www.smartwool.com/webapp/wcs/stores/servlet/VFAjaxProductAvailabilityView?"
                       f"storeId={self.store_id}& &productId={self.product_id}")

        return scrapy.Request(request_url, meta={"product": product}, callback=self.parse_skus)

    def parse_info(self, response):
        product = ProductLoader(item=SmartwoolCrawlerItem(), response=response)
        self.product_id = response.css('#product-imgs::attr(data-product-id)').get()
        product.add_value('pid', self.product_id)
        product.add_value('gender', self.product_gender(response))
        product.add_value('category', self.product_category(response))
        product.add_value('brand', 'Smart Wool')
        product.add_value('url', response.url)
        product.add_css('name', '.product-content-info-name.product-info-js::text')
        product.add_css('description', '.desc-container.pdp-details-desc-container::text')
        product.add_css('care', '.pdp-care-list-item::text')
        product.add_value('image_urls', self.product_image_urls(response))
        return product.load_item()

    def parse_product_page(self, response):
        self.store_id = response.css('meta[name="storeId"]::attr(content)').get()
        self.category_id = response.css('meta[name="categoryId"]::attr(content)').get()

        for size in self.page_size:
            requested_url = f"{response.url}/VFAjaxGetFilteredSearchResultsView?categoryId={self.category_id}&beginIndex={size}"
            yield scrapy.Request(url=requested_url, callback=self.parse_product_request)

    def parse_product_request(self, response):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),])+', response.text)
        if urls:
            for url in urls[:-1]:
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'] = self.skus(response)

        del product['prices_detail'], product['color_key'], product['size'], product['size_key']
        return product

    def skus(self, response):
        product = response.meta['product']
        product_detail = []

        raw_product = json.loads(response.text)
        stock_detail = self.stock_detail(raw_product, product['size_key'])

        for color in raw_product['attributes'][product['color_key']]:
            for sku_id in color['catentryId']:
                stock, size = stock_detail[str(sku_id)]

                skus = product['prices_detail']
                skus['color'] = color['display']
                skus['size'] = size
                skus['sku_id'] = color['display'] + "_" + size
                if not stock:
                    skus['out_of stock'] = True

                product_detail.append(skus.copy())
        return product_detail

    def stock_detail(self, raw_product, size_key):
        stock_detail = {}

        for sku_id, stock in raw_product['stock'].items():
            size = [size['display'] for size in raw_product['attributes'][size_key] if sku_id in str(size['catentryId'])]
            stock_detail[sku_id] = (stock, '/'.join(size))

        return stock_detail

    def product_category(self, response):
        category_list = response.css('.page-breadcrumb-list a::text,.page-breadcrumb-list span::text').getall()
        return [categorry.strip() for categorry in category_list]

    def product_gender(self, response):
        category_list = self.product_category(response)
        category = " ".join(category_list)
        return [gender for gender in self.gender if gender in category.lower()]

    def product_size(self, response):
        size_options = response.css('.product-content-form-size-btn-label.attr-box::text').getall()
        return [size.strip() for size in size_options]

    def product_price_detail(self, response):
        product_price = {
            'price': response.css('meta[property="og:price:amount"]::attr(content)').get(),
            'currency': response.css('meta[property="og:price:currency"]::attr(content)').get(),
        }

        previous_price = response.css('.original-price-js ::text').get()
        if previous_price:
            product_price['previous_price'] = previous_price

        return product_price

    def product_image_urls(self, response):
        image_urls = response.css('.color-swatches-js img::attr(src)').getall()
        return ["https:" + image for image in image_urls]

