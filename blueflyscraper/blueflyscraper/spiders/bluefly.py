from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BlueflyItem
from ..items import SkuItem


class BlueflySpider(CrawlSpider):
    name = "bluefly"
    allowed_domains = ['bluefly.com']
    start_urls = ['http://www.bluefly.com/']
    rules = [Rule(LinkExtractor(allow=['/[A-Za-z]+\/index']), process_links='link_filtering', follow=True),
             Rule(LinkExtractor(restrict_xpaths=('//a[@class="mz-productlisting-title"]')), callback='parse_blurefly_item'),
             Rule(LinkExtractor(restrict_xpaths=('//a[@class="mz-pagenumbers-next"]')))]
    custom_settings = {
        "DOWNLOAD_DELAY": 10
    }

    def link_filtering(self, links):
        for link in links:
            link.url = link.url.replace('/index', '?pageSize=96')
        return links

    def parse_blurefly_item(self, response):
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
        sku = SkuItem()
        sku['colour'] = self.parse_colour(response)
        sku['price'] = self.parse_price(response)
        sku['previous_prices'] = self.parse_prev_prices(response)
        sku['size'] = self.parse_size(response)
        item['skus'] = sku
        return item

    def parse_price(self, response):
        return response.css('div.mz-price::text').extract()[0].strip()

    def parse_size(self, response):
        return response.css('.mz-productoptions-sizebox::text').extract()

    def parse_prev_prices(self, response):
        return "".join(response.css(".mz-price.is-crossedout::text").extract()).strip()

    def parse_colour(self, response):
        return response.css('.mz-productoptions-optionvalue::text').extract()[0]

    def parse_product_id(self, url):
        url_pats = url.split("/")
        return url_pats[-1]

    def parse_brand(self, response):
        return response.css('.mz-productbrand >a::text').extract()[0]

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
        temp = "".join(response.css('.mz-breadcrumb-current::text').extract()).strip()
        return temp.replace("{} ".format(self.parse_brand(response)), '')

    def parse_gender(self, response):
        gender_val = response.css('.mz-breadcrumb-link:not(.is-first)::text').extract()[0]
        return gender_val if gender_val == "Men" or gender_val == "Women" or gender_val == "Kids" else "Undefined"
