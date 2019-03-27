import json
import re

from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from carhartt_crawler.items import CarharttCrawlerItem


class HollisterCrawler(CrawlSpider):

    name = 'carhartt-gb-crawl'
    allowed_domains = ['carhartt.com', 'scene7.com']
    start_urls = ['https://www.carhartt.com/gb/en-gb/']

    listings_css = ['.central-nav > ul a']
    products_css = ['#product-grid > div > div > div > div a']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product')
    )

    product_image_url_t = 'https://s7d9.scene7.com/is/image/{}?fit=constrain,1&wid=64&hei=64&fmt=jpg&qlt=60'
    product_colour_url_t = 'https://www.carhartt.com/DefiningAttributesDesktopView?selectedAttribute=_{}&' \
                           'langId=104&storeId={}&productId={}'

    formdata = {
        'langId': 104,
        'contentBeginIndex': 0,
        'requesttype': 'ajax',
    }

    def parse_pagination(self, response):
        page_size = 12
        yield Request(url=response.url, callback=self.parse)
        products = response.css('#custom-product-count ::text').extract_first()

        if products:
            formdata = self.formdata.copy()
            formdata['storeId'] = url_query_parameter(response.url, "storeId")
            formdata['catalogId'] = url_query_parameter(response.url, "catalogId")

            for _, page in enumerate(range(0, int(products), page_size)):
                formdata['beginIndex'], formdata['productBeginIndex'] = page, page
                yield Request(url=add_or_replace_parameter(response.url, 'resultsPerPage', page_size),
                              method='POST', body=json.dumps(formdata), callback=self.parse)

    def parse_product(self, response):
        item = CarharttCrawlerItem()

        item['skus'] = {}
        item['lang'] = 'en'
        item['market'] = 'GB'
        item['brand'] = 'carhartt'
        item['url'] = self.product_url(response)
        item['care'] = self.product_care(response)
        item['name'] = self.product_name(response)
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
        css = '#breadcrumbs .small-12 a ::text'
        return [response.css(css).extract()[1]]

    def product_name(self, response):
        css = '.title-top.t5 ::text'
        return response.css(css).extract_first()

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        item.pop('meta')
        return item

    def raw_product(self, response):
        css = '#product-details ::attr(data-inventory-url)'
        return {i.split('=')[0]: i.split('=')[1] for i in
                response.css(css).extract_first().split('&')}

    def product_description(self, response):
        return response.css('#desc li ::text').extract() or []

    def product_gender(self, response):
        css = '#panel2-1 .bronze-text ::text'
        return response.css(css).extract_first().split(' ')[0]

    def product_care(self, response):
        return response.css('#panel2-3 li ::text').extract() or []

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\r*)(\t*)(\n*)', '', i) for i in raw_text]
        return re.sub('(\r*)(\t*)(\n*)', '', raw_text)

    def product_image_urls(self, response):
        css = '#pdp-s7-media-viewer-container ::attr(data-default-media-set)'
        return [self.product_image_url_t.format(i.split(';;')[0]) for i in
                response.css(css).extract_first().split(',')]

    def product_retailer_sku(self, response):
        sku_r = re.compile(r'\d+')
        css = '#product-details ::attr(data-inventory-url)'
        return sku_r.findall(response.css(css).extract_first().split('&')[3])[0]

    def product_pricing(self, response):
        css = '#currencySelectionHidden ::attr(value)'
        pricing = {'currency': response.css(css).extract_first()}
        prev_price = response.css('.price.t16.not-bold del ::text').extract_first()
        pricing['price'] = response.css('.price.t16.not-bold span ::text').extract_first()

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def colour_requests(self, response, item):
        raw_product = self.raw_product(response)
        colours = response.css('.pdpRedesign a ::attr(title)').extract()
        colour_ids = response.css('.pdpRedesign a ::attr(data-attr-val-id)').extract()

        if colour_ids and colours:
            return [Request(callback=self.parse_skus,
                            meta={'colour': colour, 'item': item, 'product': response},
                            url=self.product_colour_url_t.format(colour_id, raw_product['storeId'],
                            raw_product['productId'])) for colour_id, colour in zip(colour_ids, colours)]

    def parse_skus(self, response):
        skus = {}
        colour = response.meta['colour']
        common_sku = self.product_pricing(response.meta['product'])

        for size_s in Selector(text=response.text).css('li a '):
            sku = common_sku.copy()
            size = self.clean(size_s.css(' ::text').extract_first())
            sku['size'] = size or 'One Size'

            if colour:
                size = f'{colour}_{size}'
                sku['colour'] = colour

            if size_s.css('.unavailable'):
                sku['out_of_stock'] = True

            skus[size] = sku

        response.meta['item']['skus'].update(skus)
        return self.next_request_or_item(response.meta['item'])
