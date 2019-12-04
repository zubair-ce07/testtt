import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider, Request

from ..items import Product


class ProductParser(Spider):
    seen_ids = set()
    name = 'ugg_spider'

    def parse(self, response):
        retailer_sku_id = self.product_retailer_sku(response)
        product_price = self.product_price(response)
        if retailer_sku_id in self.seen_ids or not product_price:
            return

        self.seen_ids.add(retailer_sku_id)
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        item = Product()
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['brand'] = 'UGG'
        item['url'] = response.url
        item['market'] = 'AU'
        item['retailer'] = 'UGG-AU'
        item['name'] = self.product_name(response)
        item['description'] = self.product_description(response)
        item['images_url'] = self.product_images(response)
        item['skus'] = self.product_sku(response)
        item['meta'] = {'requests': self.product_sku_requests(response, item)}

        return self.next_item_or_request(item)

    def next_item_or_request(self, item):
        if item['meta']['requests']:
            request = item['meta']['requests'].pop()
            yield request
        else:
            item.pop('meta')
            yield item

    def product_retailer_sku(self, response):
        sku_data = self.raw_product(response)
        return sku_data.get('displayCode')

    def product_name(self, response):
        return response.css('.product-name::text').get()

    def product_gender(self, response):
        gender = response.css('.product-spec-list dd::text').get()
        return gender if gender else 'unisex'

    def product_category(self, response):
        css = '.breadcrumb-item a::attr(data-id)'
        return response.css(css).getall()[1:]

    def product_description(self, response):
        css = '.product-detail-card .card-text::text'
        raw_description = response.css(css).get()
        return raw_description.strip()

    def product_price(self, response):
        prices = {}
        prices['price'] = response.css('.prices .value::attr(content)').get()
        prices['currency'] = response.css('.prices [itemprop="priceCurrency"]::attr(content)').get()
        prices['previous_prices'] = response.css('.prices .strike-through span::attr(content)').getall()
        return prices

    def product_sku_requests(self, response, item):
        requests = []
        css = '.color-value:not(.selected)::attr(data-attr-value)'
        product_sku_variants = response.css(css).getall()
        product_id = self.product_id(response)

        for color_variant in product_sku_variants:
            url = response.urljoin(f'{product_id}{color_variant}.html')
            requests.append(
                Request(url=url, callback=self.add_product_skus, meta={'item': item})
            )
        return requests

    def product_id(self, response):
        raw_data = response.css('[type="application/ld+json"]::text').get()
        raw_data = json.loads(raw_data)
        return raw_data.get('itemReviewed').get('@id')

    def add_product_skus(self, response):
        item = response.meta['item']
        item['images_url'] += self.product_images(response)
        item['skus'] += self.product_sku(response)
        return self.next_item_or_request(item)

    def product_images(self, response):
        raw_images = response.css('.product-detail-img::attr(data-json)').get()
        raw_images_content = json.loads(raw_images)
        large_sized_images = raw_images_content.get('large')
        return [img_item.get('url') for img_item in large_sized_images]

    def product_sku(self, response):
        skus = []
        sku_data = self.raw_product(response)
        product_sizes = self.product_sizes(response)

        common_sku = self.product_price(response)
        for product_size in product_sizes:
            sku = common_sku.copy()
            sku['colour'] = sku_data.get('displayValue'),
            sku['size'] = product_size,
            sku['sku_id'] = self.product_retailer_sku(response)
            skus.append(sku)

        return skus

    def raw_product(self, response):
        raw_data = response.css('.render-product-selected::attr(data-json)').get()
        return json.loads(raw_data)

    def product_sizes(self, response):
        css = '.select-size option:not([disabled])::text'
        raw_sizes = response.css(css).getall()[1:]
        return self.clean(raw_sizes)

    def clean(self, raw_text):
        clean_text = []
        for text_item in raw_text:
            clean_item = text_item.strip()
            if clean_item:
                clean_text.append(clean_item)
        return clean_text


class UggCrawler(CrawlSpider):
    name = 'ugg_crawler'
    product_parser = ProductParser()

    allowed_domains = ['au.ugg.com']
    start_urls = ['https://au.ugg.com']
    allow = r'/catalog/'
    listing_css = ('.btn-show-all',)
    cookies = {'NM()sdf': '905077ed-6e1f-27a1-1c38-95b01189b480;'}
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'DOWNLOAD_DELAY': '5'
    }

    rules = (
        Rule(LinkExtractor(allow=allow, restrict_css=listing_css), callback='parse_listing'),
    )

    def start_requests(self):
        yield Request(self.start_urls[0], cookies=self.cookies)

    def parse_listing(self, response):
        product_requests = response.css('.card-img a::attr(href)').getall()
        meta = {'trail': [response.url]}
        yield from [Request(url=response.urljoin(url), cookies=self.cookies, callback=self.product_parser.parse,
                            meta=meta) for url in product_requests]

        next_page_url = response.css('.show-more button::attr(data-url)').get()
        if not next_page_url:
            return
        yield Request(url=response.urljoin(next_page_url), cookies=self.cookies, callback=self.parse_listing)
