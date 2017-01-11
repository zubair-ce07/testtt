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
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['url'] = response.url
        garment['name'] = self.product_name(response)
        garment['category'] = self.product_category(response)
        garment['brand'] = self.product_brand_name(response)
        garment['description'] = self.product_description(response)
        garment['currency'] = self.product_currency(response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.get_image_urls(response)
        garment['spider_name'] = self.name
        garment['retailer'] = 'thesting'
        garment['price'] = self.product_price(response)
        is_sale = self.is_sale(response)
        if is_sale:
            garment['previous_price'] = self.product_old_price(response)
        garment['url_original'] = response.url
        garment['care'] = self.product_care(response)
        garment['skus'] = {}
        color_info = self.get_color_info(response)
        return self.get_skus(garment, color_info)

    def get_image_urls(self, response):
        script = response.css('div#overlay-mask + script')
        pattern = re.compile('listImages":\s*(\[.*?\])', re.DOTALL)
        str_json = script.re_first(pattern)
        array = json.loads(str_json)
        return [obj['urlPresetZoom'] for obj in array]

    def get_skus(self, item, color_info):
        if color_info:
            name, url = color_info.pop()
            return Request(url='http://www.thesting.com/' + url,
                           callback=self.parse_color_sku,
                           meta={
                               'item': item,
                               'color_name': name,
                               'color_info': color_info,
                           })
        return item

    def parse_color_sku(self, response):
        item = response.meta['item']
        color_info = response.meta['color_info']
        color = response.meta['color_name']
        price = self.product_price(response)
        currency = self.product_currency(response)
        sizes = self.product_sizes(response)
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
        return self.get_skus(item, color_info)

    def get_color_info(self, response):
        script_elem = response.css('div#overlay-mask + script')
        all_colors_raw = script_elem.re_first('"allColors":\s*(\[[^\]]*\])')
        all_colors_json = json.loads(all_colors_raw)
        return [(color['name'], color['productPageColorUrl'])
                for color in all_colors_json]

    def product_price(self, response):
        script = response.css('script:contains("saleStatus")')
        return int(script.re_first('"price":[\s"]*([\d\.]*)').replace('.', ''))

    def product_old_price(self, response):
        script = response.css('script:contains("saleStatus")')
        return int(script.re_first('"fromPrice":[\s"]*([\d\.]*)').replace('.', ''))

    def product_currency(self, response):
        script = response.css('div#overlay-mask + script')
        return script.re_first(r'"currency":[\s"]*([^:ascii:])')

    def product_care(self, response):
        script = response.css('div#overlay-mask + script')
        care_raw = script.re_first(r'"productFabrics":\s*(\[[^\]]*\])')
        care_json = json.loads(care_raw)
        return [care['value'] for care in care_json]

    def product_gender(self, response):
        script = response.css('script:contains("pageAffinity")')
        affinity = script.re_first(r'"pageAffinity": "(.*)"').lower()
        return ('women', 'men')[affinity == 'male']

    def product_sizes(self, response):
        script_elem = response.css('div#overlay-mask + script')
        sizes_raw = script_elem.re_first(r'"availableSizes":\s*(\[[^\]]*\])')
        sizes_json = json.loads(sizes_raw)
        return sizes_json

    def is_sale(self, response):
        return int(response.css('script:contains("saleStatus")')
                   .re_first(r'"saleStatus": (\d+)'))

    def product_description(self, response):
        script = response.css('div#overlay-mask + script')
        return response.css('meta[name="description"]::attr(content)').extract_first()

    def product_brand_name(self, response):
        script = response.css('div#overlay-mask + script')
        return script.re_first(r'"brandName":\s\"(.*)\"')

    def product_category(self, response):
        script = response.css('div#overlay-mask + script')
        return script.re(r'"productCategory":\s*\"(.*)\"')

    def product_name(self, response):
        script = response.css('div#overlay-mask + script')
        return script.re_first(r'"productName":\s*\"(.*)\"')

    def product_retailer_sku(self, response):
        script = response.css('div#overlay-mask + script')
        return script.re_first(r'"genericCode":\s*\"(.*)\"')
