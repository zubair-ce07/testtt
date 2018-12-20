import json

from scrapy.http import Request
from urllib.parse import urlencode, quote
from w3lib.url import url_query_parameter, add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'maxfashion'
    allowed_domains = ['maxfashion.com', '3hwowx4270-dsn.algolia.net']
    default_brand = 'MAX'
    category_url = 'https://3hwowx4270-dsn.algolia.net/1/indexes/*/queries?' \
                   'X-Algolia-API-Key=4c4f62629d66d4e9463ddb94b9217afb&' \
                   'X-Algolia-Application-Id=3HWOWX4270&' \
                   'X-Algolia-Agent=Algolia%20for%20vanilla%20JavaScript%202.9.7'
    listings_data = {
        "query": "*",
        "hitsPerPage": "50",
        "page": "0",
        "facets": "*",
        "query": "",
        "numericFilters": "price > 1",
        "getRankingInfo": "1",
        "attributesToHighlight": "null",
        "attributesToRetrieve": "url",
        "tagFilters": '[["max"]]'
    }


class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    lang = 'ar'
    start_url = 'https://www.maxfashion.com/ae/ar/search'


class MixinSA(Mixin):
    retailer = Mixin.retailer + '-sa'
    market = 'SA'
    lang = 'ar'
    start_url = 'https://www.maxfashion.com/sa/ar/search'


class MixinBH(Mixin):
    retailer = Mixin.retailer + '-bh'
    market = 'BH'
    lang = 'ar'
    start_url = 'https://www.maxfashion.com/bh/ar/search'


class MaxFashionParseSpider(BaseParseSpider):
    raw_description_css = '.holder .descr-text ::text'
    price_css = '#products-details-price-01 ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['trail'] = self.add_trail(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        if self.is_homeware(garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)

        return garment

    def product_id(self, response):
        css = '[name="baseProduct"]::attr(value)'
        return clean(response.css(css))[0]

    def product_name(self, response):
        css= '#product-details-name::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '.breadcrumb ::text'
        return clean(response.css(css))

    def product_gender(self, garment):
        trail = [text for text, _ in garment['trail']]
        soup = garment['category'] + [garment['name']] + trail + garment['description']

        return self.gender_lookup(soupify(soup)) or Gender.ADULTS.value

    def image_urls(self, response):
        css = '[media="(min-width:1367px)"]::attr(srcset)'
        return clean(response.css(css))

    def skus(self, response):
        skus = {}

        common_sku = self.product_pricing_common(response)

        colour_css = '[checked=\'checked\']::attr(data-product-color)'
        common_sku['colour'] = clean(response.css(colour_css))[0]

        raw_sizes_s = response.css('.set-size li') or [response]
        for raw_size_s in raw_sizes_s:
            sku = common_sku.copy()

            size = clean(raw_size_s.css('[id^="filter-form-label-size"]::text'))
            sku['size'] = size[0] if size else self.one_size

            stock_s = clean(raw_size_s.css('::attr(data-stock-status)'))
            if raw_size_s.css('[class="stock hide"]') or (stock_s and stock_s[0] == 'outOfStock'):
                sku['out_of_stock'] = True

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def is_homeware(self, garment):
        return any("home" in c.lower() for c in garment['category'][1:])


class MaxFashionCrawlSpider(BaseCrawlSpider, Mixin):
    def start_requests(self):
        categories = ['women', 'men', 'girls', 'boys', 'home', 'shoes-women','shoes-men', 'shoes-girls', 'shoes-boys']
        return [Request(url=add_or_replace_parameter(self.start_url, 'q', f'allCategories:{category}'),
                        callback=self.parse_listings)
                        for category in categories]

    def parse_listings(self, response):
        session_x = '//script[contains(., "SearchKey")]/text()'
        index_name = response.xpath(session_x).re_first('ProductIndex = \'(.*)\'')
        category = url_query_parameter(response.url, 'q').split(':')[-1]

        self.listings_data['facetFilters'] = f'["inStock:1","approvalStatus:1","allCategories:{category}"]'
        listings_form_data = {
            "requests" : [{
                "indexName" : index_name,
                "params" : urlencode(self.listings_data, quote_via=quote, safe='*')
        }]}

        return Request(url=self.category_url,
                       callback=self.parse_navigation,
                       body=json.dumps(listings_form_data),
                       method='POST',
                       meta={'category' : category})

    def parse_navigation(self, response):
        raw_urls = json.loads(response.text)
        for raw_url in raw_urls['results'][0]['hits']:
            path = raw_url['url'][next(iter(raw_url['url']))]['ar']
            yield Request(url=f'{self.start_url}/{path}', callback=self.parse_item)

        if raw_urls['results'][0]['page'] == 0:
            for page_no in range(1, raw_urls['results'][0]['nbPages'] + 1):
                category = response.meta['category']
                self.listings_data['facetFilters'] = f'["inStock:1","approvalStatus:1","allCategories:{category}"]'
                self.listings_data['page'] = str(page_no)
                listings_form_data = {
                    "requests": [{
                        "indexName": raw_urls['results'][0]["indexUsed"],
                        "params": urlencode(self.listings_data, quote_via=quote, safe='*')
                    }]}

                yield Request(url=self.category_url,
                               callback=self.parse_navigation,
                               body=json.dumps(listings_form_data),
                               method='POST',
                               meta={'category': category})


class MaxFashionAEParseSpider(MaxFashionParseSpider, MixinAE):
    name = MixinAE.retailer + '-parse'


class MaxFashionAECrawlSpider(MaxFashionCrawlSpider, MixinAE):
    name = MixinAE.retailer + '-crawl'
    parse_spider = MaxFashionAEParseSpider()


class MaxFashionSAParseSpider(MaxFashionParseSpider, MixinSA):
    name = MixinSA.retailer + '-parse'


class MaxFashionSACrawlSpider(MaxFashionCrawlSpider, MixinSA):
    name = MixinSA.retailer + '-crawl'
    parse_spider = MaxFashionSAParseSpider()


class MaxFashionBHParseSpider(MaxFashionParseSpider, MixinBH):
    name = MixinBH.retailer + '-parse'


class MaxFashionBHCrawlSpider(MaxFashionCrawlSpider, MixinBH):
    name = MixinBH.retailer + '-crawl'
    parse_spider = MaxFashionBHParseSpider()
