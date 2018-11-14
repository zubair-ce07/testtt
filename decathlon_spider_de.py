import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class MixinDE:
    market = 'DE'
    retailer = 'decath-lon-de'

    allowed_domains = ['www.decathlon.de']
    start_urls = [
        'https://www.decathlon.de',
    ]

    denied_r = [
        'alles-fur-den-hund', 'angelruten-rollen-angelsets', 'angelzubehor', 'ausrustung', 'badminton',
        'basketballe', 'batteries', 'battery', 'billard', 'binoculars', 'bogensport', 'bootszubehor', 'bottle',
        'boule', 'camera', 'city_roller-und-scooter', 'communication', 'compasses', 'darts', 'drachen',
        'elektronik', 'ersatzrollen', 'fahrrader', 'fahrradteile', 'fahrradzubehor', 'fitnessgerate',
        'equipment', 'gesundheit-pflege', 'golfschlager', 'golfschläger', 'gps', 'handballe', 'headphone',
        'helmet', 'insoles', 'kajak', 'karpfenangeln', 'laces', 'light', 'lighting', 'locks', 'massage',
        'mobile', 'monitors', 'monoculars', 'pedometers', 'pferdezubehor', 'prazisionsspiele-wurfspiele',
        'proteine', 'recording', 'reitzubehor', 'route', 'rugbyballe', 'schnursenkel', 'schwimmhilfen baby',
        'skateboard-longboard', 'snowboard', 'sporternahrung-getranke', 'stand-up-paddle-sup',
        'taschen-zubehör', 'tennis', 'tennis accessor', 'tennis racket', 'tischtennis', 'torch', 'track',
        'trophies', 'tyre', 'volleyballe', 'wartung-und-pflege', 'wasser_mannschaftssport', 'weather stations',
        'weigh', 'weitere', 'wellenreiten-sup', 'windsurfen-kitesurfen', 'zubehör herrenschuh'
    ]

    unwanted_items_re = re.compile('|'.join(denied_r), re.I)


class DEParseSpider(BaseParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'
    raw_description_css = '#conversion-zone > p ::text,.benefit ::text,.description:not(.description--hidden) ::text'

    def parse(self, response):
        pids = self.product_ids(response)
        for pid in pids:
            garment = self.new_unique_garment(pid)

            if not garment:
                return

            self.boilerplate_normal(garment, response)

            if self.is_unwanted_item(garment):
                return

            garment['gender'] = response.meta['gender']
            garment['skus'] = self.skus(response, pid, garment['name'])
            garment['image_urls'] = self.image_urls(response, pid)

            return garment

    def skus(self, response, retailer_sku, name):
        skus = {}

        money_css = '[property="product:original_price:currency"]::attr(content),' \
                    '#conversion-zone .crossed-price ::text'
        money_strs = clean(response.css(money_css))

        common_sku = {
            'colour': self.model_color(response, retailer_sku, name),
        }

        sizes_css = f'.sizes__wrapper[data-id="{retailer_sku}"] li.sizes__size[data-id]'
        sizes = response.css(sizes_css)
        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = clean(size.css('.sizes__info ::text'))[0]
            sku['stock_level'] = clean(size.css('.sizes__stock__info::text'))[0]

            money_strs += clean(size.xpath('./@data-price'))
            sku.update(self.product_pricing_common(response=size, money_strs=money_strs))

            if sku['stock_level'] == '0':
                sku['out_of_stock'] = True

            sku_id = clean(size.xpath('./@data-id'))[0]
            skus[sku_id] = sku

        return skus

    def is_unwanted_item(self, garment):
        soup = [garment['name']] + garment['category'] or []
        soup = ''.join(soup).lower()

        if self.unwanted_items_re.search(soup):
            self.logger.info('Dropping unwanted item %s' % garment['url'])
            return True

        return False

    def product_ids(self, response):
        return clean(response.css('.sizes__wrapper::attr(data-id)'))

    def image_urls(self, response, sku_id):
        images_css = f'.product-picture__slides--alt[data-model-id="{sku_id}"] ::attr(data-iesrc)'
        return clean(response.css(images_css))

    def product_brand(self, response):
        return clean(response.css('head+script::text').re_first('"brand": "(.*?)"') or '')

    def product_name(self, response):
        return clean(response.css('.product-title-right ::text'))[0]

    def product_category(self, response):
        category_css = '.breadcrumbs-mobile li:not(.home):not(.current) ::attr(title)'
        return clean(response.css(category_css))[1:]

    def model_color(self, response, retailer_sku, name):
        color_css = f'.model-selection[data-model-id="{retailer_sku}"]::attr(data-color)'
        color = clean(response.css(color_css) or response.css('.model-color::text'))
        return color[0] if color else self.detect_colour(name)


class DECrawlSpider(BaseCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = DEParseSpider()

    listings_css = '.cat-item,ul.pagination a[aria-label="Next"]'
    products_css = '#in-product-list article'

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css, allow='/c1-herren/'),
             callback='parse_and_add_men'),
        Rule(LinkExtractor(restrict_css=listings_css, allow='/c1-kinder/'),
             callback='parse_and_add_unisex_kids'),
        Rule(LinkExtractor(restrict_css=listings_css, allow='/c1-damen/'),
             callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=listings_css, allow='(accessoires|special)'),
             callback='parse_and_add_unisex_adults'),
    )

