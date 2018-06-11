import json
import re

from parsel import Selector
from scrapy.spiders import Rule, Request
from scrapy.http import FormRequest
from scrapy.link import Link

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class PaginationLE():
    def extract_links(self, response):
        products_per_page = response.css('option::attr(value)').extract()

        if not products_per_page:
            return [Link(response.url)]

        max_product_limit = max(products_per_page)
        category_code = response.css('#CategoriaCodigo::attr(value)').extract_first()
        page_url = f'http://www.khelf.com.br/categoria/1/{category_code}'

        return [Link(page_url+f'/0//MaisRecente/Decrescente/{max_product_limit}/{pn}//0/0/.aspx') for pn in range(10)]


class Mixin:
    retailer = 'khelf'
    allowed_domains = ['khelf.com.br']


class MixinBR(Mixin):
    retailer = Mixin.retailer + '-br'
    market = 'BR'
    start_urls = ['http://www.khelf.com.br/relogio-casio-g-shock-12529.aspx/p']


class KhelfParseSpider(BaseParseSpider):
    price_css = '#lblPrecos'
    request_url = 'http://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,Khelf.ashx'
    ignore_extension = '.gif'

    gender_map = [
        ('masculino', 'men'),
        ('masculina', 'men'),
        ('masculino', 'men'),
        ('masculinas', 'men'),
        ('feminina', 'women'),
        ('feminininas', 'women'),
        ('feminio', 'women')
    ]


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
        garment['meta'] = {'requests_queue': self.request_colour(response, garment, product_web_id)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        raw_colours = json.loads(response.text)
        garment = response.meta.get('garment')
        product_web_id = response.meta.get('product_web_id')
        common_sku = response.meta.get('common_sku')
        colours = self.colour_url(str(raw_colours['value'][0]))
        garment['meta']['requests_queue'] += self.request_sizes(colours, garment, response,
                                                                product_web_id, common_sku)

        if not garment['meta']['requests_queue']:
            common_sku['size'] = 'U'
            garment['skus'][product_web_id] = common_sku
        
        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = self.skus(response)
        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        garment = response.meta['garment']
        colour = response.meta['colour']
        raw_product = json.loads(response.text)
        common_sku = response.meta.get('common_sku')
        sizes = self.sizes(str(raw_product['value'][3]))

        out_of_stock_sizes = self.out_of_stock_sizes(str(raw_product['value'][3]))
        garment['image_urls'].extend(self.image_urls_in_request(raw_product['value'][1]))
        
        for size in sizes:
            sku = {}
            sku = common_sku.copy()
            sku['size'] = size
            sku['colour'] = colour

            if size in out_of_stock_sizes:
                sku['out_of_stock'] = True

            skus[colour.lower() + '-' + size.lower() if colour else size] = sku
        
        garment['skus'].update(skus)

        return garment

    def request_colour(self, response, garment, product_web_id):
        price = self.raw_price(response)
        try:
            common_sku = self.product_pricing_common(None, money_strs=price)

            if product_web_id:
                parameters = {"ProdutoCodigo": product_web_id, "ColorCode": "0"}
                return [Request(self.request_url, callback=self.parse_colour, method='POST',
                                                  body=json.dumps(parameters), 
                                                  headers={'X-AjaxPro-Method': 'CarregaSKU', 'Referer': response.url},
                                                  meta={'garment': garment, 'product_web_id': product_web_id,
                                                        'common_sku': common_sku})]
        except IndexError:
            return
    
    def request_sizes(self, colours, garment, response, product_web_id, common_sku):
        requests = []
        for colour in colours:
            parameters = {"CarValorCodigo1": colour, "CarValorCodigo2": "0", "CarValorCodigo3": "0",
                          "CarValorCodigo4": "0", "CarValorCodigo5": "0", "ProdutoCodigo": product_web_id}
            requests.append(Request(self.request_url, callback=self.parse_skus, method='POST',
                                                      body=json.dumps(parameters),
                                                      headers={'X-AjaxPro-Method': 'DisponibilidadeSKU',
                                                               'Referer': response.url}, 
                                                      meta={'garment': garment, 'colour': colour, 
                                                            'common_sku': common_sku}))

        return requests

    def raw_price(self, response):
        return clean(response.css('#lblPrecos>span>strong::text'))

    def raw_product(self, response):
        raw_product = re.findall("dataLayer.push(.+?);", response.text, re.S)[0][1:-1]
        return json.loads(raw_product)

    def raw_description(self, response):
        raw_description = clean(response.css('#description p::text'))
        raw_description += clean(response.css('.especificacion p::text'))
        return raw_description

    def product_care(self, response):
        return [pc for pc in self.raw_description(response) if self.care_criteria(pc)]

    def product_description(self, response):
        return [pd for pd in self.raw_description(response) if not self.care_criteria(pd)]

    def colour_url(self, colour):
        colours = []
        ignore_url = ['javascript:;', 'javascript']
        selector = Selector(colour)
        colours_url = selector.css('.color li a::attr(href)').extract()

        for url in colours_url:
            if url in ignore_url:
                continue
            colour = url.replace('javascript:ArmazenaOpcao', '')
            colour = colour[1:-2]
            colour = colour.split(",")
            colours.append((colour[1]).strip())
        
        return colours

    def sizes(self, response):
        selector = Selector(response)
        return clean(selector.css('.field ul li a::text').extract())

    def out_of_stock_sizes(self, response):
        selector = Selector(response)
        return clean(selector.css('.field ul .warn a::text').extract())

    def image_urls(self, response):
        images = clean(response.css('.images .thumbs li a img::attr(src)'))
        return [image for image in images if self.ignore_extension not in image]

    def product_category(self, response):
        categories = clean(response.css('#breadcrumbs span a::attr("title")'))
        return categories[1:]

    def sku_id(self, raw_product):
        if 'RKProductID' in raw_product:
            return raw_product['RKProductID']

    def product_gender(self, raw_product):
        product_name = raw_product['RKProductName']
        soup = product_name.lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender
        return 'unisex-adults'

    def product_web_id(self, raw_product):
        if 'RKProductWebID' in raw_product:
            return raw_product['RKProductWebID']

    def product_name(self, response):
        return clean(response.css('.name::text'))

    def out_of_stock(self, raw_description):
        return raw_description['RKProductAvailable']

    def image_urls_in_request(self, response):
        allowed_url = 'http://www.khelf.com.br/Imagens/produtos/'
        return [image for image in response if allowed_url in image and self.ignore_extension not in image]


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
