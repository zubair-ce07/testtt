from w3lib.url import add_or_replace_parameters

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    retailer = 'americangolf'
    spider_one_sizes = ['One Size']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    allowed_domains = ['americangolf.co.uk']
    start_urls = [
        'https://www.americangolf.co.uk/'
    ]

    color_requests_t = 'https://www.americangolf.co.uk/on/demandware.store/Sites-AmericanGolf-GB-Site' \
                       '/en_GB/Product-Variation'


class ParseSpider(BaseParseSpider):
    price_css = '[itemprop="price"]::attr(content), .mrrp .value ::text'
    care_css = '.careguide-section ::text'
    description_css = '.intro-paragraph ::text'
    raw_brand_css = 'script:contains(ecommerce)'
    brand_re = 'brand\"\:\"(.+?)\",'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': []
        }

        if '/golf-clubs/' in response.url:
            response.meta['garment'] = garment
            return self.parse_club_sku(response)

        requests = self.color_requests(response, product_id)
        garment['meta'] = {
            'requests_queue': requests
        }

        return self.next_request_or_garment(garment)

    def parse_club_sku(self, response):
        garment = response.meta['garment']
        seen_requests = set(garment['meta'].get('seen', []))

        variations_css = '#va-hand,#va-setoptions,#va-shafttype,#va-flex,#va-bounce,#va-loft'
        requests, variations = self.variation_requests(response, variations_css)
        requests_queue = [request for request in requests if request.url not in seen_requests]
        seen_requests.update([request.url for request in requests_queue])

        cart_css = '#add-to-cart ::attr(disabled)'
        if not bool(clean(response.css(cart_css).get(''))):
            sku = self.product_pricing_common(response)

            if not sku['currency']:
                currency_css = '[itemprop="priceCurrency"]::text'
                sku['currency'] = clean(response.css(currency_css))[0]

            sku['size'] = '_'.join([variation for variation in variations])
            sku_key = sku['size'].replace(' ', '')
            garment['skus'].update({sku_key: sku})

        requests_queue.extend(garment['meta']['requests_queue'])
        garment['meta'] = {
            'requests_queue': requests_queue,
            'seen': seen_requests
        }

        return self.next_request_or_garment(garment)

    def variation_requests(self, response, variations_css):
        variations = []
        variation_sels = response.css('.product-content-ctr').css(variations_css)

        for dropdown_sel in variation_sels.css('select'):
            selected_value = clean(dropdown_sel.css('[selected]::text'))
            if selected_value:
                variations.append(selected_value[0])

        variation_urls = clean(variation_sels.css('::attr(value)'))
        return [response.follow(url, callback=self.parse_club_sku) for url in variation_urls
                if url not in response.url], variations

    def parse_sku(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        color = clean(response.css('.selected-variant::text'))

        if color:
            common_sku['colour'] = color[0]

        if not common_sku['currency']:
            currency_css = '[itemprop="priceCurrency"]::text'
            common_sku['currency'] = clean(response.css(currency_css))[0]

        sizes = clean(response.css('.swatchanchor-inner ::text'))
        for size in sizes or self.spider_one_sizes:
            sku = common_sku.copy()
            sku['size'] = size
            sku_key = f'{sku["colour"]}_{sku["size"]}' if sku.get('colour') else f'{sku["size"]}'
            skus[sku_key] = sku

        return skus

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.parse_sku(response))
        return self.next_request_or_garment(garment)

    def color_requests(self, response, product_id):
        colors_css = '.attribute:nth-child(1) .swatches a::attr(data-variationvalue)'
        request = []

        for color in clean(response.css(colors_css)):
            args = {
                'pid': product_id,
                f'dwvar_{product_id}_variantimage': color,
                'source': 'detail',
                'format': 'ajax'
            }

            request_url = add_or_replace_parameters(self.color_requests_t, args)
            request.append(response.follow(request_url, callback=self.parse_color))

        return request

    def product_id(self, response):
        return clean(response.css('[itemprop="productID"]::text'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name::text'))[0]

    def product_category(self, response):
        raw_category_css = 'script:contains(ecommerce)'
        regex = 'category\"\:\"(.+?)\",'
        return response.css(raw_category_css).re_first(regex).split('/')

    def image_urls(self, response):
        images_css = '.carousel .carousel-tile a:not(.dialoglink)::attr(href)'
        return clean(response.css(images_css), '#')

    def product_gender(self, response):
        soup = clean(response.css('script:contains(ecomm_gender) ::text'))[0]
        return self.gender_lookup(soup) or Gender.ADULTS.value


class CrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.category-level-1-li', '[rel="next"]',
        '.header-navigation-left .li-level-1',
    ]
    product_css = [
        '.product-name a'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, tags=['link', 'a']), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


class ParseSpiderDE(MixinUK, ParseSpider):
    name = MixinUK.retailer + '-parse'


class CrawlSpiderDE(MixinUK, CrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ParseSpiderDE()
