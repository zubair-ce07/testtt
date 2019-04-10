import re
import json

from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from carhartt_crawler.items import CarharttCrawlerItem


class CarharttCrawler(CrawlSpider):

    formdata = {
        'langId': 104,
        'contentBeginIndex': 0,
        'requesttype': 'ajax',
    }

    name = 'carhartt-gb-crawl'
    products_css = ['#product-grid']
    listings_css = ['.central-nav > ul a']
    allowed_domains = ['carhartt.com', 'scene7.com']
    start_urls = ['https://www.carhartt.com/gb/en-gb/']

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
        )

    image_url_t = 'https://s7d9.scene7.com/is/image/{}?fit=constrain,1&wid=64&hei=64&fmt=jpg&qlt=60'
    colour_url_t = 'https://www.carhartt.com/DefiningAttributesDesktopView?selectedAttribute=_{}&' \
                   'langId=104&storeId={}&productId={}'

    def parse_pagination(self, response):
        page_size = 24
        products = response.css('#custom-product-count ::text').extract_first()

        if not products:
            return

        formdata = self.formdata.copy()
        formdata['storeId'] = url_query_parameter(response.url, 'storeId')
        formdata['catalogId'] = url_query_parameter(response.url, 'catalogId')

        for page in range(0, int(products), page_size):
            formdata['beginIndex'], formdata['productBeginIndex'] = page, page
            yield Request(callback=self.parse, body=json.dumps(formdata), method='POST',
                  url=add_or_replace_parameter(response.url, 'resultsPerPage', page_size))

    def parse_product(self, response):
        item = CarharttCrawlerItem()

        item['skus'] = {}
        item['lang'] = 'en'
        item['market'] = 'GB'
        item['brand'] = 'carhartt'
        item['url'] = response.url
        item['care'] = self.product_care(response)
        item['name'] = self.product_name(response)
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

    def product_description(self, response):
        return response.css('#desc li ::text').extract()

    def product_care(self, response):
        return response.css('#panel2-3 li ::text').extract()

    def product_gender(self, response):
        css = '#panel2-1 .bronze-text ::text'
        return response.css(css).extract_first().split(' ')[0]

    def parse_colour(self, response):
        response.meta['item']['skus'].update(self.skus(response))
        return self.next_request_or_item(response.meta['item'])

    def product_category(self, response):
        return response.css('#breadcrumbs a ::text').extract()[1:]

    def product_name(self, response):
        return response.css('.title-top.t5 ::text').extract_first()

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\r*)(\t*)(\n*)', '', i) for i in raw_text]
        return re.sub('(\r*)(\t*)(\n*)', '', raw_text)

    def product_image_urls(self, response):
        css = '#pdp-s7-media-viewer-container ::attr(data-default-media-set)'
        return [self.image_url_t.format(i.split(';;')[0]) for i in
                response.css(css).extract_first().split(',')]

    def product_id(self, response):
        css = '#product-details ::attr(data-inventory-url)'
        return response.css(css).extract_first().split('&')[3].split('=')[-1]

    def skus(self, response):
        skus = {}
        colour = response.meta.get('colour')
        common_sku = response.meta['pricing']

        for size_s in Selector(text=response.text).css('li a '):
            size = self.clean(size_s.css(' ::text').extract_first())
            sku = common_sku.copy()
            sku['colour'] = colour
            sku['size'] = size or 'One Size'

            if size_s.css('.unavailable'):
                sku['out_of_stock'] = True

            skus[f'{colour}_{size}'] = sku

        return skus

    def product_pricing(self, response):
        prev_price = response.css('.price.t16.not-bold del ::text').extract_first()
        pricing = {'price': response.css('.price.t16.not-bold span ::text').extract_first()}
        pricing['currency'] = response.css('#currencySelectionHidden ::attr(value)').extract_first()

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def colour_requests(self, response, item):
        pricing = self.product_pricing(response)
        css = '#product-details ::attr(data-inventory-url)'
        colours = response.css('.pdpRedesign a ::attr(title)').extract()
        colour_ids = response.css('.pdpRedesign a ::attr(data-attr-val-id)').extract()
        raw_product = {i.split('=')[0]: i.split('=')[1] for i in response.css(css).extract_first().split('&')}

        if colour_ids and colours:
            return [Request(url=self.colour_url_t.format(colour_id, raw_product['storeId'], raw_product['productId']),
                    callback=self.parse_colour, meta={'colour': colour, 'item': item, 'pricing': pricing})
                    for colour_id, colour in zip(colour_ids, colours)]
