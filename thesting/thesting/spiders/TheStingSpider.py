import json
from scrapy.http.request import Request
from scrapy.link import Link
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from thesting.items import TheStingItem


class ProductLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        script = response.css('div.listings > script')
        product_urls = script.re('\"urlProductDetailPage\":\s*\"(.*)\"')
        product_links = [Link(url='http://www.thesting.com/' + link) for link in product_urls]
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
        Rule(LinkExtractor(restrict_css=('.topnav-container'), ), callback='parse_list'),
    ]

    def parse_list(self, response):
        for link in ProductLinkExtractor().extract_links(response):
            yield Request(url=link.url, callback=self.parse_item)

        pagination_links = PaginationLinksExractor().extract_links(response)
        if pagination_links:
            for link in pagination_links:
                yield Request(url=link.url, callback=self.parse_list)

    def parse_item(self, response):
        script = response.css('div#overlay-mask + script')
        garment = TheStingItem()
        garment['retailer_sku'] = script.re_first('(?<="genericCode":)\s*\"(.*)\"')
        garment['url'] = response.url
        garment['name'] = script.re_first('(?<="productName":)\s*\"(.*)\"')
        garment['category'] = script.re('(?<="productCategory":)\s*\"(.*)\"')
        garment['brand'] = script.re_first('(?<="brandName":)\s\"(.*)\"')
        garment['description'] = response.css('meta[name="description"]::attr(content)').extract_first()
        garment['currency'] = self.product_currency(script)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.get_image_urls(response)
        garment['spider_name'] = self.name
        garment['retailer'] = 'thesting'
        garment['price'] = self.product_price(response)
        is_sale = int(response.css('script:contains("saleStatus")')
                      .re_first('(?<=\"saleStatus\":) (\d+)'))
        if is_sale:
            garment['previous_price'] = self.product_old_price(response)
        garment['url_original'] = response.url
        garment['care'] = self.product_care(response)
        color_info = self.get_color_info(response)
        garment['skus'] = {}
        return self.get_skus(garment, color_info)

    def get_image_urls(self, response):
        script = response.css('div#overlay-mask + script')
        str_json = script.re_first('(?<="listImages":)[\s"]*(\[[^\]]*\])')
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
        script = response.css('div#overlay-mask + script')
        color = response.meta['color_name']
        price = self.product_price(response)
        currency = self.product_currency(script)
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
        script_elem = response.css('div#overlay-mask + script::text')
        all_colors_raw = script_elem.re_first('(?<="allColors":)\s*(\[[^\]]*\])')
        all_colors_json = json.loads(all_colors_raw)
        return [(color['name'], color['productPageColorUrl'])
                for color in all_colors_json]

    def product_price(self, response):

        script = response.css('script:contains("saleStatus")::text')
        return int(script.re_first('(?<="price":)[\s"]*([\d\.]*)').replace('.', ''))

    def product_old_price(self, response):
        script = response.css('script:contains("saleStatus")::text')
        return int(script.re_first('(?<="fromPrice":)[\s"]*([\d\.]*)').replace('.', ''))

    def product_currency(self, script):
        return script.re_first('(?<="currency":)[\s"]*([^:ascii:])')

    def product_care(self, response):
        script= response.css('div#overlay-mask + script::text')
        care_raw = script.re_first('(?<="productFabrics":)\s*(\[[^\]]*\])')
        care_json = json.loads(care_raw)
        return [care['value'] for care in care_json]

    def product_gender(self, response):
        script = response.css('script:contains("pageAffinity")')
        affinity = script.re_first('(?<="pageAffinity":) "(.*)"')
        if affinity.lower() == 'male':
            return 'men'
        elif affinity.lower() == 'female':
            return 'women'

    def product_sizes(self, response):
        script_elem = response.css('div#overlay-mask + script::text')
        sizes_raw = script_elem.re_first('(?<="availableSizes":)\s*(\[[^\]]*\])')
        sizes_json = json.loads(sizes_raw)
        return sizes_json
