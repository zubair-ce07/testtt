from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from ..items import IntersportItem


class IntersportSpider(CrawlSpider):
    name = 'intersport_spider'
    start_urls = ['http://www.intersport.fr/']
    allowed_domains = ['intersport.fr', 'media.intersport.fr']

    visited_items = set()

    GENDER_MAP = {'femme': 'women', 'homme': 'men', 'enfant': 'unisex-kids', 'garcon': 'boy', 'fille': 'girl'}
    LANG = 'fr'
    CURRENCY = 'EUR'
    BASE_URL = "http://www.intersport.fr"
    IMAGE_REQUEST_URL = "http://media.intersport.fr/is/image/intersportfr/{retailer_id}_IS?req=set"
    IMAGE_BASE_URL = "http://media.intersport.fr/is/image/{img_url}?$produit_l$"

    rules = [Rule(LinkExtractor(restrict_css='.responsive-menu'), callback='parse'),
             Rule(LinkExtractor(restrict_css='.products-list', deny='text='), callback='parse_item'), ]

    def parse(self, response):
        yield from super(IntersportSpider, self).parse(response)
        next_url_css = ".pagination-next a::attr(href)"
        next_url = response.css(next_url_css).extract_first()
        if next_url:
            yield Request(next_url, callback=self.parse)

    def parse_item(self, response):
        retailer_sku = self.item_retailer_sku(response)
        if self.is_visited(retailer_sku):
            return
        item = IntersportItem()
        product_name = self.item_product_name(response)
        item['lang'] = self.LANG
        item['brand'] = self.item_brand(response)
        item['care'] = self.item_care(response)
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['name'] = product_name
        item['gender'] = self.item_gender(product_name)
        item['retailer_sku'] = retailer_sku
        item['url'] = response.url
        item['skus'] = self.item_skus(response, retailer_sku)
        color_urls = response.css(".colors-slider .product-image a::attr(name)").extract()

        image_requests = self.item_image_requests(color_urls, item)
        color_urls = [c_url for c_url in color_urls if c_url not in response.url]
        color_requests = self.item_color_request(color_urls, item, response)

        item['request_queue'] = color_requests + image_requests
        yield self.next_request_or_item(item)

    def next_request_or_item(self, item):
        request_queue = item.get('request_queue')
        if request_queue:
            request = request_queue.pop()
            request.meta['item'] = item
            return request
        else:
            del item['request_queue']
            return item

    def item_color_request(self, color_urls, item, response):
        color_request = []
        for url in color_urls:
            color_request.append(Request(response.urljoin(url), callback=self.parse_item_skus, ))
        return color_request

    def item_image_requests(self, color_urls, item):
        img_requests = []
        for c_url in color_urls:
            color_id = c_url[:-1].split('-')[-1]
            url = self.IMAGE_REQUEST_URL.format(retailer_id=color_id.replace("~", "_"))
            img_requests.append(Request(url, callback=self.parse_item_image_urls, ))
        return img_requests

    def parse_item_skus(self, response):
        item = response.meta['item']
        item_skus = item.get('skus', {})
        retailer_id = self.item_retailer_sku(response)
        item_skus.update(self.item_skus(response, retailer_id))
        item['skus'] = item_skus
        yield self.next_request_or_item(item)

    def parse_item_image_urls(self, response):
        item = response.meta['item']
        image_urls = item.get('image_urls', [])
        item['image_urls'] = self.item_image_urls(response, image_urls)
        yield self.next_request_or_item(item)

    def is_visited(self, retailer_sku):
        if retailer_sku in self.visited_items:
            return True
        self.visited_items.add(retailer_sku)
        return False

    def item_retailer_sku(self, response):
        item_id = response.css('.ref-produit::text').extract_first()
        return item_id.split("Ref ")[1]

    def item_product_name(self, response):
        return response.css("a[class=link] h1::text").extract_first()

    def item_care(self, response):
        item_care = response.css(".body-panel .small-12::text").extract()
        return [c.strip() for c in item_care if c.strip()]

    def item_category(self, response):
        return response.css(".breadcrumbs a::text").extract()[1:-1]

    def item_description(self, response):
        description = response.css(".body-panel p::text").extract()
        return [d.strip() for d in description if d.strip()]

    def item_gender(self, product_name):
        for gender_str, gender in self.GENDER_MAP.items():
            if gender_str in product_name.lower():
                return gender
        return 'unisex-adults'

    def item_brand(self, response):
        return response.css("a[class=link] a::text").extract_first()

    def item_price(self, response):
        dollars = response.css('.prix-produit div::text').extract()
        dollars = [p.strip() for p in dollars if p.strip()]
        cents = response.css('.prix-produit sup::text').extract()
        curreny_sign = cents[0][0]
        cents = [c[1:].strip() for c in cents]
        prices = [int(p + c) for p, c in list(zip(dollars, cents))]
        prices.sort()
        return [curreny_sign, prices]

    def item_sizes(self, response):
        sizes = {}
        size_selector = response.css(".tailles-produit button")
        for s_size in size_selector:
            out_of_stock = False
            size = s_size.css("::text").extract_first().strip()
            if s_size.css('button[disabled]'):
                out_of_stock = True
            sizes[size] = out_of_stock
        return sizes

    def item_skus(self, response, retailer_id):
        skus = {}
        colour = response.css('.ref-produit::text').extract_first()[-3:]
        for size, out_of_stock in self.item_sizes(response).items():
            sku = {}
            sku['size'] = size
            sku['colour'] = colour
            curreny_sign, prices = self.item_price(response)
            if curreny_sign == '€':
                sku['currency'] = self.CURRENCY
            sku['price'] = prices[0]
            if len(prices) > 1:
                sku['previous_prices'] = prices[1]
            if out_of_stock is True:
                sku['out_of_stock'] = out_of_stock
            sku_id = (colour + size).replace(" ", "")
            skus[sku_id] = sku
        return skus

    def item_image_urls(self, response, image_urls):
        url_list = response.css('i::attr(n)').extract()
        image_urls.extend([self.IMAGE_BASE_URL.format(img_url=url) for url in url_list])
        return image_urls
