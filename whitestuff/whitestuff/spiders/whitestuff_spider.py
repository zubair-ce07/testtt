import re
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from whitestuff.items import WhitestuffProduct


class WhitestuffSpiderSpider(CrawlSpider):
    name = "whitestuff_spider"
    allowed_domains = ["whitestuff.com"]
    start_urls = [
        'http://www.whitestuff.com/',
    ]

    listings_xpaths = ['//div[contains(@class,"flexbox")]//div',
                       '//*[@class="next"]']
    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpaths)),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="seoworkaround"]/a']),
             callback='parse_product_contents')
    )

    def parse_product_contents(self, response):
        item = WhitestuffProduct()
        item['spider_name'] = self.name
        item['retailer'] = 'whitestuff'
        item['currency'] = 'GBP'
        item['market'] = 'UK'
        item['category'] = self.product_category(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['price'] = self.product_price(response)
        item['description'] = self.product_description(response)
        item['url_original'] = response.url
        item['brand'] = 'White Stuff'
        item['image_urls'] = self.product_image_urls(response)
        item['care'] = []
        item['name'] = self.product_name(response)
        item['url'] = response.url
        item['gender'] = self.product_gender(response)
        item['industry'] = None
        item['skus'] = self.product_skus(response)
        yield item

    def product_category(self, response):
        return response.xpath('//div[@id="crumb"]//a//text()').extract()

    def product_price(self, response):
        return response.xpath('//meta[@property="product:price:amount"]//@content').extract()[0]

    def product_retailer_sku(self, response):
        return response.xpath('//div[@class="float-right f-12 pt"]//text()').extract()[0].split()[-1]

    def product_description(self, response):
        return [response.xpath('//div[@class="mtb"]//text()').extract()[0]]

    def product_name(self, response):
        return response.css('h1.f-bold::text').extract()

    def product_image_urls(self, response):
        images = []
        script = response.xpath('//script[contains(. ,"var imgItems")]').extract()
        data = re.findall('imgItems = ({[\s|\S]*})\s*//REM', script[0])[0]
        image_data = json.loads(data)

        base_url = 'http://8ecd5324393ba533cde7-3564c0ef81381895aa2677fe0727dfd2.r62.cf3.' \
                   'rackcdn.com/images/products/large/'
        for image in image_data.values():
            urls = image.strip('#').split('#')
            for url in urls:
                if 'http' in url:
                    images += [url]
                else:
                    images += [base_url + url]
        return images

    def product_gender(self, response):
        available_genders = ['Women', 'Men', 'Kids', 'Girls', ' Boys']
        category = self.product_category(response)
        for gender in available_genders:
            if any(gender.lower() in cat for cat in category):
                return gender
        return 'unisex-adults'

    def product_skus(self, response):
        skus = {}
        script = response.xpath('//script[contains(. ,"var variants")]').extract()
        data = re.findall('variants = ({[\s|\S]*})\s*var imgItems', script[0])[0]
        product_data = json.loads(data)
        price = response.xpath('//meta[@property="product:price:amount"]//@content').extract()[0]
        sku_common = {'currency': 'GBP', 'price': price}
        prev_price = response.xpath('//meta[@property="og:price:standard_amount"]//@content').extract()[0]
        if prev_price != price:
            sku_common['previous_prices'] = [prev_price]
        for prod in product_data.values():
            colour = prod['option1']
            size = self.extract_size(prod['option2'])
            sku = {'colour': colour, 'size': size}
            sku.update(sku_common)
            if not prod['sell']:
                sku['out_of_stock'] = True
            skus[colour + '_' + str(size)] = sku
        return skus

    def extract_size(self, size):
        if size.lower() == 'one size':
            return size
        prod_size = re.findall(r'\d+', size)
        return prod_size[0] if prod_size else size.split()[-1]
