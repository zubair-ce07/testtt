import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from boss_crawler.items import BossCrawlerItem


class BossSpider(CrawlSpider):

    name = 'boss-uk-crawl'
    allowed_domains = ['hugoboss.com']
    start_urls = ['https://www.hugoboss.com/uk/']

    listings_css = ['.nav-list.nav-list--first-level']
    products_css = ['.search-result-content.search-result-content--sticky.is-category-search']

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def parse_pagination(self, response):
        page_size = 60
        css = '.search-result-options__brand-badge::text'
        pages = response.css(css).extract_first()
        pages = int(pages) if pages else 0

        for page in range(0, pages+1, page_size):
            next_url = add_or_replace_parameter(response.url, 'sz=60&start', page)
            yield Request(url=next_url, callback=self.parse)

    def parse_product(self, response):
        item = BossCrawlerItem()
        raw_product = self.raw_product(response)

        item['skus'] = {}
        item['lang'] = 'en'
        item['market'] = 'UK'
        item['gender'] = 'women'
        item['url'] = self.product_url(response)
        item['care'] = self.product_care(response)
        item['name'] = self.product_name(raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['category'] = self.product_category(raw_product)
        item['image_urls'] = self.product_images_urls(response)
        item['description'] = self.product_description(response)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)
        item['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_item(item)

    def parse_colour(self, response):
        item = response.meta['item']
        colour = response.meta['colour']
        item['skus'].update(self.skus(response, colour))
        return self.next_request_or_item(item)

    def skus(self, response, colour):
        skus = {}
        sizes_css = '.product-stage__choose-size--container a'

        for size_s in response.css(sizes_css):
            size = size_s.css('a::attr(title)').extract_first()
            sku = {'colour': colour}

            if size_s.css('a::attr(disabled)'):
                sku['out_of_stock'] = True

            sku['price'] = self.product_pricing(response)
            sku['currency'] = self.product_currency(response)
            sku['size'] = size
            skus[f'{colour}_{size}'] = sku
        return skus

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        item.pop('meta')
        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['name']

    def product_brand(self, raw_product):
        return raw_product['brand']

    def product_category(self, raw_product):
        return raw_product['category']

    def product_retailer_sku(self, raw_product):
        return raw_product['sku']

    def product_care(self, response):
        css = '.accordion__care-icon__text::text'
        return response.css(css).extract()

    def product_currency(self, response):
        css = '.product-price meta::attr(content)'
        return response.css(css).extract_first()

    def product_images_urls(self, response):
        css = '.slider-item--thumbnail-image img::attr(src)'
        return response.css(css).extract()

    def product_description(self, response):
        css = '.product-container__text__description::text'
        description = response.css(css).extract_first()
        return description.replace('\t', '').replace('\n', '')

    def raw_product(self, response):
        css = 'script:contains("dataLayer.push(") ::text'
        raw_product = response.css(css).re_first('\{.ecommerce.*\}')
        raw_product = json.loads(raw_product)
        return raw_product['ecommerce']['detail']['products'][0]

    def product_pricing(self, response):
        prev_price_css = '.product-price.product-price--price-standard::text'
        price_css = '.product-price.product-price--price-sales.product-price--price::text'
        prev_price = response.css(prev_price_css).extract_first()
        price = response.css(price_css).extract_first()

        if prev_price:
            prev_price = prev_price.strip('\n')
            if prev_price:
                return {'price': price.strip('\n'),
                        'previous_price': prev_price}

        return price.strip('\n')

    def colour_requests(self, response):
        urls_css = '.swatch-list__button.swatch-list__button--is-large a::attr(href)'
        colours_css = '.swatch-list__button.swatch-list__button--is-large a::attr(title)'
        urls = response.css(urls_css).extract()
        colours = response.css(colours_css).extract()
        return [Request(url=response.urljoin(u), callback=self.parse_colour,
                meta={'colour': c}, dont_filter=True) for c, u in zip(colours, urls)]
