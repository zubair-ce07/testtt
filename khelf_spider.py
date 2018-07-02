import json
import re

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
from scrapy.http import FormRequest
from scrapy.link import Link

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'khelf'
    allowed_domains = ['khelf.com.br']


class MixinBR(Mixin):
    retailer = Mixin.retailer + '-br'
    market = 'BR'
    start_urls = ['http://www.khelf.com.br/']


class PaginationLE():
    pagination_url = 'http://www.khelf.com.br/categoria/1/{}/0//MaisRecente/Decrescente/{}/{}//0/0/.aspx'


    def extract_links(self, response):
        products_per_page = clean(response.css('option::attr(value)'))

        if not products_per_page or not response.css('.pagination'):
            return [Link(response.url)]

        css = '.set-next a::attr(href)'
        max_pages = clean(response.css(css))[0]
        max_pages = max_pages.replace('javascript:MudaPagina', '')
        max_pages = int(max_pages[1:-1])
        category_code = clean(response.css('#CategoriaCodigo::attr(value)'))[0]

        return [Link(self.pagination_url.format(category_code, products_per_page[0], pn)) for pn in range(max_pages)]


class KhelfParseSpider(BaseParseSpider):
    price_css = '#lblPrecos>span>strong::text'
    product_api_url = 'http://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,Khelf.ashx'
    ignore_extension = '.gif'


    def parse(self, response):
        raw_product = self.raw_product(response)
        sku_id = self.sku_id(raw_product)
        product_web_id = self.product_web_id(raw_product)

        if not sku_id:
            return

        garment = self.new_unique_garment(sku_id)

        if not garment:
            return
        
        self.boilerplate_normal(garment, response)
        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(raw_product)

        if self.validate_price(response):
            garment['meta'] = {'requests_queue': self.request_colour(response, garment, product_web_id)}
        else:
            garment['out_of_stock'] = True

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        raw_colours = json.loads(response.text)
        garment = response.meta.get('garment')
        product_web_id = response.meta.get('product_web_id')
        common_sku = response.meta.get('common_sku')
        colours = self.colour_url(str(raw_colours['value'][0]))
        sizes = self.request_sizes(colours, response)

        if not sizes:
            common_sku['size'] = self.one_size
            garment['skus'][product_web_id] = common_sku
        else:
            garment['meta']['requests_queue'] += sizes

        # if not garment['meta']['requests_queue']:
        #     common_sku['size'] = self.one_size
        #     garment['skus'][product_web_id] = common_sku
        
        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta.get('garment')
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        garment = response.meta['garment']
        colour = response.meta['colour']
        raw_product = json.loads(response.text)
        common_sku = response.meta.get('common_sku')
        garment['image_urls'].extend(self.image_urls_in_request(raw_product))
        sizes = self.sizes(raw_product)

        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = clean(size.css('a::text')[0])
            sku['colour'] = colour

            if size.css('.warn'):
                sku['out_of_stock'] = True

            skus[colour.lower() + '-' + sku['size'].lower() if colour else sku['size']] = sku
        
        return skus

    def request_colour(self, response, garment, product_web_id):
        common_sku = {}

        if self.validate_price(response):
            common_sku = self.product_pricing_common(response)

        if product_web_id:
            parameters = {"ProdutoCodigo": product_web_id, "ColorCode": "0"}
            return [Request(self.product_api_url, callback=self.parse_colour, method='POST',
                                                  body=json.dumps(parameters), 
                                                  headers={'X-AjaxPro-Method': 'CarregaSKU', 'Referer': response.url},
                                                  meta={'product_web_id': product_web_id,
                                                        'common_sku': common_sku})]
    
    def request_sizes(self, colours, response):
        requests = []
        request_headers = {'X-AjaxPro-Method': 'DisponibilidadeSKU','Referer': response.url}
        parameters = {"CarValorCodigo1": "0", "CarValorCodigo2": "0",
                      "CarValorCodigo3": "0", "CarValorCodigo4": "0",
                      "CarValorCodigo5": "0", "ProdutoCodigo": response.meta.get('product_web_id')}

        for colour in colours:
            parameters['CarValorCodigo1'] = colour
            requests.append(Request(self.product_api_url, callback=self.parse_skus, method='POST',
                                                          body=json.dumps(parameters),
                                                          headers=request_headers, 
                                                          meta={'colour': colour, 
                                                                'common_sku': response.meta.get('common_sku')}))

        return requests

    def validate_price(self, response):
        return response.css(self.price_css)

    def raw_product(self, response):
        raw_product = response.xpath('//script//text()').re("\{.*\:.*\}")
        return json.loads(raw_product[0])

    def raw_description(self, response):
        raw_description = clean(response.css('#description p::text'))
        return raw_description

    def product_care(self, response):
        return [pc for pc in self.raw_description(response) if self.care_criteria(pc)]

    def product_description(self, response):
        return [pd for pd in self.raw_description(response) if not self.care_criteria(pd)]

    def colour_url(self, colour):
        selector = Selector(text=colour)
        colours_url = selector.css('.color li a').re('\(.*,.*,.*,.*\)')
        return [colour.split(",")[1].replace("%20", "") for colour in colours_url]

    def sizes(self, response):
        response = str(response['value'][3])
        selector = Selector(text=response)
        return selector.css('ul[class=""] li')

    def product_category(self, response):
        categories = clean(response.css('#breadcrumbs span a::attr("title")'))
        return categories[1:]

    def sku_id(self, raw_product):
        return raw_product.get('RKProductID')

    def product_gender(self, raw_product):
        product_name = raw_product['RKProductName']
        soup = product_name.lower()
        return self.gender_lookup(soup) or 'unisex-adults'

    def product_web_id(self, raw_product):
        return raw_product.get('RKProductWebID')

    def product_name(self, response):
        return clean(response.css('.name::text'))

    def out_of_stock(self, raw_description):
        return raw_description['RKProductAvailable']

    def image_urls(self, response):
        return clean(response.css('#big_photo_container a::attr(href)'))

    def image_urls_in_request(self, response):
        raw_images = response['value'][1]
        allowed_url = 'http://www.khelf.com.br/Imagens/produtos/'
        return [image for image in raw_images if allowed_url in image and self.ignore_extension not in image]


class KhelfCrawlSpider(BaseCrawlSpider):
    listing = ['#nav']
    product = ['.show-three']

    rules = (Rule(LinkExtractor(restrict_css=listing), callback='parse'),      
             Rule(LinkExtractor(restrict_css=product), callback='parse_item'),
             Rule(PaginationLE(), callback='parse'))


class KhelfBRParseSpider(KhelfParseSpider, MixinBR):
    name = MixinBR.retailer + '-parse'


class KhelfBRCrawlSpider(KhelfCrawlSpider, MixinBR):
    name = MixinBR.retailer + '-crawl'
    parse_spider = KhelfBRParseSpider()
