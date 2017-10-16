import re
import json
from w3lib.url import url_query_parameter, add_or_replace_parameter
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FarFetchSpider(CrawlSpider):

    name = "farfetch"
    start_urls = ["https://www.farfetch.com/uk/"]
    product_api_url = "https://www.farfetch.com/uk/product/GetDetailState?productId={0}&storeId={1}&categoryId={2}&designerId={3}"
    main_menu_css = ['#header-tabs-container a']
    section_menu_css = ['#tab_248 li.js-asyncMenuChild a']
    product_css = '.ab-available-sizes-product-card a.listing-item-content'
    rules = (
        Rule(LinkExtractor(restrict_css=main_menu_css),),
        Rule(LinkExtractor(restrict_css=section_menu_css), callback='parse_products'),
    )

    def parse_products(self, response):

        product_urls = response.css(self.product_css+"::attr(href)").extract()
        for product_url in product_urls:
            yield Request(response.urljoin(product_url), callback=self.parse_product)

        next_page_disabled = self.product_next_page(response)
        if product_urls and not next_page_disabled:
            page_no = url_query_parameter(response.url, 'page', 1)
            new_value = int(page_no)+1
            ajax_url = add_or_replace_parameter(response.url, 'page', str(new_value))
            yield Request(url=ajax_url, callback=self.parse_products)

    def parse_product(self, response):
        garment = self.product_info(response)
        garment['skus'] = {}
        garment['requests'] = []
        garment['imageUrl'] = self.product_images(response)
        garment['care'] = self.product_care(response)
        garment['requests'].append(self.product_meta(garment))
        return self.request_or_garment(garment)

    def product_info(self, response):
        product_json = response.css('script::text').extract()[3]
        product_json = re.findall('window.universal_variable.product = ({.*?})', product_json)
        product_json = json.loads(product_json[0])
        filtered_product_info = {parameter: value for (parameter, value) in product_json.items() if "_" not in parameter}
        filtered_product_info['url'] = response.urljoin(filtered_product_info['url'])
        return filtered_product_info

    def product_meta(self, garment):
        api_url = self.product_api_url.format(garment['id'], garment['storeId'], garment['categoryId'], garment['manufacturerId'])
        return Request(url=api_url, callback=self.parse_product_meta, meta={'garment': garment})

    def parse_product_meta(self, response):
        json_response = json.loads(response.body.decode())
        trail = [response.meta['garment']['url'] if trail_url =="#" else response.urljoin(trail_url) for trail_url in re.findall('href=\"(.*?)\"', json_response['ProductBreadCrumb'])]
        response.meta['garment']['trail'] = trail
        response.meta['garment']['skus'] = self.product_sku(json_response)
        return self.request_or_garment(response.meta['garment'])

    def product_sku(self, garment_meta):
        sku = {}
        for size in garment_meta['SizesInformationViewModel']['AvailableSizes']:
            sku_id = size['SizeId']
            sku[sku_id] = {
                'size': size['Description'],
                'price': size['PriceInfo']['Price']
            }
        return sku

    def product_care(self, response):
        return response.css('[data-tstid="Content_Composition&Care"] dd::text').extract()

    def product_images(self, response):
        return [response.urljoin(image_url) for image_url in response.css('.bx-pager-thumb img::attr(src)').extract()]

    def product_sizes(self, response):
        return response.css("#detailSizeDropdown").extract()

    def product_next_page(self, response):
        return response.css('.js-lp-pagination-next.pagination-disabled').extract_first()

    def request_or_garment(self, garment):
        if garment['requests']:
            return garment['requests'].pop()
        return garment
