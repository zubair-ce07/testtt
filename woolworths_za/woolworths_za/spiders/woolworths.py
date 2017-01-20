import re
import time
from scrapy.http.request.form import FormRequest
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider
from woolworths_za.items import WoolworthsItem


class WoolworthsSpider(CrawlSpider):
    name = "woolworths"
    allowed_domains = ["woolworths.co.za"]
    start_urls = ['http://www.woolworths.co.za/store/cat/Men/Clothing/_/N-1z13s3l']
    product_filter = ['/Gifts',
                      '/Beauty',
                      '/Homeware',
                      '/Household',
                      '/Food',
                      '/Essentials',
                      '/Today-s-Deal'
                      ]
    rules = [
        Rule(LinkExtractor(restrict_css=[
            'div.horizontal-menu-container',
            'ul.nav-list--main',
            'ol.pagination__pages',
        ])),
        Rule(LinkExtractor(restrict_css='a.product-card__details',
                           deny=product_filter),
             callback='parse_item'),
    ]

    def parse_item(self, response):
        garment = WoolworthsItem()
        garment['name'] = self.product_name(response)
        garment['brand'] = self.product_brand(response)
        garment['category'] = self.product_category(response)
        garment['retailer'] = 'woolworths'
        garment['price'] = self.product_price(response)
        if self.is_sale(response):
            garment['previous_price'] = self.product_old_price(response)
        garment['currency'] = self.product_currency(response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.product_images(response)
        garment['description'] = self.product_description(response)
        garment['industry'] = None
        garment['market'] = 'ZA'
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['care'] = self.product_care(response)
        garment['date'] = int(time.time())
        garment['skus'] = {}
        garment['images'] = self.get_images(response)
        skus = self.get_skus(response)
        return self.fetch_skus(garment, skus)

    def product_name(self, response):
        selector = 'meta[itemprop="name"]::attr(content)'
        return response.css(selector).extract_first()

    def product_brand(self, response):
        selector = 'meta[itemprop="brand"]::attr(content)'
        return response.css(selector).extract_first()

    def product_category(self, response):
        selector = 'li.breadcrumb__crumb a::text'
        return response.css(selector).extract()

    def product_currency(self, response):
        selector = 'meta[itemprop="priceCurrency"]::attr(content)'
        return response.css(selector).extract_first()

    def product_description(self, response):
        selector = 'meta[itemprop="description"]::attr(content)'
        return response.css(selector).extract()

    def product_retailer_sku(self, response):
        selector = 'meta[itemprop="productId"]::attr(content)'
        return response.css(selector).extract_first()

    def product_color(self, response):
        selector = 'meta[itemprop="color"]::attr(content)'
        return response.css(selector).extract_first().strip()

    def get_product_colors(self, response):
        color_elems = response.css('img.colour-swatch')
        colors = []
        pattern = re.compile('changeMainProductColour\((\d+)')
        for elem in color_elems:
            onclick = elem.css('::attr(onclick)').extract_first()
            colors += [
                {
                    'title': elem.css('::attr(title)')
                        .extract_first()
                        .strip(),
                    'id': re.findall(pattern, onclick)[0]
                }
            ]
        return colors

    def get_product_sizes(self, response):
        size_elems = response.css('a.product-size')
        sizes = []
        pattern = re.compile('changeMainProductSize\(\d+,(\d+)')
        selector = '::attr(onclick)'
        for elem in size_elems:
            onclick = elem.css(selector).extract_first()
            title = elem.css('::text').extract_first().replace(' ', '_')
            id = re.findall(pattern, onclick)[0]
            sizes += [{'title': title, 'id': id}]
        return sizes

    def get_skus(self, response):
        colors = self.get_product_colors(response)
        sizes = self.get_product_sizes(response)
        return [(color, size) for color in colors for size in sizes]

    def get_images(self, response):
        colors = self.get_product_colors(response)
        return [color['id'] for color in colors]

    def parse_sku_price(self, response):
        garment = response.meta['garment']
        skus = response.meta['skus']
        id, sku = self.make_sku(response).popitem()
        garment_skus = garment['skus']
        garment_skus[id] = sku
        if skus:
            return self.fetch_skus(garment, skus)

        images = garment['images']
        if images:
            return self.fetch_images(garment, images)

        return garment

    def fetch_skus(self, garment, skus):
        if skus:
            color, size = skus.pop()
            price_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp'
            meta = {'garment': garment,
                    'skus': skus,
                    'color': color,
                    'size': size,
                    }
            formdata = {'productItemId': garment['retailer_sku'],
                        'colourSKUId': color['id'],
                        'sizeSKUId': size['id'],
                        }
            yield FormRequest(url=price_url, formdata=formdata, callback=self.parse_sku_price, meta=meta)

    def price_from_ajax(self, response):
        price_css = 'span.price::text'
        return int(response.css(price_css).re_first('[\d|\.]+').replace('.', ''))

    def make_sku(self, response):
        garment = response.meta['garment']
        color = response.meta['color']
        size = response.meta['size']
        price = self.price_from_ajax(response)
        currency = garment['currency']
        sku_id = color['title'].replace(' ', '_') + '_' + size['title']
        sku = {
                'color': color['title'],
                'size': size['title'],
                'price': price,
                'currency': currency,
            }
        prev_price = garment.fields.get('previous_price')
        if prev_price:
            sku.update({'previous_price':prev_price})
        return {sku_id: sku}

    def product_price(self, response):
        selector = 'meta[itemprop="price"]::attr(content)'
        return int(response.css(selector).extract_first().replace('.', ''))

    def product_old_price(self, response):
        selector = 'span.price--original::text'
        return int(response.css(selector).re_first('[\d|\.]+').replace('.', ''))

    def product_images(self, response):
        selector = 'a[data-gallery-full-size]::attr(data-gallery-full-size)'
        return ['http://' + link.lstrip('/')
                for link in response.css(selector).extract()]

    def fetch_images(self, garment):
        images = garment['images']
        color_id = images.pop()
        product_id = garment['retailer_sku']
        image_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/image-shots.jsp'
        meta = {
            'garment': garment,
        }
        formdata = {
            'colourSKUId': color_id,
            'productId': product_id,
        }
        return FormRequest(url=image_url, formdata=formdata, callback=self.parse_image, meta=meta)

    def parse_image(self, response):
        garment = response.meta['garment']
        images = garment['images']
        urls = self.ajax_extract_images(response)
        garment['image_urls'].extend(urls)
        if images:
            return self.fetch_images(garment)
        return garment

    def ajax_extract_images(self, response):
        urls = response.css('div.pdp__image img::attr(src)').extract()
        return ['http://' + url.lstrip('/') for url in urls]

    def is_sale(self, response):
        return response.css('span.price--discounted')

    def product_care(self, response):
        desc = self.product_description(response)
        pattern = re.compile('\d+%.*$', re.MULTILINE)
        return re.findall(pattern, desc[0])

    def product_gender(self, response):
        patterns = [
            ('men', '/Men'),
            ('women', '/Women'),
            ('boys', '/Boys'),
            ('girls', '/Girls'),
            ('unisex', '/Unisex'),
            ('unisex-kids', '/School-Uniform'),
        ]

        for gender, gender_pattern in patterns:
            if gender_pattern in response.url:
                return gender
