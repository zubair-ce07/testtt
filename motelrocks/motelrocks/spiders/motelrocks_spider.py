import re

from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from ..items import MotelrocksItem


class MotelRocksSpider(CrawlSpider):
    name = 'motelrocks-uk'
    start_urls = ['http://www.motelrocks.com/']
    allowed_domains = ['motelrocks.com', ]

    visited_items = set()
    lang = 'en'
    currency = 'GBP'
    brand = 'Motel'
    page_size = 20
    pagination_url = 'http://www.motelrocks.com/categories_ajax.php'
    form_data = {'isajax': '1', 'invocation': 'page', 'pagesize': '20'}

    rules = [
        Rule(LinkExtractor(restrict_css='ul#nav-menu'), callback='parse'),
        Rule(LinkExtractor(restrict_css='div#CategoryContent .xProductDetails'), callback='parse_item'),
    ]

    def parse(self, response):
        yield from super(MotelRocksSpider, self).parse(response)
        item_count = response.css('.pagingcontent .paging-title ::text').re('(\d+)')
        if 'php' in response.url or not item_count:
            return
        page_count = int(item_count[0]) // self.page_size + 1
        cat_id = response.xpath('//script[contains(text(),"categoryid")]').re("categoryid:'(\d+)")[0]
        self.form_data['categoryid'] = cat_id
        for pg_no in range(2, page_count + 1):
            self.form_data['page'] = str(pg_no)
            yield FormRequest(self.pagination_url, method='POST', formdata=self.form_data, callback=self.parse)

    def parse_item(self, response):
        retailer_sku = self.item_retailer_sku(response)
        if self.is_visited(retailer_sku):
            return
        item = MotelrocksItem()
        item['lang'] = self.lang
        item['brand'] = self.brand
        item['care'] = []
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['name'] = self.item_product_name(response)
        item['gender'] = 'women'
        item['retailer_sku'] = retailer_sku
        item['url'] = response.url
        item['skus'] = self.item_skus(response)
        item['image_urls'] = self.item_image_urls(response)
        colour_urls = response.css(".colswatch:not([style*='{}'])::attr(href)".format(retailer_sku)).extract()
        yield item
        for url in colour_urls:
            yield Request(url, callback=self.parse)

    def is_visited(self, retailer_sku):
        if retailer_sku in self.visited_items:
            return True
        self.visited_items.add(retailer_sku)
        return False

    def item_image_urls(self, response):
        return response.css('div#thumbnails-mask img::attr(src)').extract()

    def clean(self, data_list_or_str):
        if isinstance(data_list_or_str, str):
            return data_list_or_str.strip()
        return [d.strip() for d in data_list_or_str if d.strip()]

    def item_retailer_sku(self, response):
        return response.xpath('//script[contains(text(),"productId")]').re('productId = (\d+);')[0]

    def item_product_name(self, response):
        return response.css('h1[itemprop="name"] ::text').extract_first()

    def item_category(self, response):
        return self.clean(response.css('.breadcrumbs ::text').extract())[:-1]

    def item_description(self, response):
        return self.clean(response.css('div#Details ::text').extract())

    def integer_price(self, prices):
        integer_prices = []
        for price in prices:
            price = ''.join(re.findall('\d+', price))
            if not price:
                continue
            integer_prices.append(int(price) * 100)
        integer_prices.sort()
        return integer_prices

    def item_price(self, response):
        prices = self.clean(response.css('div[itemprop="offerDetails"] ::text').extract())
        prices = self.integer_price(prices)
        return prices[0], prices[1:]

    def item_sizes(self, response):
        sizes = {}
        size_selector = response.css('.Value li')
        for s_size in size_selector:
            out_of_stock = False
            size = self.clean(s_size.css(" ::text").extract())[0]
            if s_size.css('::attr(instock)').extract_first() != "1":
                out_of_stock = True
            sizes[size] = out_of_stock
        return sizes

    def item_skus(self, response):
        skus = {}
        common = {}
        price, previous_prices = self.item_price(response)
        common['colour'] = self.item_retailer_sku(response).replace("58522", "")
        common['currency'] = self.currency
        common['price'] = price
        common['previous_prices'] = previous_prices
        for size, out_of_stock in self.item_sizes(response).items():
            sku = common.copy()
            sku['size'] = size
            if out_of_stock:
                sku['out_of_stock'] = out_of_stock
            skus["{}_{}".format(common['colour'], size)] = sku
        return skus
