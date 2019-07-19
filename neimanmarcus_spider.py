import json
from urllib.parse import urljoin

from scrapy import Request, FormRequest, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import url_query_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'neimanmarcus'
    default_brand = 'NeimanMarcus'
    allowed_domains = ['neimanmarcus.com']


class MixinTW(Mixin):
    retailer = Mixin.retailer + '-tw'
    market = 'TW'
    lang = 'en'
    homeware = 'homeware'

    pagination_url = 'https://www.neimanmarcus.com/en-tw/category.service?instart_disable_injection=true'
    region_payload = '%7B%22currencyPreference%22%3A%22TWD%22%2C%22countryPreference%22%3A%22TW%22%2C%22securityStatus' \
                     '%22%3A%22Anonymous%22%2C%22cartItemCount%22%3A0%7D'

    start_urls = ['https://www.neimanmarcus.com/en-tw/index.jsp']


class NeimanMarcusParseSpider(BaseParseSpider):
    sku_url = 'https://www.neimanmarcus.com/en-tw/product.service?instart_disable_injection=true'
    img_url_t = 'http://neimanmarcus.scene7.com/is/image/NeimanMarcus/{}?&wid=1200&height=1500'
    sku_payload_t = '{{"ProductSizeAndColor":{{"productIds":"{}"}}}}'

    raw_description_css = '.productCutline ::text'
    price_css = '.product-price ::text, .item-price ::text'

    def parse(self, response):
        response.meta['products_response'] = response
        yield self.products_request(response)

    def parse_products(self, response):
        raw_products = self.raw_products(response)
        response = response.meta['products_response']
        products_s = response.css('.hero-zoom-frame')

        for product_s, raw_skus in zip(products_s, raw_products):
            garment = self.new_unique_garment(self.product_id(product_s))

            if not garment:
                continue

            self.boilerplate(garment, response)

            garment['name'] = self.product_name(product_s)
            garment['brand'] = self.product_brand(product_s)
            garment['image_urls'] = self.image_urls(product_s)
            garment['care'] = self.product_care(product_s)
            garment['description'] = self.product_description(product_s)
            garment['category']  = self.product_category(garment)
            garment['skus'] = self.skus(product_s, raw_skus)

            if self.is_apparel(garment):
                garment['gender'] = self.product_gender(garment)
            else:
                garment['industry'] = self.homeware

            return garment

    def product_id(self, product_s):
        return clean(product_s.css('.product-images ::attr("prod-id")'))[0]

    def product_name(self, product_s):
        return clean(product_s.css('.product-name span::text'))[0]

    def image_urls(self, product_s):
        image_urls = clean(product_s.css('.product-images ::attr(data-zoom-url)'))
        image_urls = [urljoin(self.start_urls[0], image_url) for image_url in image_urls]

        raw_colour_codes = clean(product_s.css('#color-pickers ::attr(data-sku-img)'))
        raw_colour_codes = [json.loads(rc_codes).values() for rc_codes in raw_colour_codes]

        colour_codes = [c_code for rc_codes in raw_colour_codes for c_code in rc_codes]

        return image_urls + [self.img_url_t.format(cc) for cc in colour_codes]

    def product_category(self, garment):
        return clean([category for category, _ in garment.get('trail', [])])

    def product_gender(self, garment):
        trail = soupify([f'{category} {url}' for category, url in garment.get('trail') or []]).lower()
        return self.gender_lookup(trail) or self.gender_lookup(soupify(garment['description'])) or Gender.ADULTS.value

    def skus(self, product_s, raw_skus):
        skus = {}
        common_sku = self.product_pricing_common(product_s)

        for raw_sku in raw_skus['skus']:
            sku = common_sku.copy()
            colour = raw_sku.get('color')

            if colour:
                sku['colour'] = colour.split('?')[0]

            sku['size'] = raw_sku.get('size') or self.one_size
            skus[f'{sku["size"]}-{sku["colour"]}' if colour else sku['size']] = sku

        return skus

    def is_apparel(self, garment):
        trail = soupify([f'{category} {url}' for category, url in garment.get('trail') or []]).lower()
        return 'men' in trail and 'home' not in trail

    def raw_products(self, response):
        products = json.loads(response.text)
        return json.loads(products['ProductSizeAndColor']['productSizeAndColorJSON'])

    def products_request(self, response):
        formdata = {'data': self.payload(response)}
        return FormRequest(url=self.sku_url, formdata=formdata, meta=response.meta.copy(), callback=self.parse_products)

    def payload(self, response):
        raw_product = json.loads(response.css('script:contains("window.utag_data")::text').re_first('({.*})'))
        product_ids = soupify(raw_product['product_id'], ',')
        payload = self.sku_payload_t.format(product_ids)

        return payload


class NeimanMarcusCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.silo-nav [href*=men]',
        '.silo-nav [href*=boys]',
        '.silo-nav [href*=girls]',
        '.silo-nav [href*=baby]',
        '.silo-nav [href*=home]',
        '.silo-nav [href*=contemporary]',
        '.silo-nav [href*=shoes]',
        '.silo-nav [href*=handbags]',
        '.silo-nav [href*=jewelry]',
    ]
    products_css = ['#productTemplateId']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def start_requests(self):
        cookie = {'profile_data': self.region_payload}
        yield Request(url=self.start_urls[0], cookies=cookie, callback=self.parse)

    def parse(self, response):
        yield from super().parse(response)
        yield from self.pagination_requests(response)


    def pagination_requests(self, response):

        pagination_formdata = {
            'service': 'getCategoryGrid',
            'sid': 'getCategoryGrid'
        }


        nav_path = url_query_parameter(response.url, 'navpath')

        category_url = clean(response.css('[rel="canonical"]::attr(href)'))
        category_id = category_url[0].split('-')[-1]

        total_pages = clean(response.css('#epagingTop .pageOffset ::attr(pagenum)'))

        if not nav_path or not category_url or not total_pages:
            return []

        payload = '{{"GenericSearchReq":{{"pageOffset":{},"pageSize":"30","refinements":"",' \
            f'"selectedRecentSize":"","activeFavoriteSizesCount":"0","activeInteraction":"true",' \
            f'"mobile":false,"sort":"SELLABLE_DATE|1","endecaDrivenSiloRefinements":"navpath={nav_path}",' \
            f'"definitionPath":"/nm/commerce/pagedef_rwd/template/EndecaDrivenHome",' \
            f'"userConstrainedResults":"true","updateFilter":"false","rwd":"true",' \
            f'"categoryId":"{category_id}","sortByFavorites":false,"isFeaturedSort":false,"prevSort":""}}}}}}}}'

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for page_no in range(1, int(total_pages[-1])):
            formdata = pagination_formdata.copy()
            formdata['data'] = payload.format(page_no)

            yield FormRequest(url=self.pagination_url, formdata=formdata, meta=meta.copy(), callback=self.products_requests)


    def products_requests(self, response):
        raw_category = json.loads(response.text)
        raw_products = Selector(text=raw_category['GenericSearchResp']['productResults'])

        urls = clean(raw_products.css('#productTemplateId ::attr(href)'))
        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        return [response.follow(url=url, callback=self.parse_item, meta=meta.copy()) for url in urls]


class NeimanMarcusTWParseSpider(MixinTW, NeimanMarcusParseSpider):
    name = MixinTW.retailer + '-parse'


class NeimanMarcusTWCrawlSpider(MixinTW, NeimanMarcusCrawlSpider):
    name = MixinTW.retailer + '-crawl'
    parse_spider = NeimanMarcusTWParseSpider()
