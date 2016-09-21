from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BlueflyItem
from itertools import product


class BlueflySpider(CrawlSpider):
    name = "bluefly"
    allowed_domains = ['bluefly.com']
    start_urls = ['http://www.bluefly.com/']
    rules = [Rule(LinkExtractor(allow=['/[A-Za-z]+\/index'], deny=['/beauty\/index']), process_links='link_filtering'
                  , follow=True),
             Rule(LinkExtractor(restrict_css='.mz-productlisting-title'),
                  callback='parse_bluefly_item', follow=True),
             Rule(LinkExtractor(restrict_css='.mz-pagenumbers-next'))]

    def link_filtering(self, links):
        for link in links:
            link.url = link.url.replace('/index', '?pageSize=96')
        return links

    def parse_bluefly_item(self, response):
        item = BlueflyItem()
        item['brand'] = self.parse_brand(response)
        item['category'] = self.parse_category(response)
        item['merch_info'] = self.parse_merch_info(response)
        item['url_original'] = response.url
        item['product_id'] = self.parse_product_id(response.url)
        item['image_urls'] = self.parse_image_urls(response)
        item['name'] = self.parse_name(response)
        item['description'] = self.parse_description(response)
        item['care'] = self.parse_care(response)
        item['gender'] = self.parse_gender(response)
        item['skus'] = self.parse_skus(response)
        return item

    def parse_skus(self, response):
        skus = {}
        if self.out_of_stock(response):
            skus['out_of_stock'] = True
        else:
            numeric_sizes = self.parse_numeric_sizes(response)
            colours = self.parse_colour(response)
            colours_size = len(colours)
            for size, colour in product(numeric_sizes, colours):
                skus[self.sku_key(size, colour, colours_size)] = self.parse_sku(response, size, colour)
        return skus

    def sku_key(self, numeric_size, colour, colour_size):
        return numeric_size if colour_size is 1 else "{}_{}".format(colour, numeric_size)

    def out_of_stock(self, response):
        return response.css(".waitlist")

    def parse_sku(self, response, numeric_size, color):
        sku = {}
        size = self.parse_size(response, numeric_size)
        sku['size'] = size
        sku['price'] = self.parse_price(response)
        sku['currency'] = 'USD'
        sku['previous_prices'] = self.parse_prev_prices(response)
        sku['colour'] = color
        return sku

    def parse_numeric_sizes(self, response):
        css = ".mz-productoptions-sizebox::attr(data-value)"
        return response.css(css).extract() or ['one_size']

    def parse_price(self, response):
        return response.css('div.mz-price::text').extract()[0].strip()

    def parse_size(self, response, data_value):
        size = response.css(".mz-productoptions-sizebox[data-value = '{}']::text".format(data_value))
        return size.extract()[0] if size else 'one_size'

    def parse_prev_prices(self, response):
        prev_prices = "".join(response.css(".mz-price.is-crossedout::text").extract())
        return [prev_prices.replace('Retail:', '').strip()] if prev_prices else ''

    def parse_colour(self, response):
        css1 = '.product-color-list > li > a::attr(title)'
        css2 = '.mz-productoptions-optionvalue::text'
        return response.css(css1).extract() or [response.css(css2).extract()[0]]

    def parse_product_id(self, url):
        return url.split("/")[-1]

    def parse_brand(self, response):
        return response.css('.mz-productbrand > a::text').extract()[0]

    def parse_description(self, response):
        return response.css('.mz-productdetail-description::text').extract() + self.parse_details(response)

    def parse_details(self, response):
        return response.css('.mz-productdetail-props > li::text').extract()

    def parse_care(self, response):
        return response.css('.mz-productdetail-props').xpath('li[contains(text(),"%")]/text()').extract()

    def parse_category(self, response):
        return response.css('.mz-breadcrumb-link:not(.is-first)::text').extract()

    def parse_merch_info(self, response):
        merch_info = response.css('.mz-price-message::text').extract()
        return merch_info[0].strip() if merch_info else ""

    def parse_image_urls(self, response):
        return response.css('.mz-productimages-thumb::attr(data-zoom-image)').extract()

    def parse_name(self, response):
        name = "".join(response.css('.mz-breadcrumb-current::text').extract()).strip()
        return name.replace("{} ".format(self.parse_brand(response)), '', 1)

    def parse_gender(self, response):
        gender = 'Undefined'
        for category in self.parse_category(response):
            if "Girls" in category:
                gender = 'Girls'
            elif "Boys" in category:
                gender = "Boys"
            elif "Men" in category:
                gender = "Men"
            elif "Women" in category:
                gender = "Women"
        return gender
