from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest
from urllib.parse import parse_qsl
from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'woolrich-us'
    market = 'US'

    allowed_domains = ['woolrich.com']
    start_urls = ['http://www.woolrich.com/woolrich/?countryCode=US']


class WoolrichParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    product_api_url = 'http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp'
    price_css = '.price ::text'

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
        ('Men', 'men'),
        ('Women', 'women')
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)

        garment['meta'] = {
            'requests_queue': self.color_requests(response, garment),
        }

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.size_requests(response)
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.fitting_requests(response)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_fitting(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def fitting_requests(self, response):
        requests = []
        for fitting_sel in response.css('.dimensionslist a:not([stocklevel="0"])'):
            sku_id = clean(fitting_sel.css('::attr(id)'))[0]
            form_data = dict(parse_qsl(response.request.body.decode()))
            form_data.update({'skuId': sku_id})
            requests.append(
                self.variant_request(
                    callback=self.parse_fitting,
                    form_data=form_data
                )
            )
        return requests

    def variant_request(self, callback, form_data):
        return FormRequest(url=self.product_api_url, callback=callback, dont_filter=True, formdata=form_data)

    def color_requests(self, response, garment):
        requests = []
        for color_sel in response.css('#productDetails .colorlist .link'):
            if color_sel.css('.disabled'):
                continue
            color_id = clean(color_sel.css('img::attr(colorid)'))[0]
            form_data = {
                'productId': garment['retailer_sku'],
                'colorId': color_id
            }
            requests.append(
                self.variant_request(callback=self.parse_color, form_data=form_data)
            )
        return requests

    def size_requests(self, response):

        requests = []
        for size_selector in response.css('.sizelist a:not([stocklevel="0"])'):
            size = clean(size_selector.css('::text'))[0]
            form_data = dict(parse_qsl(response.request.body.decode()))
            form_data.update({'selectedSize': size})
            sku_id_size = clean(size_selector.css('::attr(id)'))[0]
            if not sku_id_size == size:
                form_data.update({'skuId': sku_id_size})
            requests.append(
                self.variant_request(form_data=form_data, callback=self.parse_size)
            )
        return requests

    def skus(self, response):
        skus = {}
        sku = self.product_pricing_common_new(response)
        css = '.sizelist option[selected] ::text, .dimensionslist option[selected] ::text'
        size = '/'.join(clean(response.css(css)))
        sku['size'] = self.one_size if 'EA' in size else size
        sku['colour'] = clean(response.css('.colorlist .selected::attr(title)'))[0]
        sku_id = clean(response.css('.sizelist .selected::attr(id)'))[0]
        if sku_id == size and response.css('.selected.childDimensions'):
            sku_id = clean(response.css('.selected.childDimensions::attr(id)'))[0]
        elif sku_id == size:
            return skus
        skus[sku_id] = sku
        return skus

    def image_urls(self, response):
        css = '[itemprop="image"]::attr(src), #prod-detail__slider-nav img::attr(src)'
        image_urls = clean(response.css(css))
        return image_urls

    def product_category(self, response):
        return clean(response.css('.wrap.breadcrumb a::text'))[1:]

    def product_care(self, response):
        features = clean(response.css('.row .span4 li::text'))
        return [x for x in features if self.care_criteria_simplified(x)]

    def product_brand(self, response):
        name = self.raw_name(response)
        for brand in self.brands:
            if brand in name:
                return brand
        return 'Woolrich'

    def product_name(self, response):
        name = self.raw_name(response)
        return clean(name.replace(self.product_brand(response), ''))

    def product_description(self, response):
        css = '[itemprop="description"]::text, .pdp_specs li::text'
        description = clean(response.css(css))
        return description

    def product_id(self, response):
        return clean(response.css('[itemprop="productID"]::text'))[0]

    def product_gender(self, response):
        name = self.raw_name(response)
        for gender_str, gender in self.gender_map:
            if gender_str in name:
                return gender
        return 'unisex-adults'

    def raw_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]


class WoolrichCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WoolrichParseSpider()

    listing_css = [
        '.nav.navbar-nav .upper',
        '.nav.nav-list.nav-',
        '.clear.addMore'
    ]
    product_css = '.productCard'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=('div', 'a'), attrs=('nextpage', 'href')),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css,), callback='parse_item')
    )
