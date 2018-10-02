from scrapy import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'barneys-us'
    default_brand = 'BARNEYS'
    allowed_domains = ['www.barneys.com']
    start_urls = ['http://www.barneys.com/global/ajaxGlobalNav.jsp']
    colour_utl_t = 'https://www.barneys.com/browse/ajaxProductDetailDisplay.jsp'
    one_sizes = ['1 SZ']
    MERCH_INFO = ['pre-order', 'final sale']


class MixinCA(Mixin):
    retailer = 'barneys-ca'
    market = 'CA'
    cookies = 'CA-CAD'


class MixinCN(Mixin):
    retailer = 'barneys-cn'
    market = 'CN'
    cookies = 'CN-CNY'


class MixinJP(Mixin):
    retailer = 'barneys-jp'
    market = 'JP'
    cookies = 'JP-JPY'


class MixinSE(Mixin):
    retailer = 'barneys-se'
    market = 'SE'
    cookies = 'SE-SEK'


class MixinTR(Mixin):
    retailer = 'barneys-tr'
    market = 'TR'
    cookies = 'TR-TRY'


class MixinAE(Mixin):
    retailer = 'barneys-ae'
    market = 'AE'
    cookies = 'AE-AED'


class MixinEU(Mixin):
    retailer = 'barneys-eu'
    market = 'EU'
    cookies = 'NL-EUR'


class MixinRU(Mixin):
    retailer = 'barneys-ru'
    market = 'RU'
    cookies = 'RU-RUB'


class MixinAU(Mixin):
    retailer = 'barneys-au'
    market = 'AU'
    cookies = 'AU-AUD'


class MixinDK(Mixin):
    retailer = 'barneys-dk'
    market = 'DK'
    cookies = 'DK-DKK'


class MixinNO(Mixin):
    retailer = 'barneys-no'
    market = 'NO'
    cookies = 'NO-NOK'


class MixinKR(Mixin):
    retailer = 'barneys-kr'
    market = 'KR'
    cookies = 'KR-KRW'


class MixinHK(Mixin):
    retailer = 'barneys-hk'
    market = 'HK'
    cookies = 'HK-HKD'


class MixinBR(Mixin):
    retailer = 'barneys-br'
    market = 'BR'
    cookies = 'BR-BRL'


class MixinNL(MixinEU):
    retailer = 'barneys-nl'
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
        garment['gender'] = self.product_gender(response)

        if self.is_homeware(response):
            garment['gender'] = None
            garment['industry'] = 'homeware'

        garment['skus'] = self.parse_skus(response)
        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        colour = clean(response.css('.atg_store_colorPicker'))
        size = clean(response.css(self.size_css))

        if not colour and not size:
            return self.one_size_skus(response)

        elif size:
            return self.skus(response, self.currency(response))

        return {}

    def colour_requests(self, response):
        colour_requests = []
        currency = self.currency(response)
        colour_ids = clean(response.css('.atg_store_colorPicker .hidden-xs ::attr(data-productid)'))

        for c_id in colour_ids:
            form_data = {
                'productId': c_id,
                'picker': 'pickerColorSizeContainer.jsp',
                'isAjax': 'true',
            }
            colour_requests.append(FormRequest(url=self.colour_utl_t, dont_filter=True, method='POST',
                                               meta={'currency': currency}, formdata=form_data,
                                               callback=self.parse_colours))

        return colour_requests

    def parse_colours(self, response):
        garment = response.meta['garment']
        currency = response.meta['currency']
        size = clean(response.css(self.size_css))
        garment['image_urls'] += self.image_urls(response)

        if not size:
            garment['skus'].update(self.colour_skus(response))

        else:
            garment['skus'].update(self.skus(response, currency))

        return self.next_request_or_garment(garment)

    def one_size_skus(self, response):
        one_size_skus = {}
        sku = self.product_pricing_common(response)

        if self.is_stock_unavailable(response):
            sku['out_of_stock'] = True

        colour = response.css('[data-fpcolor]::attr(data-fpcolor)').extract()[0]

        if colour != 'NO COLOR':
            sku['colour'] = colour

        sku['size'] = self.one_size
        sku_id = response.css('[data-fpskuid]::attr(data-fpskuid)').extract()[0]
        one_size_skus[sku_id] = sku

        return one_size_skus

    def colour_skus(self, response):
        colour_skus = {}
        sku = self.product_pricing_common(response)
        colours = response.css('.atg_store_colorPicker .hidden-xs a')

        for colour_sel in colours:
            sku_id = clean(colour_sel.css('::attr(data-productid)'))[0]
            sku['colour'] = clean(colour_sel.css('::attr(title)'))[0]
            size = clean(colour_sel.css('::attr(data-sku-sizes)'))[0]
            sku['size'] = size if size not in self.one_sizes else self.one_size

            if self.is_stock_unavailable(response):
                sku['out_of_stock'] = True

            colour_skus[sku_id] = sku
        return colour_skus

    def skus(self, response, currency):
        skus = {}

        for sku_sel in response.css('.sizePicker'):
            sku_id = clean(sku_sel.css('::attr(data-skuid)'))[0]
            price = clean(sku_sel.css('::attr(data-list-price)'))[0]
            p_price = clean(sku_sel.css('::attr(data-sale-price)'))
            sku = self.product_pricing_common(None, money_strs=[price, p_price, currency])
            colour = clean(sku_sel.css('::attr(data-vendorcolor)'))[0]

            sku['colour'] = colour
            size = clean(sku_sel.css('::text'))[0]
            sku['size'] = size if size not in self.one_sizes else self.one_size
            is_sold_out = clean(sku_sel.css('::attr(data-availabilitystatus)'))[0]

            if is_sold_out != '1000':
                sku['out_of_stock'] = True

            skus[sku_id] = sku
        return skus

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

    def currency(self, response):
        return clean(response.css(self.price_css))[0].split(' ')[0]

    def merch_info(self, response):
        merch_info_css = '#atg_behavior_addItemToCart::attr(value), .final-sale ::text'
        merch_info = clean(response.css(merch_info_css))
        soup = ' '.join(merch_info).lower()
        return [m for m in self.MERCH_INFO if m in soup]

    def is_stock_unavailable(self, response):
        stock_msg = clean(response.css('#atg_behavior_addItemToCart::attr(value)'))[0]
        return stock_msg != 'add to bag'


class BarneysCrawlSpider(BaseCrawlSpider):

    def start_requests(self):
        return [Request(url=self.start_urls[0], cookies={'usr_currency': self.cookies})]

    listing_css = [
        '.topnav-level-2',
        '#atg_store_pagination',
        '.pagination-link'
    ]

    deny_r = ['/toys-gifts/']

    products_css = '.name-link'

    rules = (Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r), callback='parse'),
             Rule(LinkExtractor(restrict_css=products_css, deny=deny_r), callback='parse_item'))


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
