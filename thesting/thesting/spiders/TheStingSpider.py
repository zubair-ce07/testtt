import json
import re
from scrapy.http.request import Request
from scrapy.link import Link
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from thesting.items import TheStingItem


class ProductLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        script = response.css('div.listings > script')
        product_urls = script.re('\"urlProductDetailPage\":\s*\"(.*)\"')
        product_links = [Link(url=response.urljoin(link)) for link in product_urls]
        return product_links


class PaginationLinksExractor(LinkExtractor):
    def extract_links(self, response):
        total_pages = response.css('input#totalOfPages::attr(value)').extract_first()
        if total_pages:
            total_pages = int(total_pages)
            current_page = int(response.css('input#currentPage::attr(value)').extract_first())
            base_url = response.css('input#baseRequestURI::attr(value)').extract_first()
            pagination_links = [Link(url='http://www.thesting.com/en{0}?page={1}'.format(base_url, page))
                                for page in range(1, total_pages + 1) if page is not current_page]
            return pagination_links


class TheStingSpider(CrawlSpider):
    name = "thesting"
    start_urls = [
        'http://www.thesting.com/en-gb/'
    ]

    allowed_domains = [
        'www.thesting.com'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css='.topnav-container'), callback='parse_list'),
    ]

    def parse_list(self, response):
        for link in ProductLinkExtractor().extract_links(response):
            yield Request(url=link.url, callback=self.parse_item)

        pagination_links = PaginationLinksExractor().extract_links(response)
        if pagination_links:
            for link in pagination_links:
                yield Request(url=link.url, callback=self.parse_list)

    def parse_item(self, response):
        garment = TheStingItem()
        product_data = self.parse_product_data(response)
        garment['retailer_sku'] = self.product_retailer_sku(product_data)
        garment['url'] = response.url
        garment['name'] = self.product_name(product_data)
        garment['category'] = self.product_category(product_data)
        garment['brand'] = self.product_brand_name(product_data)
        garment['description'] = self.product_description(product_data)
        garment['currency'] = self.product_currency(product_data)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(product_data)
        garment['spider_name'] = self.name
        garment['retailer'] = 'thesting'
        garment['price'] = self.product_price(product_data)
        is_sale = self.is_sale(product_data)
        if is_sale:
            garment['previous_price'] = self.product_old_price(product_data)
        garment['url_original'] = response.url
        garment['care'] = self.product_care(product_data)
        garment['skus'] = {}
        all_colors = self.get_all_colors(product_data)
        return self.get_skus(garment, all_colors)

    def image_urls(self, product_data):
        return [image.get('urlPresetZoom')
                for image in product_data.get('listImages')]

    def get_skus(self, item, colors):
        if colors:
            name, url = colors.pop()
            return Request(url='http://www.thesting.com/' + url,
                           callback=self.parse_color_sku,
                           meta={
                               'item': item,
                               'color_name': name,
                               'colors': colors,
                           })
        return item

    def parse_color_sku(self, response):
        product_data = self.parse_product_data(response)
        item = response.meta['item']
        colors = response.meta['colors']
        color = response.meta['color_name']
        price = self.product_price(product_data)
        currency = self.product_currency(product_data)
        sizes = self.product_sizes(product_data)
        for size in sizes:
            variant_code = size['variantCode']
            item['skus'][variant_code] = {
                'colour': color,
                'size': size['name'],
                'price': price,
                'currency': currency
            }
            if not size['available']:
                item['skus'][variant_code].update({'out_of_stock': True})
        return self.get_skus(item, colors)

    def get_all_colors(self, product_data):
        all_colors = product_data['allColors']
        return [(color['name'], color['productPageColorUrl'])
                for color in all_colors]

    def product_price(self, product_data):
        price = product_data.get('productPriceData') \
            .get('productPrice') \
            .get('price')
        return str(price).replace('.', '')

    def product_old_price(self, product_data):
        price = product_data.get('productPriceData') \
            .get('fromPrice') \
            .get('price')
        return str(price).replace('.', '')

    def product_currency(self, product_data):
        return product_data.get('productPriceData')\
            .get('productPrice')\
            .get('currency')

    def product_care(self, product_data):
        fabrics = product_data['productFabrics']
        return [fabric['value'] for fabric in fabrics]

    def product_gender(self, response):
        script = response.css('script:contains("pageAffinity")')
        affinity = script.re_first(r'"pageAffinity": "(.*)"').lower()
        return ('women', 'men')[affinity == 'male']

    def product_sizes(self, product_data):
        return product_data.get('availableSizes')

    def is_sale(self, product_data):
        return product_data.get('productPriceData').get('fromPrice')

    def product_description(self, product_data):
        return product_data.get('productDescription')

    def product_brand_name(self, product_data):
        return product_data.get('brandName')

    def product_category(self, product_data):
        return product_data.get('productCategory')

    def product_name(self, product_data):
        return product_data.get('productName')

    def product_retailer_sku(self, product_data):
        return product_data.get('genericCode')

    def parse_product_data(self, response):
        script = response.css('div#overlay-mask + script')
        pattern = re.compile('productDataJson = (\{.*);\s*\<\/', re.DOTALL)
        raw_json = script.re_first(pattern)
        raw_json = raw_json.replace('\'', '"')  # Replace single quote with double quotes
                                                # otherwise json parsing breaks
        product_data = json.loads(raw_json)
        return product_data.get('productData')
