from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, Gender, soupify, clean


class MixinUS:
    retailer = 'tennis-warehouse-us'
    market = 'US'
    default_brand = 'Tennis Warehouse'
    image_url_t = 'https://img2.tennis-warehouse.com/watermark/rs.php?path={0}-{1}-{2}.jpg'
    allowed_domains = ['tennis-warehouse.com']
    start_urls = ['https://www.tennis-warehouse.com/equipment.html']


class ParseSpider(BaseParseSpider, MixinUS):
    raw_description_css = 'div[itemprop="description"] *::text'
    price_css = '.product_pricing *::text'
    brand_css = 'meta[itemprop="brand"]::attr(content)'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["gender"] = self.product_gender(garment)
        garment["skus"] = self.skus(response)
        garment["image_urls"] = self.image_urls(response, garment)

        if not garment["skus"]:
            garment["out_of_stock"] = True

        return garment

    def product_id(self, response):
        return response.css('.wishlist_poplink::attr(data-code)').extract_first()

    def product_name(self, response):
        return response.css('.product_header h1::text').extract_first()

    def image_urls(self, response, garment):
        total_images = len(response.css('.multiview a.changeview').extract())
        product_id = garment["retailer_sku"]
        product_colors = response.meta["color_codes"]
        image_urls = []

        for color in product_colors:
            image_urls.extend([self.image_url_t.format(product_id, color, image_no)
                               for image_no in range(1, total_images + 1)])

        return image_urls or response.css('.multiview img::attr(src)').re('(.+)&')

    def product_category(self, response):
        return clean([t for t, _ in response.meta.get("trail") if t != '' or []])

    def product_gender(self, garment):
        soup = [garment["name"], garment["url"]] + garment["category"]
        return self.gender_lookup(soupify(soup)) or Gender.ADULTS.value

    def skus(self, response):
        raw_skus = response.css('.styled_subproduct_list tr')
        skus = {}
        response.meta["color_codes"] = set()

        for raw_sku in raw_skus:
            sku = self.product_pricing_common(response)

            size = raw_sku.css('li:contains(Size) span.styleitem::text').extract_first()

            sku["colour"] = self.extract_color(raw_sku, response)
            sku["size"] = clean(size) if size else self.one_size

            sku_id = f'{sku["colour"]}_{size}'
            skus[sku_id] = sku

            code = raw_sku.css('li:contains(Colo) .styleitem::attr(data-scode)').extract_first()
            if code:
                response.meta["color_codes"].add(code)

        return skus

    def extract_color(self, raw_sku, response):
        color_code = raw_sku.css('.stocknum::text').extract_first()
        color_code = color_code.split('-')[-1] if color_code else None

        multi_color_css = '[itemprop="description"] li:contains(Colo)::text'
        color_css = f'[itemprop="description"] li:contains(Colo) li:contains("{color_code}")::text'
        color_css = color_css if color_code else multi_color_css

        color_names = response.css(color_css).extract()
        color = clean(color_names)[0] if clean(color_names) else None

        code = raw_sku.css('li:contains(Colo) .styleitem::attr(data-scode)').extract_first()

        return color or code or self.detect_colour_from_name(response)


class CrawlSpider(BaseCrawlSpider, MixinUS):
    listings_xpath = [
        '//div[text()="Apparel"]/following-sibling::ul[1]',
        '//a[text()="Junior Shoes"]',
        '//a[text()="Tennis Bags"]'
    ]

    listings_css = [
        '.lnav_col_header',
        '.appwrap',
        'div[class*="_featured_brands"]',
        'div[class*="_brandlist"]'
    ]

    product_css = ['.cat_border_table .name', 'div.cat_list .name']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, restrict_xpaths=listings_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


class TennisWarehouseUSParseSpider(ParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class TennisWarehouseUSCrawlSpider(CrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = TennisWarehouseUSParseSpider()
