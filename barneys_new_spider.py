from scrapy import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'barneys'
    default_brand = 'BARNEYS'

    allowed_domains = [
        'www.barneys.com',
        'www.barneyswarehouse.com'
    ]

    start_urls = [
        'http://www.barneys.com/global/ajaxGlobalNav.jsp',
        'https://www.barneyswarehouse.com/global/ajaxGlobalNav.jsp'
    ]

    colour_url = 'https://www.barneys.com/browse/ajaxProductDetailDisplay.jsp'
    outlet_url = 'https://www.barneyswarehouse.com/browse/ajaxProductDetailDisplay.jsp'

    one_sizes = ['1 sz']

    merch_map = [
        ('pre-order', 'Pre Order'),
        ('final sale', 'Final Sale'),
    ]


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    cookies = 'US-USD'


class MixinCA(Mixin):
    retailer = Mixin.retailer + '-ca'
    market = 'CA'
    cookies = 'CA-CAD'


class MixinCN(Mixin):
    retailer = Mixin.retailer + '-cn'
    market = 'CN'
    cookies = 'CN-CNY'


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    cookies = 'JP-JPY'


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'
    cookies = 'SE-SEK'


class MixinTR(Mixin):
    retailer = Mixin.retailer + '-tr'
    market = 'TR'
    cookies = 'TR-TRY'


class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    cookies = 'AE-AED'


class MixinEU(Mixin):
    retailer = Mixin.retailer + '-eu'
    market = 'EU'
    cookies = 'NL-EUR'


class MixinRU(Mixin):
    retailer = Mixin.retailer + '-ru'
    market = 'RU'
    cookies = 'RU-RUB'


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    cookies = 'AU-AUD'


class MixinDK(Mixin):
    retailer = Mixin.retailer + '-dk'
    market = 'DK'
    cookies = 'DK-DKK'


class MixinNO(Mixin):
    retailer = Mixin.retailer + '-no'
    market = 'NO'
    cookies = 'NO-NOK'


class MixinKR(Mixin):
    retailer = Mixin.retailer + '-kr'
    market = 'KR'
    cookies = 'KR-KRW'


class MixinHK(Mixin):
    retailer = Mixin.retailer + '-hk'
    market = 'HK'
    cookies = 'HK-HKD'


class MixinBR(Mixin):
    retailer = Mixin.retailer + '-br'
    market = 'BR'
    cookies = 'BR-BRL'


class MixinNL(MixinEU):
    retailer = Mixin.retailer + '-nl'
    market = 'NL'


class BarneysParseSpider(BaseParseSpider):
    raw_description_css = '.pdpReadMore .hidden-xs ::text'
    brand_css = '.prd-brand ::text'
    price_css = '.picker_price_attribute ::text'
    size_css = '.sizePicker'

    def parse(self, response):
        pid = self.product_id(response)
        
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if self.is_homeware(response):
            garment['industry'] = 'homeware'

        else:
            garment['gender'] = self.product_gender(response)

        if self.is_outlet(response):
            garment['outlet'] = True

        garment['merch_info'] = self.merch_info(response)
        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)

        sizes = response.css(self.size_css)
        colour_requests = self.colour_requests(response)
        
        if colour_requests and sizes:
            garment['meta'] = {'requests_queue': colour_requests}

        else:
            garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        colour_requests = []

        css = '.atg_store_colorPicker span.hidden-xs ::attr(data-productid)'
        colour_ids = clean(response.css(css))

        for c_id in colour_ids:
            form_data = {
                'productId': c_id,
                'picker': 'pickerColorSizeContainer.jsp',
                'isAjax': 'true',
            }

            url = self.outlet_url if 'barneyswarehouse' in response.url else self.colour_url
            colour_requests.append(FormRequest(url=url, formdata=form_data, callback=self.parse_colours))

        return colour_requests

    def parse_colours(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)

        skus_css = [
            self.size_css,
            'span.pdp-swatch-img a',
            '[data-fpcolor]'
        ]

        for sku_s in next((response.css(css) for css in skus_css if response.css(css)), []):
            sku = common_sku.copy()

            colour_css = '::attr(data-vendorcolor), ::attr(title), ::attr(data-fpcolor)'
            colour = clean(sku_s.css(colour_css))[0]
            if colour.lower() != 'no color':
                sku['colour'] = colour

            size = clean(sku_s.css('::text, ::attr(data-sku-sizes)') or [self.one_size])[0]
            sku['size'] = size = self.one_size if size.lower() in self.one_sizes else size

            is_sold_out = sku_s.css('.disabled-size, .outOfStockSwatch')
            if is_sold_out or self.is_stock_unavailable(response):
                sku['out_of_stock'] = True

            skus[f'{colour}_{size}'] = sku
        return skus

    def is_stock_unavailable(self, response):
        css = '#atg_behavior_addItemToCart::attr(value)'
        stock_msg = clean(response.css(css))[0]
        return stock_msg != 'add to bag'

    def product_id(self, response):
        return clean(response.css('input.productId::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-title::text'))[0]

    def product_category(self, response):
        return clean(response.css('[itemprop="item"] ::text'))

    def product_gender(self, response):
        categories = self.product_category(response)
        return self.gender_lookup(' '.join(categories)) or Gender.ADULTS.value

    def image_urls(self, response):
        return clean(response.css('[itemprop="image"]::attr(src)'))

    def is_homeware(self, response):
        return 'Home' in ' '.join(self.product_category(response))

    def merch_info(self, response):
        css = '#atg_behavior_addItemToCart::attr(value), .final-sale ::text'
        soup = ' '.join(clean(response.css(css))).lower()
        return [merch for merch_str, merch in self.merch_map if merch_str in soup]

    def is_outlet(self, response):
        return 'barneyswarehouse.com' in response.url


class BarneysCrawlSpider(BaseCrawlSpider):

    def start_requests(self):
        return [Request(url, cookies={'usr_currency': self.cookies}) for url in self.start_urls]

    listings_css = [
        '.topnav-level-2',
        '#atg_store_pagination',
        '.pagination-link'
    ]

    deny_r = ['/toys-gifts/']

    products_css = '.name-link'

    rules = (Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse'),
             Rule(LinkExtractor(restrict_css=products_css, deny=deny_r), callback='parse_item'))


class BarneysParseSpiderUS(BarneysParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class BarneysCrawlSpiderUS(BarneysCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = BarneysParseSpiderUS()


class BarneysParseSpiderCA(BarneysParseSpider, MixinCA):
    name = MixinCA.retailer + '-parse'


class BarneysCrawlSpiderCA(BarneysCrawlSpider, MixinCA):
    name = MixinCA.retailer + '-crawl'
    parse_spider = BarneysParseSpiderCA()


class BarneysParseSpiderCN(BarneysParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'


class BarneysCrawlSpiderCN(BarneysCrawlSpider, MixinCN):
    name = MixinCN.retailer + '-crawl'
    parse_spider = BarneysParseSpiderCN()


class BarneysParseSpiderJP(BarneysParseSpider, MixinJP):
    name = MixinJP.retailer + '-parse'


class BarneysCrawlSpiderJP(BarneysCrawlSpider, MixinJP):
    name = MixinJP.retailer + '-crawl'
    parse_spider = BarneysParseSpiderJP()


class BarneysParseSpiderSE(BarneysParseSpider, MixinSE):
    name = MixinSE.retailer + '-parse'


class BarneysCrawlSpiderSE(BarneysCrawlSpider, MixinSE):
    name = MixinSE.retailer + '-crawl'
    parse_spider = BarneysParseSpiderSE()


class BarneysParseSpiderTR(BarneysParseSpider, MixinTR):
    name = MixinTR.retailer + '-parse'


class BarneysCrawlSpiderTR(BarneysCrawlSpider, MixinTR):
    name = MixinTR.retailer + '-crawl'
    parse_spider = BarneysParseSpiderTR()


class BarneysParseSpiderAE(BarneysParseSpider, MixinAE):
    name = MixinAE.retailer + '-parse'


class BarneysCrawlSpiderAE(BarneysCrawlSpider, MixinAE):
    name = MixinAE.retailer + '-crawl'
    parse_spider = BarneysParseSpiderAE()


class BarneysParseSpiderRU(BarneysParseSpider, MixinRU):
    name = MixinRU.retailer + '-parse'


class BarneysCrawlSpiderRU(BarneysCrawlSpider, MixinRU):
    name = MixinRU.retailer + '-crawl'
    parse_spider = BarneysParseSpiderRU()


class BarneysParseSpiderAU(BarneysParseSpider, MixinAU):
    name = MixinAU.retailer + '-parse'


class BarneysCrawlSpiderAU(BarneysCrawlSpider, MixinAU):
    name = MixinAU.retailer + '-crawl'
    parse_spider = BarneysParseSpiderAU()


class BarneysParseSpiderDK(BarneysParseSpider, MixinDK):
    name = MixinDK.retailer + '-parse'


class BarneysCrawlSpiderDK(BarneysCrawlSpider, MixinDK):
    name = MixinDK.retailer + '-crawl'
    parse_spider = BarneysParseSpiderDK()


class BarneysParseSpiderNO(BarneysParseSpider, MixinNO):
    name = MixinNO.retailer + '-parse'


class BarneysCrawlSpiderNO(BarneysCrawlSpider, MixinNO):
    name = MixinNO.retailer + '-crawl'
    parse_spider = BarneysParseSpiderNO()


class BarneysParseSpiderKR(BarneysParseSpider, MixinKR):
    name = MixinKR.retailer + '-parse'


class BarneysCrawlSpiderKR(BarneysCrawlSpider, MixinKR):
    name = MixinKR.retailer + '-crawl'
    parse_spider = BarneysParseSpiderKR()


class BarneysParseSpiderHK(BarneysParseSpider, MixinHK):
    name = MixinHK.retailer + '-parse'


class BarneysCrawlSpiderHK(BarneysCrawlSpider, MixinHK):
    name = MixinHK.retailer + '-crawl'
    parse_spider = BarneysParseSpiderHK()


class BarneysParseSpiderBR(BarneysParseSpider, MixinBR):
    name = MixinBR.retailer + '-parse'


class BarneysCrawlSpiderBR(BarneysCrawlSpider, MixinBR):
    name = MixinBR.retailer + '-crawl'
    parse_spider = BarneysParseSpiderBR()


class BarneysParseSpiderNL(BarneysParseSpider, MixinNL):
    name = MixinNL.retailer + '-parse'


class BarneysCrawlSpiderNL(BarneysCrawlSpider, MixinNL):
    name = MixinNL.retailer + '-crawl'
    parse_spider = BarneysParseSpiderNL()


class BarneysParseSpiderEU(BarneysParseSpider, MixinEU):
    name = MixinEU.retailer + '-parse'


class BarneysCrawlSpiderEU(BarneysCrawlSpider, MixinEU):
    name = MixinEU.retailer + '-crawl'
    parse_spider = BarneysParseSpiderEU()
