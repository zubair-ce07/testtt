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
        'Men': 'men',
        'boy': 'boy',
        'girl': 'girl',
        'herren': 'men',
        'herr': 'women',
        'jungen': 'boy',
        'women': 'women',
        'damen': 'women',
        'mädchen': 'girl',
        'kid': 'unisex-kids',
        'Kid': 'unisex-kids',
        'barn': 'unisex-kids',
        'kinder': 'unisex-kids',
    }

    name = 'schwab-de-crawl'
    allowed_domains = ['schwab.de']
    start_urls = ['https://www.schwab.de']

    products_css = ['div.c-productlist.c-productlist--4.at-product-list .product__top > a']
    rules = (Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),)

    def start_requests(self):
        url = 'https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true'
        yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        raw_urls = json.loads(response.text)

        for urls in raw_urls:
            for url in urls["sCat"]:
                yield Request(url=url['url'], callback=self.parse_pagination)

    def parse_pagination(self, response):
        raw_pages = response.css('.paging__info ::text').extract()
        yield Request(url=response.url, callback=self.parse)

        if raw_pages:
            pages = int(re.search('(\d+)', raw_pages[2]).group(1))

            if pages > 1:
                for page in range(2, pages):
                    next_url = add_or_replace_parameter(response.url, 'pageNr', page)
                    yield Request(url=next_url, callback=self.parse)

    def parse_product(self, response):
        item = SchwabCrawlerItem()

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
        item['meta'] = {'requests_queue': self.colour_requests(response)}
        item['skus'] = {}

        return self.next_request_or_item(item)

    def product_url(self, response):
        return response.url

    def product_category(self, response):
        css = '[itemprop="name"]::text'
        return response.css(css).extract()[3]

    def product_brand(self, response):
        css = '.details__brand > meta ::attr(content)'
        return response.css(css).extract_first()

    def product_name(self, response):
        css = '.at-dv-itemNameBox .at-dv-itemName ::text'
        return self.clean(response.css(css).extract_first())

    def product_description(self, response):
        css = '.details__variation__hightlights ul > li ::text'
        return response.css(css).extract()

    def product_retailer_sku(self, response):
        css = 'script:contains("kalrequest.articlesString") ::text'
        return response.css(css).re_first('ProductID=(\d*)')

    def product_image_urls(self, response):
        css = '#magic > img ::attr(data-src)'
        return ['https:'+str(i) for i in response.css(css).extract()]

    def raw_sku(self, response):
        css = 'script:contains("kalrequest.articlesString") ::text'
        return response.css(css).re_first('kalrequest.articlesString(\\(.+?),')

    def clean(self, raw_text):
        return raw_text.replace('\t', '').replace('\n', '').replace(' ', '')

    def product_gender(self, response):
        gender = 'unisex-adults'
        category_css = '[itemprop="name"]::text'

        categories = response.css(category_css).extract()
        descriptions = self.product_description(response)
        name = self.product_name(response)

        for key, value in self.GENDER_MAP.items():
            for description in descriptions:
                for category in categories:
                    if key in f'{name} {description} {category}':
                        return value

        return gender

    def product_pricing(self, response):
        price_css = '.availability > meta ::attr(content)'
        prev_price_css = '.pricing__norm--wrong > span ::text'

        price = response.css(price_css).extract()
        prev_price = response.css(prev_price_css).extract_first()

        pricing = {'price': price[0]}
        pricing['currency'] = price[1]
        prev_price = prev_price

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def product_care(self, response):
        css = '.details__desc__more__content.js-details-desc-more-content .js-tooltip-content ::text'
        return [self.clean(i) for i in response.css(css).extract()]

    def colour_requests(self, response):
        request_queue = []
        raw_sku = self.raw_sku(response)
        sku_id = self.product_retailer_sku(response)

        size_css_1 = '#variants div.l-outsp-bot-5 > button ::text'
        size_css_2 = '#variants .variants > .at-dv-size-option ::text'
        url = 'https://www.schwab.de/index.php?varselid%5B1%5D={}&cl=oxwarticledetails&anid={}'

        colours = response.css('.c-colorspots.colorspots--inlist > a ::attr(title)').extract()
        varselids = response.css('.c-colorspots.colorspots--inlist > a ::attr(data-varselid)').extract()

        raw_sku = [i.split('|') for i in raw_sku.split(';')]
        sizes = [self.clean(i) for i in response.css(size_css_1).extract()]

        if not sizes:
            sizes = response.css(size_css_2).extract()

        for id, varselid, colour in zip(range(0, len(raw_sku), len(sizes)), varselids, colours):
            colour_id = f'{sku_id}-{raw_sku[id][1]}-{raw_sku[id][3]}-{raw_sku[id][2]}'
            next_url = url.format(varselid, colour_id)
            request_queue.append(Request(url=next_url, callback=self.parse_skus,
                                         meta={'colour': colour, 'sku_id': sku_id}))

        return request_queue

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        item.pop('meta')
        return item

    def parse_skus(self, response):
        skus = {}
        item = response.meta['item']
        colour = response.meta['colour']
        sku_id = response.meta['sku_id']

        size_css_1 = '#variants div.l-outsp-bot-5 > button'
        size_css_2 = '#variants .variants > .at-dv-size-option'

        common_sku = self.product_pricing(response)

        if response.css(size_css_1):
            for size_s in response.css(size_css_1):
                size = self.clean(size_s.css(' ::text').extract_first())
                sku = common_sku.copy()
                sku['colour'] = colour

                if size_s.css(' ::attr(disabled)'):
                    sku['out_of_stock'] = True

                sku['size'] = size
                skus[f'{sku_id}_{colour}_{size}'] = sku
        else:
            for size_s in response.css(size_css_2):
                size = self.clean(size_s.css(' ::text').extract_first())
                sku = common_sku.copy()
                sku['colour'] = colour

                if size_s.css(' ::attr(disabled)'):
                    sku['out_of_stock'] = True

                sku['size'] = size
                skus[f'{sku_id}_{colour}_{size}'] = sku

        item['skus'].update(skus)
        return self.next_request_or_item(item)
