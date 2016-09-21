from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BlueflyItem


class BlueflySpider(CrawlSpider):
    name = "bluefly"
    allowed_domains = ['bluefly.com']
    start_urls = ['http://www.bluefly.com/']
    rules = [Rule(LinkExtractor(allow=['/[A-Za-z]+\/index']), process_links='link_filtering', follow=True),
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
        item['product_title'] = self.parse_product_title(response)
        item['description'] = self.parse_description(response)
        item['care'] = self.parse_care(response)
        item['gender'] = self.parse_gender(response)
        item['skus'] = self.parse_skus(response)
        return item

    def parse_skus(self, response):
        skus = {}
        for size in self.parse_numeric_sizes(response):
            skus[size] = self.parse_sku(response, size)
        return skus

    def parse_sku(self, response, numeric_size):
        sku = {}
        size = self.parse_size(response, numeric_size)
        if size:
            sku['size'] = size
        sku['price'] = self.parse_price(response)
        sku['currency'] = 'USD'
        sku['previous_prices'] = self.parse_prev_prices(response)
        sku['colour'] = self.parse_colour(response)
        return sku

    def parse_numeric_sizes(self, response):
        css = ".mz-productoptions-sizebox::attr(data-value)"
        return response.css(css).extract() or ['default']

    def parse_price(self, response):
        return response.css('div.mz-price::text').extract()[0].strip()

    def parse_size(self, response, data_value):
        size = response.css(".mz-productoptions-sizebox[data-value = '{}']::text".format(data_value))
        return size.extract()[0] if size else ''

    def parse_prev_prices(self, response):
        prev_prices = "".join(response.css(".mz-price.is-crossedout::text").extract())
        return [prev_prices.replace('Retail:', '').strip()] if prev_prices else ''

    def parse_colour(self, response):
        css1 = '.product-color-list > li > a::attr(title)'
        css2 = '.mz-productoptions-optionvalue::text'
        return response.css(css1).extract() or response.css(css2).extract()[0]

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
        return merch_info[0] if merch_info else ""

    def parse_image_urls(self, response):
        return response.css('.mz-productimages-thumbimage::attr(src)').extract()

    def parse_product_title(self, response):
        product_title = "".join(response.css('.mz-breadcrumb-current::text').extract()).strip()
        return product_title.replace("{} ".format(self.parse_brand(response)), '', 1)

    def parse_gender(self, response):
        gender_val = response.css('.mz-breadcrumb-link:not(.is-first)::text').extract()[0]
        return gender_val if gender_val in["Men", "Women", "Kids"] else "Undefined"
