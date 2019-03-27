import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from schwab_crawler.items import SchwabCrawlerItem


class SchwabCrawler(CrawlSpider):

    GENDER_MAP = {
        'dam': 'men',
        'men': 'men',
        'boy': 'boy',
        'girl': 'girl',
        'jungen': 'boy',
        'herren': 'men',
        'herr': 'women',
        'women': 'women',
        'damen': 'women',
        'mädchen': 'girl',
        'kid': 'unisex-kids',
        'barn': 'unisex-kids',
        'kinder': 'unisex-kids',
    }

    name = 'schwab-de-crawl'
    allowed_domains = ['schwab.de']
    start_urls = ['https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true']

    product_colour_url_t = 'https://www.schwab.de/index.php?varselid%5B1%5D={}&cl=oxwarticledetails&anid={}'

    products_css = ['div.c-productlist.c-productlist--4.at-product-list .product__top > a']
    rules = (Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),)

    def parse_start_url(self, response):
        yield Request(url=response.url, callback=self.parse_category)

    def parse_category(self, response):
        return [Request(url=url['url'], callback=self.parse_pagination)
                for urls in json.loads(response.text) for url in urls['sCat']]

    def parse_pagination(self, response):
        raw_pages = response.css('.paging__info ::text').extract()

        if raw_pages:
            return [Request(url=add_or_replace_parameter(response.url, 'pageNr', page), callback=self.parse)
                    for page in range(1, int(re.search('(\d+)', raw_pages[2]).group(1) or 1))]

    def parse_product(self, response):
        item = SchwabCrawlerItem()

        item['skus'] = {}
        item['lang'] = 'de'
        item['market'] = 'DE'
        item['url'] = self.product_url(response)
        item['name'] = self.product_name(response)
        item['care'] = self.product_care(response)
        item['brand'] = self.product_brand(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['image_urls'] = self.product_image_urls(response)
        item['description'] = self.product_description(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['meta'] = {'requests_queue': self.colour_requests(response, item)}

        return self.next_request_or_item(item)

    def product_url(self, response):
        return response.url

    def product_category(self, response):
        css = '[itemprop="name"]::text'
        return [response.css(css).extract()[3]]

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        item.pop('meta')
        return item

    def product_brand(self, response):
        css = '.details__brand > meta ::attr(content)'
        return response.css(css).extract_first() or 'schwab'

    def product_name(self, response):
        css = '.at-dv-itemNameBox .at-dv-itemName ::text'
        return self.clean(response.css(css).extract_first())

    def product_description(self, response):
        css = '.details__variation__hightlights ul > li ::text'
        return response.css(css).extract() or []

    def product_retailer_sku(self, response):
        css = 'script:contains("kalrequest.articlesString") ::text'
        return self.clean(response.css(css).re_first('ProductID=(\d*)'))

    def product_image_urls(self, response):
        css = '#magic > img ::attr(data-src)'
        return ['https:'+str(i) for i in response.css(css).extract()]

    def raw_sku(self, response):
        css = 'script:contains("kalrequest.articlesString") ::text'
        return response.css(css).re_first('kalrequest.articlesString(\\(.+?),')

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\t)*(\n)*[\s]', '', i) for i in raw_text]
        return re.sub('(\t)*(\n)*[\s]', '', raw_text)

    def product_gender(self, response):
        gender_soup = ' '.join([self.product_name(response)] +
                               self.product_description(response) +
                               self.product_category(response)).lower()

        for gender_str, gender in self.GENDER_MAP.items():
            if gender_str in gender_soup:
                return gender

        return 'unisex-adults'

    def product_pricing(self, response):
        price_css = '.pricing__norm--new.at-lastprice > span ::text'
        prev_price_css = '.pricing__norm--wrong > span ::text'
        currency_css = '.availability > meta ::attr(content)'

        pricing = {'price': response.css(price_css).extract_first()}
        pricing['currency'] = response.css(currency_css).extract()[1]
        prev_price = response.css(prev_price_css).extract_first()

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def product_care(self, response):
        css = '.details__desc__more__content.js-details-desc-more-content .js-tooltip-content ::text'
        return [self.clean(i) for i in response.css(css).extract()] or []

    def colour_requests(self, response, item):
        size_css_1 = '#variants div.l-outsp-bot-5 > button ::text'
        size_css_2 = '#variants .variants > .at-dv-size-option ::text'
        colour_css = '.c-colorspots.colorspots--inlist > a ::attr(title)'
        versel_id_css = '.c-colorspots.colorspots--inlist > a ::attr(data-varselid)'

        sizes = response.css(size_css_1).extract()
        colours = response.css(colour_css).extract()
        varsel_ids = response.css(versel_id_css).extract()
        raw_sku = [i.split('|') for i in self.raw_sku(response).split(';')]

        if not sizes:
            sizes = response.css(size_css_2).extract()

        if colours and sizes:
            return [Request(callback=self.parse_skus, meta={'colour': colour, 'item': item},
                            url=self.product_colour_url_t.format(varselid, f'{self.product_retailer_sku(response)}-'
                            f'{raw_sku[id][1]}-{raw_sku[id][3]}-{raw_sku[id][2]}')) for id, varselid, colour in
                            zip(range(0, len(raw_sku), len(sizes)), varsel_ids, colours)]

        return self.parse_skus(response, item)

    def parse_skus(self, response, item=None):
        skus = {}
        size_css_1 = '#variants .l-outsp-bot-5 > button'
        size_css_2 = '#variants .variants > .at-dv-size-option'

        selector = response.css(size_css_1)
        sku_id = self.product_retailer_sku(response)

        if not selector:
            selector = response.css(size_css_2)

        for size_s in selector:
            size = self.clean(size_s.css(' ::text').extract_first())
            sku = self.product_pricing(response)
            sku['size'] = size

            if not item:
                sku['colour'] = self.clean(response.meta['colour'])
                size += f'_{sku["colour"]}'

            if size_s.css(' ::attr(disabled)'):
                sku['out_of_stock'] = True

            skus[f'{sku_id}_{size}'] = sku

        if not item:
            item = response.meta['item']
            item['skus'].update(skus)
            return self.next_request_or_item(item)

        return item['skus'].update(skus)
