from scrapy.spiders import Rule, Request

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, Gender


class Mixin:
    retailer = 'leejeans-au'
    market = 'AU'
    default_brand = 'Lee'

    allowed_domains = ['leejeans.com.au']
    start_urls = ['https://leejeans.com.au/']

    cookies = {
        'KP_UID': '9a350c5b5b22e3b4338ed42c7a6e3565',
        'TA.customer': '3a17fee6-217d-4452-b999-a35f1f0be574'
    }

    spider_gender_map = {
        'girls': Gender.WOMEN.value,
        'womens': Gender.WOMEN.value,
        'licks': Gender.WOMEN.value,
        '2': Gender.WOMEN.value,
        'guys': Gender.MEN.value,
        'mens': Gender.MEN.value,
        'z': Gender.MEN.value,
        'black': Gender.MEN.value,
        'new': Gender.MEN.value
    }


class LeeJeansParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    price_css = '.product-price ::text , .old-product-price ::text'
    raw_description_x = '//div[@class="product-description "]//text()'
    deny_care = ['Features', 'Product Specification', 'Care Instructions', 'Fabrication']

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)
        return garment

    def product_id(self, response):
        return clean(response.css('.picture-thumbs::attr(data-productid)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-title ::text'))[0]

    def image_urls(self, response):
        images_s = response.css('.cloudzoom-gallery::attr(data-cloudzoom)')
        return [image_s.re_first('image:(.*?jpg)') for image_s in images_s]

    def product_category(self, response):
        return clean([t[0] for t in response.meta.get('trail', [])])

    def product_gender(self, response):
        trail = response.meta['trail'][1][1]
        soup = trail.split('/')[4]
        return self.gender_lookup(soup.lower()) or Gender.ADULTS.value

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        colour = self.detect_colour_from_name(response)

        if colour:
            common_sku['colour'] = colour

        skus = {}
        for size_s in response.css('.size-list'):
            sku = common_sku.copy()
            sku['size'] = size = clean(size_s.css('li ::text'))[0]

            if size_s.css('[data-stock="0"]'):
                sku['out_of_stock'] = True

            size_type = size_s.css('.size-list + dl .fit-list')
            for size_type_s in size_type:
                sku_type = sku.copy()
                sku_type['size'] = f'{size}_{clean(size_type_s.css("li ::text"))[0]}'

                if size_type_s.css('[data-stock="0"]'):
                    sku_type['out_of_stock'] = True

                skus[f'{sku_type["size"]}_{colour}'] = sku_type

            if not size_type:
                skus[f'{sku["size"]}_{colour}'] = sku

        return skus


class LeaJeansCrawlSpider(Mixin, BaseCrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    name = Mixin.retailer + '-crawl'
    parse_spider = LeeJeansParseSpider()

    listings_css = [
        '.menu-wrapper'
    ]
    products_css = [
        '.product-title'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookies)

