from itertools import product

from scrapy.spiders import Request

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'lindex'
    allowed_domains = ['lindex.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'

    start_urls = ['https://www.lindex.com/uk/']
    one_sizes = ['0']


class LindexParseSpider(BaseParseSpider):
    price_css = '.info .amount::text, .info .original_price::text'
    care_css = '.more_info ::text'
    description_css = '.description ::text'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)

        if self.out_of_stock(response, response):
            garment['out_of_stock'] = True
            garment.update(self.product_pricing_common(response))
            return garment

        garment['skus'] = self.skus(response)
        return garment

    def product_id(self, response):
        return clean(response.css('.product_id ::text'))[1]

    def product_name(self, response):
        return clean(response.css('.name::text'))[0]

    def product_brand(self, response):
        css = '[id*="productContainer"]::attr(data-product-brand)'
        brand = clean(response.css(css))
        if brand:
            return brand[0]
        return 'Lindex'

    def product_category(self, response):
        return clean(response.css('#breadcrumbs ::text').re('[a-z A-Z]+'))

    def product_gender(self, garment):
        soup = ' '.join(garment['category']).lower()
        return self.gender_lookup(soup)

    def skus(self, response):
        skus = {}
        colour = response.css('#ProductPage .colors li')
        sizes = response.css('.sizeSelector option:not([value="-1"])')
        common_skus = self.product_pricing_common(response)

        for colour_s, size_s in product(colour, sizes):
            sku = common_skus.copy()

            size = clean(size_s.css('::text'))[0]
            colour_id = clean(colour_s.css('::attr(data-colorid)'))[0]
            size_id = clean(size_s.css('::attr(value)'))[0].split(';')[0]
            split_on_t = '('

            if 'out of stock' in size:
                sku['out_of_stock'] = True
                split_on_t = '-'

            sku['colour'] = clean(colour_s.css('::attr(title)'))[0]
            size = size.split(split_on_t)[0]
            sku['size'] = self.one_size if size.lower() in self.one_sizes else size
            skus[f"{colour_id}_{size_id}"] = sku

        return skus

    def out_of_stock(self, hxs, response):
        css = '#ProductPage .soldout[style*=none]'
        return not response.css(css)

    def image_urls(self, response):
        return clean(response.css('.pagination ::attr(src)'))


class LindexCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.mainMenu'
    ]

    products_css = [
        '.gridPage .info'
    ]

    def parse(self, response):
        links = LinkExtractor(restrict_css=self.listings_css).extract_links(response)
        for i, link in enumerate(links):
            yield Request(link.url,
                          meta={'cookiejar': i},
                          callback=self.parse_pages)

    def parse_pages(self, response):
        server_url_t = '/SiteV3/Category/GetProductGridPage?pageIndex={0}&nodeId={1}'
        request_url_t = response.urljoin(server_url_t)

        page_id = clean(response.css('body::attr(data-page-id)'))[0]
        total_count = int(clean(response.css('#productGrid ::attr(data-page-count)'))[0])

        for idx in range(total_count):
            yield Request(request_url_t.format(idx, page_id),
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_products)

    def parse_products(self, response):
        links = LinkExtractor(restrict_css=self.products_css).extract_links(response)
        for link in links:
            yield Request(link.url,
                          meta={'trail': self.add_trail(response)},
                          callback=self.parse_item)


class LindexParseSpiderUK(LindexParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class LindexCrawlSpiderUK(LindexCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = LindexParseSpiderUK()
