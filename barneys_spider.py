import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'barneys'
    allowed_domains = ['barneys.com']
    start_urls = ['https://www.barneys.com/global/ajaxGlobalNav.jsp',
                  'https://www.barneyswarehouse.com/global/ajaxGlobalNav.jsp']


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'


class BarneysParseSpider(BaseParseSpider):
    brand_css = "span[itemprop='brand']::attr(content)"
    care_css = '.pdpReadMore ::text'
    raw_description_css = '.pdpReadMore ::text'
    price_css = '.atg_store_productPrice ::text'

    colour_request_url = 'https://www.barneys.com/browse/ajaxProductDetailDisplay.jsp'
    colour_formdata = {
        'picker': 'pickerColorSizeContainer.jsp',
        'changeStyle': 'true',
        'isLandingPage': 'false',
        'isAjax': 'true'
    }

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def is_homeware(self, response):
        soup = ' '.join(self.product_category(response))
        return 'home' in soup.lower()

    def product_id(self, response):
        css = '.product-id::attr(value)'
        return clean(response.css(css))[0][:4]

    def product_name(self, response):
        css = '.title.hidden::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = "#pdp_breadcrumbs [itemprop='name']::text"
        return clean(response.css(css))

    def product_gender(self, response):
        css = '#pdp_breadcrumbs ::text'
        soup = ' '.join(clean(response.css(css)))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        css = '#atg_store_productCore img::attr(src)'
        return clean(response.css(css))

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = clean(response.xpath("//span[@id='add_item_cart_fp']/@data-fpcolor|@data"))[0]
        skus_s = response.css('.atg_store_sizePicker .selector a')

        for sku_s in skus_s or [response]:
            sku = common_sku.copy()
            sku['size'] = sku_s.css('::attr(data-sku-size)').extract_first() or self.one_size
            css = "::attr(data-availabilitystatus), [itemprop='availability']::attr(href)"
            stock_status = str(clean(sku_s.css(css))[0]).lower()

            if stock_status == '1000' or 'outofstock' in stock_status:
                sku['out_of_stock'] = True

            sku_id = f"{sku['colour']}_{sku['size']}"
            skus[sku_id] = sku

        return skus

    def colour_requests(self, response):
        css = '.selector.pdp-swatch-img.hidden-xs a.colorSwatch:not(.color-active)::attr(data-productid)'
        colour_ids = clean(response.css(css))

        requests = []
        formdata = self.colour_formdata.copy()

        for colour_id in colour_ids:
            formdata['productId'] = colour_id
            requests.append(scrapy.FormRequest(self.colour_request_url,
                                               formdata=formdata.copy(),
                                               callback=self.parse_colour))
        return requests


class BarneysCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '.sub_category.topnav-level-3',
        'clearfix pagination-section'
    ]
    product_css = [
        '.product-image'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse', process_request='add_cookies'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    ]

    def add_cookies(self, request):
        return request.replace(cookies={'usr_currency': 'SE-SEK'})


class BarneysUSParseSpider(MixinSE, BarneysParseSpider):
    name = MixinSE.retailer + '-parse'


class BarneysUSCrawlSpider(MixinSE, BarneysCrawlSpider):
    name = MixinSE.retailer + '-crawl'
    parse_spider = BarneysUSParseSpider()
