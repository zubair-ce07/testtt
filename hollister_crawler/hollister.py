import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from hollister_crawler.items import HollisterCrawlerItem


class HollisterCrawler(CrawlSpider):

    name = 'hollister-jp-crawl'
    allowed_domains = ['hollisterco.jp', 'scene7.com']
    start_urls = ['https://www.hollisterco.jp/en_JP/guys',
                  'https://www.hollisterco.jp/en_JP/girls',
                  'https://www.hollisterco.jp/en_JP/gilly-hicks']

    listings_css = ['#secondary #category-level-1', '.infinite-scroll-placeholder']
    products_css = [
        '.search-result-items.tiles-container.clearfix.lazyloading.hide-compare.ajax .producttitle.heading3']

    rules = (Rule(LinkExtractor(restrict_css=listings_css, tags=('a', 'div'),
                                attrs=('href', 'data-grid-url')), callback='parse'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def parse_product(self, response):
        item = HollisterCrawlerItem()
        raw_product = self.raw_product(response)

        item['url'] = self.product_url(response)
        item['name'] = self.product_name(response)
        item['care'] = self.product_care(response)
        item['brand'] = self.product_brand(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['lang'] = self.product_language(raw_product)
        item['market'] = self.product_market(raw_product)
        item['category'] = self.product_category(raw_product)
        item['description'] = self.product_description(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['meta'] = {'requests_queue': self.colour_requests(response)}
        item['image_urls'] = []
        item['skus'] = {}

        return self.next_request_or_item(item)

    def product_url(self, response):
        return response.url

    def product_brand(self, raw_product):
        return raw_product['brand']

    def parse_size(self, response):
        item = response.meta['item']
        item['skus'].update(self.skus(response))
        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        item.pop('meta')
        return item

    def product_language(self, raw_product):
        return raw_product['language']

    def product_market(self, raw_product):
        return raw_product['country']

    def product_gender(self, raw_product):
        return raw_product['pagePathObj'][0]['name']

    def product_name(self, response):
        css = '.product-content.clearfix .product-name ::text'
        return self.clean(response.css(css).extract_first())

    def clean(self, raw_text):
        return raw_text.replace('\n', '').replace('\t', '')

    def product_category(self, raw_product):
        category = raw_product['pagePathObj'][0]['name']
        sub_category = raw_product['pagePathObj'][1]['name']
        return [category, sub_category]

    def product_description(self, response):
        css = '.product-sub-description ::text'
        return self.clean(response.css(css).extract_first())

    def product_retailer_sku(self, response):
        css = 'script:contains("modifiedLongSKU") ::text'
        return response.css(css).re_first('modifiedLongSKU"="(\d*-\d*-\d*-\d*)",')

    def extract_colour_parameter(self, response):
        return response.url.split('//')[-1].split('/')[-1].split('?')[1].split('=')[0]

    def product_care(self, response):
        return response.css('.product-details-bullet-list > li::text').extract()

    def raw_product(self, response):
        css = 'script:contains("pageObjectMapString") ::text'
        raw_product = response.css(css).re_first("pageObjectMapString = '(.*)';")
        return json.loads(raw_product.replace('=', ':'))

    def parse_image_urls(self, response):
        item = response.meta['item']
        img_url_t = 'https://anf.scene7.com/is/image/{}?$dwHCO-productThumbnail-v1$'
        img_ids = re.findall('"s":{"n":"(.*?)"}', response.text)
        for img_id in img_ids:
            item['image_urls'].append(img_url_t.format(img_id))
        return self.next_request_or_item(item)

    def colour_requests(self, response):
        request_queue = []
        css = '.attribute .swatches.color .list-item ::attr(title)'
        colours = response.css(css).extract()
        colour_parameter = self.extract_colour_parameter(response)

        for index, colour in enumerate(colours):
            if index != 0:
                index = '0' + str(index)
            next_url = add_or_replace_parameter(response.url, colour_parameter, index)
            request_queue.append(Request(url=next_url, callback=self.parse_colour,
                                         meta={'colour': colour}, dont_filter=True))
        return request_queue

    def product_pricing(self, response):
        pricing = {}
        prices_css = '.product-price.clearfix meta ::attr(content)'
        prices_and_currency = response.css(prices_css).extract()

        if prices_and_currency:
            if len(prices_and_currency) <= 2:
                pricing['price'] = prices_and_currency[0]
                pricing['currency'] = prices_and_currency[1]
            else:
                pricing['previous_price'] = prices_and_currency[0]
                pricing['currency'] = prices_and_currency[1]
                pricing['price'] = prices_and_currency[-2]
        return pricing

    def parse_colour(self, response):
        item = response.meta['item']
        colour = response.meta['colour']
        requests = item['meta']['requests_queue']
        url_css = 'ul.product__sizes > li:nth-child(1) > div.value > ul > li span'

        img_url_css = 'div.pdp-accordion-slider > div > div > input[type="hidden"] ::attr(value)'
        img_url = response.css(img_url_css).extract_first()
        if img_url:
            requests.append(Request(
                url=img_url, callback=self.parse_image_urls, dont_filter=True))

        for size_url_s in response.css(url_css):
            url = size_url_s.css('span::attr(data-href)').extract_first()
            size = size_url_s.css('span::text').extract_first()
            if url:
                requests.append(Request(url=url, callback=self.parse_size, dont_filter=True,
                                        meta={'colour': colour, 'size': self.clean(size)}))
        return self.next_request_or_item(item)

    def skus(self, response):
        skus = {}
        colour = response.meta['colour']
        size = response.meta['size']
        common_sku = self.product_pricing(response)
        common_sku['colour'] = colour

        lengths_css = 'ul.product__sizes > li:nth-child(2) > div.value > ul > li span'

        if size != 'ONE_SIZE':
            if response.css(lengths_css):
                for length_s in response.css(lengths_css):
                    lenght = self.clean(length_s.css('span ::text').extract_first())
                    sku = common_sku.copy()
                    sku['size'] = size

                    if length_s.css('.unselectable'):
                        sku['out_of_stock'] = True

                    skus[f'{colour}_{size}/{lenght}'] = sku
            else:
                sku = common_sku.copy()
                sku['size'] = size
                skus[f'{colour}_{size}'] = sku
        else:
            sku = common_sku.copy()
            sku['size'] = size
            skus[f'{colour}_ONE_SIZE'] = sku
        return skus
