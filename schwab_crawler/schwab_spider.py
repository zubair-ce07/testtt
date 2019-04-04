import re
import json

from scrapy.link import Link
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request

from schwab_crawler.items import SchwabCrawlerItem


class CategoryLE(LinkExtractor):

    def extract_links(self, response):
        try:
            raw_category = json.loads(response.text)
        except ValueError:
            return []
        if raw_category[0].get('sCat'):
            return [Link(url['url']) for urls in raw_category for url in urls['sCat']]
        return []


class PaginationLE(LinkExtractor):

    def extract_links(self, response):
        raw_pages = response.css('.paging__info ::text').extract()

        if not raw_pages:
            return []

        total_pages = int(re.search('(\d+)', raw_pages[2]).group(1) or 1)
        return [Link(url=add_or_replace_parameter(response.url, 'pageNr', page))
                for page in range(1, total_pages)]


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

    products_css = ['div.c-productlist.c-productlist--4.at-product-list .product__top > a']
    colour_url_t = 'https://www.schwab.de/index.php?varselid%5B1%5D={}&cl=oxwarticledetails&anid={}'

    rules = (
        Rule(CategoryLE(), callback='parse'),
        Rule(PaginationLE(), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
    )

    def parse_product(self, response):
        item = SchwabCrawlerItem()

        item['skus'] = {}
        item['lang'] = 'de'
        item['market'] = 'DE'
        item['url'] = response.url
        item['name'] = self.product_name(response)
        item['care'] = self.product_care(response)
        item['brand'] = self.product_brand(response)
        item['gender'] = self.product_gender(response)
        item['retailer_sku'] = self.product_id(response)
        item['category'] = self.product_category(response)
        item['image_urls'] = self.product_image_urls(response)
        item['description'] = self.product_description(response)
        item['meta'] = {'requests_queue': self.colour_requests(response, item)}

        return self.next_request_or_item(item)

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

    def parse_skus(self, response, item=None):
        if item:
            return item['skus'].update(self.skus(response, item))
        item = response.meta['item']
        item['skus'].update(self.skus(response))
        return self.next_request_or_item(item)

    def product_id(self, response):
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
        return re.sub('(\t)*(\n)*[\s]', '', raw_text) if raw_text else raw_text

    def product_gender(self, response):
        gender_soup = ' '.join([self.product_name(response)] + self.product_description(response) +
                               self.product_category(response)).lower()

        for gender_str, gender in self.GENDER_MAP.items():
            if gender_str in gender_soup:
                return gender

        return 'unisex-adults'

    def product_category(self, response):
        return response.css('[itemprop="itemListElement"] ::text').extract()[::2][1:]

    def product_care(self, response):
        css = '.details__desc__more__content.js-details-desc-more-content .js-tooltip-content ::text'
        return [self.clean(i) for i in response.css(css).extract()]

    def product_pricing(self, response):
        prev_price = response.css('.pricing__norm--wrong > span ::text').extract_first()
        pricing = {'currency': response.css('.availability > meta ::attr(content)').extract()[1]}
        pricing['price'] = response.css('.pricing__norm--new.at-lastprice > span ::text').extract_first()

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def colour_requests(self, response, item):
        colour_requests = []
        colour_css = '.c-colorspots.colorspots--inlist > a ::attr(title)'
        versel_ids_css = '.c-colorspots.colorspots--inlist > a ::attr(data-varselid)'
        size_css = '#variants .l-outsp-bot-5 > button ::text, #variants .variants > .at-dv-size-option ::text'

        colours = response.css(colour_css).extract()
        colour_ids = response.css(size_css).extract()
        varsel_ids = response.css(versel_ids_css).extract()
        colour_codes = [i.split('|') for i in self.raw_sku(response).split(';')]

        if not (colours and colour_ids):
            return self.parse_skus(response, item)

        for id, varsel_id, colour in zip(range(0, len(colour_codes), len(colour_ids)), varsel_ids, colours):
            colour_id = f'{self.product_id(response)}-{colour_codes[id][1]}-{colour_codes[id][3]}-{colour_codes[id][2]}'
            colour_requests.append(Request(url=self.colour_url_t.format(varsel_id, colour_id), callback=self.parse_skus,
                                           meta={'colour': colour, 'item': item}))
        return colour_requests

    def skus(self, response, item=None):
        skus = {}
        size_css = '#variants .l-outsp-bot-5 > button, #variants .variants > .at-dv-size-option'

        for size_s in response.css(size_css):
            sku = self.product_pricing(response)
            sku['size'] = self.clean(size_s.css(' ::text').extract_first())

            if size_s.css(' ::attr(disabled)'):
                sku['out_of_stock'] = True

            if item:
                skus[sku['size']] = sku
            else:
                sku['colour'] = self.clean(response.meta['colour'])
                skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus
