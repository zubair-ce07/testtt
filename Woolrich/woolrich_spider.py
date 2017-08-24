import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest

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

    genders = [
        'men', 'women'
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

    def parse_color_variants(self, response):
        garment = response.meta['garment']
        garment['image_urls'].extend(self.image_urls(response))
        garment['meta']['requests_queue'].extend(self.size_requests(response))
        return self.next_request_or_garment(garment)

    def parse_size_variants(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'].extend(self.fitting_requests(response))
        return self.next_request_or_garment(garment)

    def parse_fitting_variants(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def fitting_requests(self, response):
        requests = []
        for fitting_sel in response.css('.dimensionslist a'):
            if fitting_sel.css('[stocklevel="0"]'):
                continue
            sku_id = clean(fitting_sel.css('::attr(id)'))[0]
            form_data = {
                'productId': response.meta['garment']['retailer_sku'],
                'colorId': response.meta['color_id'],
                'selectedSize': response.meta['size'],
                'skuId': sku_id
            }
            meta = {
                'garment': response.meta['garment'],
                'color': response.meta['color'],
                'size': response.meta['size'],
                'sku_id': sku_id,
                'fit': clean(fitting_sel.css('::text'))[0]
            }
            requests.append(
                self.form_request(
                    meta=meta,
                    callback=self.parse_fitting_variants,
                    form_data=form_data
                )
            )
        return requests

    def form_request(self, callback, form_data, meta):
        return FormRequest(url=self.product_api_url, callback=callback, dont_filter=True, formdata=form_data, meta=meta)

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
            meta = {
                'garment': garment,
                'color_id': color_id,
                'color': clean(color_sel.css('::attr(title)'))[0]
            }
            requests.append(
                self.form_request(callback=self.parse_color_variants, form_data=form_data, meta=meta)
            )
        return requests

    def size_requests(self, response):
        requests = []
        for size_selector in response.css('.sizelist a'):
            if size_selector.css('[stocklevel="0"]'):
                continue
            size_id = clean(size_selector.css('::attr(id)'))[0]
            size = clean(size_selector.css('::text'))[0]
            form_data = {
                'productId': response.meta['garment']['retailer_sku'],
                'colorId': response.meta['color_id'],
                'selectedSize': size,
            }
            meta = {
                'garment': response.meta['garment'],
                'color_id': response.meta['color_id'],
                'color': response.meta['color'],
                'size': size
            }
            callback = self.parse_size_variants
            if size_id.isdigit() and not size_id == size:
                form_data.update({'skuId': size_id})
                meta.update({'sku_id': size_id})
                callback = self.parse_fitting_variants
            requests.append(
                self.form_request(form_data=form_data, meta=meta,
                                  callback=callback,)
            )
        return requests

    def skus(self, response):
        sku = {}
        color = response.meta['color']
        size = response.meta['size']
        sku_id = response.meta['sku_id']
        sku[sku_id] = {
                'color': color,
                'size': size,
        }

        if 'fit' in response.meta:
            sku[sku_id].update({'fit': response.meta['fit']})
        pricing = self.product_pricing_common_new(response)
        sku[sku_id].update(pricing)
        return sku

    def image_urls(self, response):
        main_image = clean(response.css('[itemprop="image"]::attr(src)'))
        main_image.extend(clean(response.css('#prod-detail__slider-nav img::attr(src)')))
        return main_image

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
        return self.brands[-1]

    def product_name(self, response):
        name = self.raw_name(response)
        name = clean(name.replace(self.product_brand(response), ''))
        return name

    def product_description(self, response):
        description = clean(response.css('[itemprop="description"]::text'))
        description.extend([x for x in clean(response.css('.row .span4 li::text')) if not self.care_criteria_simplified(x)])
        return description

    def product_id(self, response):
        return clean(response.css('[itemprop="productID"]::text'))[0]

    def product_gender(self, response):
        name = self.raw_name(response)
        for gender in self.genders:
            if gender in name.lower():
                return gender
        return 'unisex-adults'

    def raw_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]


class WoolrichCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WoolrichParseSpider()

    listing_css = [
        '.dropdown.yamm-fw a.upper',
        '.nav.nav-list.nav-',
        # pagination-css
        '.clear.addMore'
    ]
    product_css = '.span3.element.productCard a'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=('div', 'a'), attrs=('nextpage', 'href')),
             follow=True, callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css,), follow=True, callback='parse_item')
    )
