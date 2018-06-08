import json
import re

from parsel import Selector
from scrapy.spiders import Rule, Request
from scrapy.http import FormRequest

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean
from w3lib.url import add_or_replace_parameter as add_parameter


class Mixin:
    retailer = 'khelf'
    allowed_domains = ['khelf.com.br']


class MixinBR(Mixin):
    retailer = Mixin.retailer + '-br'
    market = 'BR'
    start_urls = ['http://www.khelf.com.br/tricot-masculino-camuflado-12621.aspx/p']


class KhelfParseSpider(BaseParseSpider):
    price_css = '#lblPrecos'
    request_url = 'http://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,Khelf.ashx'
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
            garment['skus'][product_web_id] = common_sku
        
        return self.next_request_or_garment(garment)

    def request_colour(self, response, garment, product_web_id):
        common_sku = self.product_pricing_common(response)

        if product_web_id:
            parameters = {"ProdutoCodigo": product_web_id, "ColorCode": "0"}
            return [Request(self.request_url, callback=self.parse_colour, method='POST',
                                              body=json.dumps(parameters), 
                                              headers={'X-AjaxPro-Method': 'CarregaSKU', 'Referer': response.url},
                                              meta={'garment': garment, 'product_web_id': product_web_id,
                                                    'common_sku': common_sku})]
    
    def request_sizes(self, colours, garment, response, product_web_id, common_sku):
        requests = []
        for colour in colours:
            parameters = {"CarValorCodigo1": colour, "CarValorCodigo2": "0", "CarValorCodigo3": "0",
                        "CarValorCodigo4": "0", "CarValorCodigo5": "0", "ProdutoCodigo": product_web_id}
            requests.append(Request(self.request_url, callback=self.skus, method='POST', body=json.dumps(parameters),
                                                      headers={'X-AjaxPro-Method': 'DisponibilidadeSKU',
                                                               'Referer': response.url}, 
                                                      meta={'garment': garment, 'colour': colour, 
                                                            'common_sku': common_sku}))

        return requests

    def skus(self, response):
        skus = {}
        garment = response.meta['garment']
        colour = response.meta['colour']
        raw_product = json.loads(response.text)
        common_sku = response.meta.get('common_sku')
        sizes = self.sizes(str(raw_product['value'][3]))

        if not sizes:
            skus[colour.lower()] = common_sku
            garment['skus'] = common_sku
            return self.next_request_or_garment(garment)

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

        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        raw_product = re.findall("dataLayer.push(.+?);", response.text, re.S)[0][1:-1]
        return json.loads(raw_product)

    def raw_description(self, response):
        raw_description = response.css('#description>p::text').extract()
        raw_description += response.css('.especificacion>p::text').extract() or ''
        return raw_description

    def product_care(self, response):
        return [pc for pc in self.raw_description(response) if self.care_criteria(pc)]

    def product_description(self, response):
        return [pd for pd in self.raw_description(response) if not self.care_criteria(pd)]

    def colour_url(self, color):
        colours = []
        ignore_url = ['javascript:;', 'javascript']
        selector = Selector(color)
        colours_url = selector.css('.color>li>a::attr(href)').extract()

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
        return clean(selector.css('.field>ul>li>a::text').extract())

    def out_of_stock_sizes(self, response):
        selector = Selector(response)
        return clean(selector.css('.field>ul>.warn>a::text').extract())

    def image_urls(self, response):
        images = clean(response.css('.images>.thumbs>li>a>img::attr(src)').extract())
        return [image for image in images if self.ignore_extension not in image]

    def product_category(self, response):
        categories = clean(response.css('#breadcrumbs>span>a::attr("title")').extract())
        return categories[1:]

    def sku_id(self, raw_product):
        if 'RKProductID' in raw_product:
            return raw_product['RKProductID']
        
        return None

    def product_web_id(self, raw_product):
        if 'RKProductWebID' in raw_product:
            return raw_product['RKProductWebID']
        
        return None 

    def product_name(self, response):
        return clean(response.css('.name::text').extract_first())

    def out_of_stock(self, raw_description):
        return raw_description['RKProductAvailable']

    def image_urls_in_request(self, response):
        allowed_url = 'http://www.khelf.com.br/Imagens/produtos/'
        return [image for image in response if allowed_url in image and self.ignore_extension not in image]


class KhelfCrawlSpider(BaseCrawlSpider):
    listing = ['#nav']
    product = ['.show-three']

    rules = (Rule(LinkExtractor(restrict_css=listing), callback='parse'),      
             Rule(LinkExtractor(restrict_css=product), callback='parse_item'))


class KhelfBRParseSpider(KhelfParseSpider, MixinBR):
    name = MixinBR.retailer + '-parse'


class KhelfBRCrawlSpider(KhelfCrawlSpider, MixinBR):
    name = MixinBR.retailer + '-crawl'
    parse_spider = KhelfBRParseSpider()
