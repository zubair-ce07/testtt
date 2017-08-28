from product_item import Product
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class OrseySpider(CrawlSpider):
    name = 'orsay.com'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de', ]
    download_delay = 1

    rules = (
        Rule(LinkExtractor(deny=['specials.*\.html'], restrict_css=['span.widget.widget-category-link', 'ul#nav',
                                                                    'div.toolbar-top ul.pagination']), follow=True),
        Rule(LinkExtractor(restrict_css=['h2.product-name']), callback='parse_product'),
    )

    def parse_product(self, response):
        item = Product()
        item['brand'] = self.parse_brand(response)
        item['care'] = self.parse_care(response)
        item['category'] = self.parse_category(response)
        item['description'] = self.parse_description(response)
        item['gender'] = self.parse_gender(response)
        item['image_urls'] = []
        item['name'] = self.parse_name(response)
        item['skus'] = self.get_skus(response)
        item['retailer_sku'] = self.parse_retailer_sku(response)
        item['url'] = self.parse_url(response)
        item['url_original'] = self.parse_url(response)
        response.meta['item'] = item
        response.meta['next_color_urls'] = self.parse_urls_for_color(response)
        return self.parse_next_color_items(response)

    def parse_next_color_items(self, response):
        next_color_urls = response.meta['next_color_urls']
        item = response.meta['item']
        item['image_urls'] = self.update_image_urls(item['image_urls'], response)
        item['skus'] = self.update_color_field(item['skus'], response)
        if not next_color_urls:
            yield item
        else:
            next_color_page_url = next_color_urls.pop(0)
            request = Request(next_color_page_url, callback=self.parse_next_color_items, dont_filter=True)
            request.meta['item'] = item
            request.meta['next_color_urls'] = next_color_urls
            yield request

    def parse_brand(self, response):
        return "Orsay"

    def parse_care(self, response):
        return response.css('ul.caresymbols img::attr(src)').extract()

    def parse_category(self, response):
        return response.css('div.no-display input[name^=category_name]::attr(value)').extract_first()

    def parse_description(self, response):
        return self.remove_whitespace(response.css('p.description::text').extract())

    def parse_gender(self, response):
        return "women"

    def parse_image_urls(self, response):
        return response.css('a[data-zoom-id^=mainZoom]::attr(href)').extract_first()

    def parse_name(self, response):
        return response.css('h1.product-name::text').extract()

    def parse_retailer_sku(self, response):
        return response.css('p.sku::text').extract_first().split(':')[1].strip(' ')[:6]

    def parse_urls_for_color(self, response):
        return [x for x in response.css('ul.product-colors  a::attr(href)').extract() if x != '#']

    def check_if_out_of_stock(self, response):
        return response.css('script[type="application/ld+json"]::text').extract_first().find("OutOfStock")

    def parse_color(self, response):
        return response.css('div.no-display input[name^=color]::attr(value)').extract_first()

    def parse_currency(self, response):
        return "Euro"

    def parse_price(self, response):
        return response.css('div.product-view span.price::text').extract_first()

    def parse_item_key_number(self, response):
        return response.css('div.twelve.columns label[for^="sku"]+input::attr(value)').extract_first()

    def parse_available_sizes(self, response):
        return response.css('div.sizebox-wrapper li::text').extract()

    def get_available_sizes(self, response):
        sizes = []
        for size in self.parse_available_sizes(response):
            sizes.append(size.strip('\n').strip(' '))
        sizes_of_item = filter(None, sizes)
        return sizes_of_item

    def get_skus(self, response):
        skus = dict()
        key_part = self.parse_item_key_number(response)
        sizes_of_item = self.get_available_sizes(response)
        for size in sizes_of_item:
            item_characterstics = dict(
                colour=[],
                currency=self.parse_currency(response),
                price=self.parse_price(response)
            )
            if self.check_if_out_of_stock(response) > 0:
                item_characterstics['OutOfStock'] = "True"
            key = self.get_key(key_part, size)
            item_characterstics['size'] = size
            skus[key] = item_characterstics
        return skus

    def get_key(self, key_part, size):
        return "{0}_{1}".format(key_part, size)

    def parse_url(self, response):
        return response.url

    def update_color_field(self, skus, response):
        for value in skus.values():
            value['colour'].append(self.parse_color(response))
        return skus

    def update_image_urls(self, image_urls, response):
        image_urls.append(self.parse_image_urls(response))
        return image_urls

    def remove_whitespace(self, text):
        text = str(text).replace(" ", "")
        position = text.find("UnserTipp")
        text = text[position:]
        return text
