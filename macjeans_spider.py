from scrapy import FormRequest, Request

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'macjeans'
    default_brand = 'Mac'


class MixinAT(Mixin):
    retailer = Mixin.retailer + '-at'
    market = 'AT'
    allowed_domains = [
        'mac-jeans.com'
    ]
    start_urls = [
        'https://mac-jeans.com/at-de/csrftoken'
    ]


class MacJeansParseSpider(BaseParseSpider):
    price_css = '.product--detail-upper .product--price ::text'
    raw_description_css = '.product--description ::text'
    care_css = '.product--properties ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        requests = self.stock_requests(response) + self.colour_requests(response)
        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_stock(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = '[itemprop="sku"]::text'
        return ''.join(response.css(css).re('[\d]+'))

    def product_name(self, response):
        css = '.product--header .product--title::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '.breadcrumb--list a::attr(title)'
        return clean(response.css(css))[1:-1]

    def product_brand(self, response):
        css = '[itemprop="brand"]::attr(content)'
        return clean(response.css(css))[0]

    def image_urls(self, response):
        css = '.product--image-container ' \
              '.image--element::attr(data-img-large)'
        return clean(response.css(css))

    def product_gender(self, response):
        css = '.breadcrumb--list a::attr(title)'
        soup = ' '.join(clean(response.css(css))).lower()
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        css = '.variant--option.selected--option a::attr(title)'
        common_sku['colour'] = clean(response.css(css))[0]
        skus = {}

        css = '.variant--group:first-child .no--stock:not(.is--disabled) ::text'
        out_stock_sizes = clean(response.css(css))

        for size in out_stock_sizes:
            sku = common_sku.copy()
            sku['size'] = size
            sku['out_of_stock'] = True
            sku_id = '_'.join([sku['colour'], size])
            skus[sku_id] = sku

        css = '.variant--group:first-child [checked="checked"] ~ ::text'
        size = clean(response.css(css))[0]
        css = '.variant--group:nth-child(2) label::text'
        lengths = clean(response.css(css))

        css = '.variant--group:nth-child(2) .variant--option.no--stock ::text'
        out_stock_lengths = response.css(css)
        common_sku['size'] = size

        for length in lengths:
            sku = common_sku.copy()
            if length in out_stock_lengths:
                sku['out_of_stock'] = True

            sku_id = '_'.join([sku['colour'], size, length])
            skus[sku_id] = sku

        return skus

    def stock_requests(self, response):
        css = '.variant--group:nth-child(2) .variant--option input::attr(value)'
        length_value = clean(response.css(css))[0]
        formdata = {"group[1]": "", 'group[2]': length_value,
                    '__csrf_token': response.meta['csrf_token']}
        cookies = {'__csrf_token-3': response.meta['csrf_token']}
        requests = []
        css = '.variant--group:first-child .variant--option:not(.no--stock) ' \
              '.option--input:not([checked="checked"])::attr(value)'

        for size in clean(response.css(css)):
            formdata['group[1]'] = size
            requests.append(FormRequest(response.url, formdata=formdata,
                                        cookies=cookies, callback=self.parse_stock))

        return requests

    def colour_requests(self, response):
        css = '.variant--group:first-child ' \
              '.variant--option:not(.selected--option) a::attr(href)'
        urls = clean(response.css(css))
        return [response.follow(url, callback=self.parse_colour, meta=response.meta.copy()) for url in urls]


class MacJeansCrawlSpider(BaseCrawlSpider):
    home_url = 'https://mac-jeans.com/at-de/'
    csrf_token = ''

    def parse_start_url(self, response):
        self.csrf_token = response.headers['X-Csrf-Token'].decode("utf-8")
        meta = {'trail': self.add_trail(response)}
        return Request(self.home_url, callback=self.parse_category, meta=meta.copy())

    def parse_category(self, response):
        meta = {'trail': self.add_trail(response)}
        urls = response.css('#menu-overlay a::attr(href)')
        return [response.follow(url, callback=self.parse_products, meta=meta.copy()) for url in urls]

    def parse_products(self, response):
        css = '.product--info > a::attr(href)'
        urls = clean(response.css(css))

        if not urls:
            return

        meta = {'csrf_token': self.csrf_token,
                'trail': self.add_trail(response)}
        yield from [response.follow(url, callback=self.parse_item, meta=meta.copy())
                    for url in set(urls)]
        css = '.paging--link.is--active ~ a::attr(href)'
        url = clean(response.css(css))

        if not url:
            return

        meta = {'trail': self.add_trail(response)}
        yield response.follow(url[0], callback=self.parse_products, meta=meta.copy())


class MacJeansParseSpiderAT(MacJeansParseSpider, MixinAT):
    name = MixinAT.retailer + '-parse'


class MacJeansCrawlSpiderAT(MacJeansCrawlSpider, MixinAT):
    name = MixinAT.retailer + '-crawl'
    parse_spider = MacJeansParseSpiderAT()
