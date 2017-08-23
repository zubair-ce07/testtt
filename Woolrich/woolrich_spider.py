import json
import re
from termcolor import colored

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, FormRequest, Selector

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'woolrich-us'
    lang = 'en'
    market = 'US'

    allowed_domains = ['woolrich.com']
    start_urls = ['http://www.woolrich.com/woolrich/?countryCode=US']


class WoolrichParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    product_api_url = 'http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp'
    price_css = '#productDetails .dividers .price .price_sale span::text, .price_reg.strikethrough::text, .price'

    brands = [

        'Frost River X Woolrich',
        'Topo X Woolrich',
        'Westerlind X Woolrich',
        'Dogfish X Woolrich',
        'Converse X Woolrich',
        'The Hill-Side X Woolrich',
        'Woolrich'
    ]

    gender_map = [
        'Men', 'Women'
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = response.css('img[itemprop="image"]::attr(src)').extract()
        garment['image_urls'].extend(response.css('#prod-detail__slider-nav img::attr(src)').extract())
        garment['gender'] = self.product_gender(response)

        garment['meta'] = {
            'requests_queue': self.garment_requests(response, product_id, garment),
        }

        return self.next_request_or_garment(garment)

    def garment_requests(self, response, prodId, garment):
        color_ids = self.product_color_ids(response)
        requests = []
        for colorid in color_ids:
            requests.append(
                FormRequest(
                    url=self.product_api_url,
                    formdata={
                        'productId': prodId,
                        'colorId': colorid['color'],
                    },
                    callback=self.parse_color_variants,
                    dont_filter=True,
                    meta={
                        'garment': garment,
                        'product_id': prodId,
                        'color_id': colorid['color']
                    }
                )
            )
        return requests

    def parse_color_variants(self, response):
        garment = response.meta['garment']
        garment['image_urls'].extend(self.image_urls(response))
        color = response.meta['color_id']
        product_id = response.meta['product_id']
        requests = []
        for indx, size in enumerate(self.product_sizes(response)):
            if not size['out_of_stock']:
                if not self.is_size_id(response):
                    requests.append(
                        FormRequest(
                            url=self.product_api_url,
                            formdata={
                                'productId': product_id,
                                'colorId': color,
                                'selectedSize': size['size'],
                            },
                            callback=self.parse_size_variants,
                            dont_filter=True,
                            meta={
                                'garment': garment,
                                'product_id': product_id,
                                'color_id': color,
                                'size': size['size']
                            }
                        )
                    )
                else:
                    id_from_size = self.id_from_size(response)
                    requests.append(
                        FormRequest(
                            url=self.product_api_url,
                            formdata={
                                'productId': product_id,
                                'colorId': color,
                                'selectedSize': size['size'],
                                'skuId': id_from_size[indx]
                            },
                            callback=self.parse_product_final_variants,
                            dont_filter=True,
                            meta={
                                'garment': garment,
                                'product_id': product_id,
                                'color_id': color,
                                'sku_id': id_from_size[indx],
                                'size': size['size']
                            }
                        )
                    )
            else:
                pricing = self.product_pricing_common_new(response)
                garment['skus'].update({
                    color + '_' + size['size'] + '_' + product_id: {
                        'color': color,
                        'size': size['size'],
                        'out_of_stock': size['out_of_stock'],
                        'price': pricing['price'],
                        'currency': pricing['currency']
                    }
                })
        garment['meta']['requests_queue'].extend(requests)
        return self.next_request_or_garment(garment)

    def parse_size_variants(self, response):
        garment = response.meta['garment']
        size = response.meta['size']
        color = response.meta['color_id']
        product_id = response.meta['product_id']

        requests = []
        for sku in self.product_skuID(response):
            if not sku['out_of_stock']:
                requests.append(
                    FormRequest(
                        url=self.product_api_url,
                        formdata={
                            'productId': product_id,
                            'colorId': color,
                            'selectedSize': size,
                            'skuId': sku['sku_id']
                        },
                        callback=self.parse_product_final_variants,
                        dont_filter=True,
                        meta={
                            'garment': garment,
                            'product_id': product_id,
                            'color_id': color,
                            'size': size,
                            'sku_id': sku['sku_id']
                        }
                    )
                )
            else:
                pricing = self.product_pricing_common_new(response)
                garment['skus'].update({
                    color + '_' + size + '_' + product_id: {
                        'color': color,
                        'size': size,
                        'out_of_stock': sku['out_of_stock'],
                        'sku_id': sku['sku_id'],
                        'price': pricing['price'],
                        'currency': pricing['currency']
                    }
                })
        garment['meta']['requests_queue'].extend(requests)
        return self.next_request_or_garment(garment)

    def parse_product_final_variants(self, response):
        garment = response.meta['garment']
        color_id = response.meta['color_id']
        size = response.meta['size']
        sku_id = response.meta['sku_id']
        product_id = response.meta['product_id']
        pricing = self.product_pricing_common_new(response)
        garment['skus'].update({
            color_id + '_' + size + '_' + product_id: {
                'color': color_id,
                'size': size,
                'out_of_stock': False,
                'sku_id': sku_id,
                'price': pricing['price'],
                'currency': pricing['currency']
            }
        })
        return self.next_request_or_garment(garment)

    def product_skuID(self, response):
        r = re.compile('id="([\d]+)"')
        temp = []
        try:
            temp = [{
                'sku_id': r.search(x).group(1) or None,
                'out_of_stock': 'stocklevel="0"' in x
            } for x in response.css('.dimensionslist li a').extract(
            )]
        except Exception:
            pass

        return temp

    def parse_product_variants(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    # def skus(self, response):
    #     skus = {}
    #     body = str(response.request.body)
    #     regex_color = re.compile('colorId=([a-zA-Z]+)')
    #     regex_size = re.compile('selectedSize=([a-zA-Z0-9]+)')
    #     color_id = regex_color.search(body).group(1)
    #     size_id = regex_size.search(body).group(1)
    #     sku_id = color_id + '_' + (size_id or '') + '_' + re.compile(
    #         'productId=([\d]+)').search(body).group(1)
    #     # TODO - get pricing right
    #     price = 'price is not here for now'
    #     skus = {
    #         sku_id: {
    #             'price': price,
    #             'color': color_id,
    #             'size': size_id
    #         }
    #     }
    #     return skus

    def id_from_size(self, response):
        aq = response.css('.sizelist li a').extract()
        arr = [re.compile('id="([\d]+)"').search(val).group(1) for val in response.css('.sizelist li a').extract()]
        return arr

    def is_size_id(self, response):
        if 'id' not in response.css('.sizelist li a').extract_first():
            return False
        r = re.compile('id="([\d]+)"')
        if r.search(response.css('.sizelist li a').extract_first()) is None:
            return False
        return True

    def image_urls(self, response):
        return response.css('#prod-detail__slider-nav img::attr(src)').extract()

    def product_category(self, response):
        return response.css('.wrap.breadcrumb .container a::text').extract()[1:]

    def product_care(self, response):
        features = response.css('.row.pdp_specs .span4 li::text').extract()
        care = []
        care.extend([x for x in features if self.care_criteria_simplified(x)])
        return care

    def product_brand(self, response):
        name = response.css('h1[itemprop="name"]::text').extract_first()
        for brand in self.brands:
            if brand in name:
                return brand
        return self.brands[-1]

    # def product_fitting(self, response):
    #     r = re.compile('>([\s\S]*)<')
    #     fittings = [r.search(x).group(1).strip() for x in
    #             response.css('.dimensionslist li a').extract() if 'stocklevel="0"' not in x]
    #     if(len(fittings) == 0):
    #         r = re.compile('id="([\d]+)"')
    #         fittings = [r.search(x).group(1) for x in response.css('.sizelist li a').extract() if 'stocklevel="0"' not in x]
    #     return fittings

    def product_sizes(self, response):
        sizes = response.css(".sizelist li a::text").extract()
        out_of_stock = ['stocklevel="0"' in x for x in response.css(".sizelist li a").extract()]
        return [{'size': val, 'out_of_stock': out_of_stock[indx]} for indx, val in enumerate(sizes)]

    def product_color_ids(self, response):
        colors = response.css(".colorlist li a img::attr(colorid)").extract()
        color_links = response.css(".colorlist li a").extract()
        in_stock = [ 'disabled' not in x  for x in color_links]
        return [{'color': val, 'out_of_stock': in_stock[indx]} for indx, val in enumerate(colors)]

    def product_name(self, response):
        name =  response.css('h1[itemprop="name"]::text').extract_first()
        for brand in self.brands:
            if brand in name:
                name = name.replace(brand, '').strip()
        return name

    def product_description(self, response):
        description = response.css('span[itemprop="description"]::text').extract_first()
        description += '. '.join([x for x in response.css('.row.pdp_specs .span4 li::text').extract() if 'wash' not in x and 'Care' not in x and 'clean' not in x])
        return description

    def product_id(self, response):
        return response.css('span[itemprop="productID"]::text').extract_first()

    def product_gender(self, response):
        name = response.css('h1[itemprop="name"]::text').extract_first()
        for gender in self.gender_map:
            if gender in name:
                return gender
        return 'unisex-adults'

class WoolrichCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WoolrichParseSpider()

    listing_css = [
        '.dropdown.yamm-fw a.upper',
        '.nav.nav-list.nav-',
    ]
    pagination_css = [
        '.clear.addMore'
    ]
    product_css = '.span3.element.productCard a'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css,), follow=True,
             callback='paging_requests'),
        Rule(LinkExtractor(restrict_css=pagination_css, tags=('div',),
                           attrs=('nextpage',)),
             follow=True, callback='paging_requests'),
        Rule(LinkExtractor(restrict_css=product_css,), callback='parse_item')
    )

    def paging_requests(self, response):
        # print(colored(response, 'red'))
        pass
