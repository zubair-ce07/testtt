from scrapy import FormRequest, Request

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'macjeans'
    default_brand = 'Mac'


class MixinAT(Mixin):
    retailer = Mixin.retailer + '-at'
    market = 'AT'
    allowed_domains = ['mac-jeans.com']
    start_urls = ['https://mac-jeans.com/at-de/csrftoken']
    home_url = 'https://mac-jeans.com/at-de/'


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    allowed_domains = ['mac-jeans.com']
    start_urls = ['https://mac-jeans.com/de-de/csrftoken']
    home_url = 'https://mac-jeans.com/de-de/'


class MacJeansParseSpider(BaseParseSpider):
    price_css = '.product--detail-upper .product--price ::text'
    raw_description_css = '.product--description ::text'
    care_css = '.product--properties ::text, block-prices--cell ::text'
    brand_css = '[itemprop="brand"]::attr(content)'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        requests = self.size_requests(response) + self.colour_requests(response)
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
        return ''.join(response.css(css).re('\d'))

    def product_name(self, response):
        css = '.product--header .product--title::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '.breadcrumb--list a::attr(title)'
        return clean(response.css(css))[1:-1]

    def image_urls(self, response):
        css = '.product--image-container .image--element::attr(data-img-large)'
        return clean(response.css(css))

    def product_gender(self, response):
        css = '.breadcrumb--list a::attr(title)'
        soup = ' '.join(clean(response.css(css)))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        colour_css = '.variant--option.selected--option a::attr(title)'
        common_sku['colour'] = clean(response.css(colour_css))[0]
        skus = {}

        length_css = '.variant--group:contains(Länge) .variant--option:not(.no--stock) ::text'
        lengths = clean(response.css(length_css))
        size_css = '.variant--group:contains(Größe) [checked="checked"] ~ ::text'
        common_sku['size'] = clean(response.css(size_css))[0]

        for length in lengths:
            sku = common_sku.copy()

            sku_id = '_'.join([sku['colour'], sku['size'], length])
            skus[sku_id] = sku

        return skus

    def size_requests(self, response):
        length_css = '.variant--group:contains(Länge) .variant--option input::attr(value)'
        length_value = clean(response.css(length_css))[0]
        formdata = {'__csrf_token': response.meta['csrf_token'],
                    'group[2]': length_value, }
        cookies = {'__csrf_token-3': response.meta['csrf_token'],
                   '__csrf_token-1': response.meta['csrf_token']}
        requests = []
        size_css = '.variant--group:contains(Größe) .variant--option:not(.no--stock) ' \
                   '.option--input:not([checked="checked"])::attr(value)'

        for size in clean(response.css(size_css)):
            formdata['group[1]'] = size
            requests.append(FormRequest(response.url, formdata=formdata,
                                        cookies=cookies, callback=self.parse_stock))

        return requests

    def colour_requests(self, response):
        css = '.variant--group:contains(Größe) ' \
              '.variant--option:not(.selected--option) a::attr(href)'
        urls = clean(response.css(css))
        return [response.follow(url, callback=self.parse_colour, meta=response.meta.copy()) for url in urls]


class MacJeansCrawlSpider(BaseCrawlSpider):
    def parse_start_url(self, response):
        meta = {'trail': self.add_trail(response),
                'csrf_token': response.headers['X-Csrf-Token'].decode("utf-8")}
        return Request(self.home_url, callback=self.parse_category, meta=meta.copy())

    def parse_category(self, response):
        response.meta['trail'] = self.add_trail(response)
        urls = response.css('#menu-overlay a::attr(href)')
        return [response.follow(url, callback=self.parse_listing, meta=response.meta.copy()) for url in urls]

    def parse_listing(self, response):
        yield from self.product_requests(response)
        url = clean(response.css('.paging--link.is--active ~ a::attr(href)'))

        if not url:
            return

        yield response.follow(url[0], callback=self.parse_listing, meta=response.meta.copy())

    def product_requests(self, response):
        products_url_css = '.product--info > a::attr(href)'
        urls = clean(response.css(products_url_css))

        if not urls:
            return []

        response.meta['trail'] = self.add_trail(response)
        return [response.follow(url, callback=self.parse_item, meta=response.meta.copy())
                for url in set(urls)]


class MacJeansParseSpiderAT(MacJeansParseSpider, MixinAT):
    name = MixinAT.retailer + '-parse'


class MacJeansCrawlSpiderAT(MacJeansCrawlSpider, MixinAT):
    name = MixinAT.retailer + '-crawl'
    parse_spider = MacJeansParseSpiderAT()


class MacJeansParseSpiderDE(MacJeansParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class MacJeansCrawlSpiderDE(MacJeansCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = MacJeansParseSpiderDE()
