import re
import json
import codecs
from urllib.parse import\
    urlsplit, urlunsplit, urlencode, parse_qsl

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider

from crawler_tasks.items import GenericProduct


class AmazonUkSpider(Spider):
    name = 'amazon_uk'
    allowed_domains = ['amazon.co.uk']
    start_urls = [
        'https://www.amazon.co.uk/b/ref=nav_shopall_sa_wmn?'
        'ie=UTF8&node=11360243031',

        'https://www.amazon.co.uk/b/ref=nav_shopall_sa_men?'
        'ie=UTF8&node=9337137031',

        'https://www.amazon.co.uk/b/ref=nav_shopall_sa_kids?'
        'ie=UTF8&node=9337138031',

        'https://www.amazon.co.uk/Jewellery-Rings-Earrings-Bracelets-Necklaces-Diamonds'
        '/b/ref=nav_shopall_sa_jwl?ie=UTF8&node=193716031',

        'https://www.amazon.co.uk/Watches-Chronograph-Analogue-Digital-Automatic'
        '/b/ref=nav_shopall_sa_wat?ie=UTF8&node=328228011',

        'https://www.amazon.co.uk/Totes-Clutch-Shoulderbag-Messengerbag-Satchel'
        '/b/ref=nav_shopall_sa_bags?ie=UTF8&node=1769551031',

        'https://www.amazon.co.uk/luggage/b/ref=nav_shopall_sa_lug?'
        'ie=UTF8&node=2454166031',

        'https://www.amazon.co.uk/sunglasses-accessories-oakley'
        '/b/ref=nav_shopall_sa_sunglasses?ie=UTF8&node=362410011'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 12
    }

    default_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    genders_types = [
        'women', 'men', 'girls', 'boys'
    ]

    def parse(self, response):
        urls = self.sub_category_urls(response)
        if not urls:
            urls = self.left_navigation_urls(response)

        for url in urls:
            complete_url = response.urljoin(url)
            yield self.reset_cookies(
                Request(complete_url, headers=self.default_headers,
                        callback=self.traverse_sub_categories)
            )
            # TODO: remove break
            # break

    def sub_category_urls(self, response):
        sub_category_section = response.css('[class="categoryRefinementsSection"]')
        if sub_category_section:
            return sub_category_section.css('li:not([class]) ::attr(href)').extract()

        return []

    def left_navigation_urls(self, response):
        left_navigations = response.css('.left_nav')
        for nav_section in left_navigations:
            nav_urls = nav_section.css('::attr(href)').extract()
            if nav_urls and '/s/ref=amb_link' in nav_urls[0]:
                return nav_urls

        return []

    def traverse_sub_categories(self, response):
        sub_category_urls = self.sub_category_urls(response)
        if not sub_category_urls:
            return self.parse_product_listing(response)

        sub_category_requests = []
        for url in sub_category_urls:
            complete_url = response.urljoin(url)
            sub_category_requests.append(
                self.reset_cookies(
                    Request(complete_url, headers=self.default_headers,
                            callback=self.traverse_sub_categories)
                )
            )
            # TODO: remove break
            # break

        return sub_category_requests

    def parse_product_listing(self, response):
        items = response.css('[id^="result_"]')
        for item in items:
            url = item.css(
                ':not([href*="bestseller"])::attr(href)'
            ).extract_first()

            complete_url = response.urljoin(url)
            yield self.reset_cookies(
                Request(complete_url, headers=self.default_headers,
                        callback=self.parse_product)
            )
            # TODO: remove return
            # return

        pagination_url =\
            response.css('[id="pagnNextLink"]::attr(href)').extract_first()
        if not pagination_url:
            return None

        pagination_url = response.urljoin(pagination_url)
        return self.reset_cookies(
            Request(pagination_url, headers=self.default_headers,
                    callback=self.parse_product_listing)
        )

    def parse_product(self, response):
        product = GenericProduct()
        product['merch_info'] = []
        product['product_id'] = ''
        product['market'] = 'UK'
        product['url'] = response.url
        product['description'] = self.strip_text_items(
            response.css('#productDescription ::text').extract()
        )
        product['care'] = self.strip_text_items(
            response.css('#feature-bullets ::text').extract()
        )
        product['name'] = self.product_name(response)
        product['category'] = self.product_category(response)
        product['brand'] = self.brand_name(response)
        product['gender'] = self.product_gender(product['category'])
        product['image_urls'] = self.image_urls(response)

        return self.parse_sku_variations(response, product)

    def strip_text_items(self, items):
        return [item.strip() for item in items if item.strip()]

    def product_name(self, response):
        name = response.css('#productTitle::text').extract_first()
        if not name:
            name = self.strip_text_items(
                response.css('#btAsinTitle ::text').extract()
            )[0]

        return name.strip()

    def product_category(self, response):
        texts = response.css('#showing-breadcrumbs_div a::text').extract()
        if texts:
            return self.strip_text_items(texts)

        return self.strip_text_items(
            response.css('#wayfinding-breadcrumbs_feature_div a::text').extract()
        )

    def brand_name(self, response):
        brand = response.css('#brand ::text').extract_first()
        if brand:
            return brand.strip()

        return ''

    def product_gender(self, categories):
        lower_case_categories = [s.lower() for s in categories]
        for gender in self.genders_types:
            for category in lower_case_categories:
                if gender in category:
                    return gender
        return ''

    def image_urls(self, response):
        raw_text = self.raw_image_urls(response)
        if not raw_text:
            return []

        urls = []
        images = json.loads(raw_text)
        for color, color_images in images.items():
            for image_set in color_images:
                img_url = image_set.get('hiRes')
                if not img_url:
                    img_url = image_set.get('large')
                urls.append(img_url)

        return urls

    def raw_image_urls(self, response):
        regexes = [
            'data\["colorImages"\] =(.*);',
            "colorImages': (.*),\s+'",
            'var colorImages = (.*);'
        ]
        for regex in regexes:
            raw_text = response.css('script').re(regex)
            if raw_text and 'http' in raw_text[0]:
                return raw_text[0].replace("\'initial\'", '"initial"')

        return None

    def parse_sku_variations(self, response, product):
        sku_variations = response.css('script')\
            .re('dimensionValuesDisplayData" :(.*),\s+?"')
        if not sku_variations:
            product['skus'] = {
                'sku_id': self.product_price(response)
            }
            return product

        sku_variations = json.loads(sku_variations[0])
        sku_variations = self.label_sku_variations(response, sku_variations)
        sku_id, sku = self.current_sku(response, sku_variations)
        product['skus'] = {
            sku_id: sku
        }
        del sku_variations[sku_id]

        product['meta'] = {
            'sku_variations': sku_variations,
            'request_queue': self.prepare_sku_requests(
                response, sku_variations.keys()),
        }
        return self.next_request_or_product(product)

    def label_sku_variations(self, response, sku_variations):
        labels = response.css('script')\
            .re('"dimensions" :(.*),\s+?"')
        labels = json.loads(labels[0])

        labeled_variation = {}
        for id, variation in sku_variations.items():
            labeled_variation[id] =\
                {key: value for key, value in zip(labels, variation)}

        return labeled_variation

    def current_sku(self, response, sku_variations):
        sku_id = response.css('script')\
            .re('currentAsin" : "(\w+)"')[0]
        current_sku = self.product_price(response)
        current_sku['size'] = sku_variations[sku_id].get('size_name', '')
        current_sku['colour'] = sku_variations[sku_id].get('color_name', '')

        return sku_id, current_sku

    def prepare_sku_requests(self, response, sku_ids):
        sku_url_prefix = response.css('script')\
            .re('"immutableURLPrefix":"([^,]+)"')[0]
        psc = response.css('script')\
            .re('"full":{"mTypeSpecificURLParams":{"psc":(\d+)}')[0]

        sku_url_prefix = response.urljoin(sku_url_prefix)

        sku_requests = []
        for sku_id in sku_ids:
            sku_url = self.prepare_sku_request_url(
                sku_url_prefix, sku_id, psc)
            meta = {
                'sku_id': sku_id
            }
            sku_requests.append(
                self.reset_cookies(
                    Request(sku_url, headers=self.default_headers,
                            meta=meta, callback=self.parse_sku)
                )
            )
            #TODO: remove break
            # break

        return sku_requests

    def prepare_sku_request_url(self, url_prefix, sku_id, psc):
        other_params = [
            ('psc', psc),
            ('asinList', sku_id),
            ('id', sku_id),
            ('mType', 'full')
        ]

        scheme, net_loc, path, query, fragment = urlsplit(url_prefix)
        params = parse_qsl(query)
        params.extend(other_params)
        query = urlencode(params)

        return urlunsplit(
            (scheme, net_loc, path, query, fragment)
        )

    def parse_sku(self, response):
        product = response.meta['product']
        sku_id = response.meta['sku_id']
        sku_variations = product['meta']['sku_variations']

        selector = self.sku_response_selector(response)
        sku = self.product_price(selector)
        sku['size'] = sku_variations[sku_id].get('size_name', '')
        sku['colour'] = sku_variations[sku_id].get('color_name', '')

        product['skus'][sku_id] = sku
        return self.next_request_or_product(product)

    def sku_response_selector(self, response):
        raw_text = response.body.decode()
        price_div = re.search('price_feature_div":"(.*)}', raw_text).group()
        unescaped_text = codecs.escape_decode(price_div.encode())[0]
        return Selector(text=unescaped_text)

    def product_price(self, selector):
        price = selector.css('#priceblock_ourprice::text').extract_first()
        previous_price = ''
        if not price:
            price = selector.css(
                '#priceblock_saleprice::text'
            ).extract_first()
            previous_price = selector.css(
                '[class="a-text-strike"]::text'
            ).extract_first()

        if price:
            return self.apply_price_regex(price, previous_price)

        return {
            'currency': '',
            'price': '',
            'previous_price': ''
        }

    def apply_price_regex(self, price, previous_price):
        price_regex = '([^0-9 ]+)(.*)'
        price_match = re.search(price_regex, price)

        if previous_price:
            previous_price = re.search(
                price_regex, previous_price).group(2)

        return {
            'currency': price_match.group(1),
            'price': price_match.group(2),
            'previous_price': previous_price
        }

    def next_request_or_product(self, product):
        request_queue = product['meta']['request_queue']
        if request_queue:
            request = request_queue.pop()
            request.meta['product'] = product
            request.priority = 1
            return request

        del product['meta']
        return product

    def reset_cookies(self, request):
        request.meta['dont_merge_cookies'] = True
        request.cookies = {}
        return request
