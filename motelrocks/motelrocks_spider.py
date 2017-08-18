import re
import scrapy
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrape_motelrocks.items import MotelRocksItem


class MotelRocksSpider(CrawlSpider):
    name = "motelrocks_spider"
    allowed_domains = ["motelrocks.com"]
    start_urls = ['http://www.motelrocks.com/']

    rules = (Rule(LinkExtractor(restrict_css=('ul#nav-menu li a',)), callback='request_next_pages'),)

    def get_category_id(self, response):
        categoryid = response.xpath('//script[contains(.,"catid:")]//text()').extract_first()
        categoryid = re.search('categoryid:.-?(\w)+.', categoryid).group().split(':')[1]
        return re.sub('[^\w]', '', categoryid)

    def request_next_pages(self, response):
        total_pages = int(response.css('div.pageitem::text').extract()[-2])
        pagenum = 1
        categoryid = self.get_category_id(response)

        while pagenum <= total_pages:
            formdata = {'page': str(pagenum), 'invocation': 'page', 'categoryid': categoryid}
            yield FormRequest(
                url='http://www.motelrocks.com/categories_ajax.php',
                formdata=formdata,
                callback=self.extract_current_page_links
            )
            pagenum += 1

    def extract_current_page_links(self, response):
        product_links = response.css('div.catproddiv .xProductDetails a::attr(href)').extract()
        for link in product_links:
            yield scrapy.Request(link, callback=self.parse_motelrocks_item)

    def parse_brand_name(self):
        return 'MotelRocks'

    def parse_description_info(self, response):
        return response.css('#Details p span::text').extract()

    def parse_item_name(self, response):
        return response.css('#product-desc h1::text').extract_first()

    def parse_item_url(self, response):
        return response.url

    def parse_retailer_sku_info(self, response):
        return response.css('input#product_id::attr(value)').extract_first()[:-3]

    def parse_gender(self):
        return 'women'

    def parse_item_other_color_urls(self, response):
        return response.css('#colourswatch .colswatch::attr(href)').extract()

    def parse_image_urls(self, response):
        return response.css('div#ProductDetails .prodpicsidethumb img::attr(src)').extract()[:5]

    def parse_item_price(self, response):
        price = response.css('em.ProductPrice::text').extract_first()
        if price:
            return price.encode('ascii', 'ignore')
        else:
            sale_price = response.css('em.ProductPrice span::text').extract_first()
            return sale_price.encode('ascii', 'ignore')

    def parse_sku_color_info(self, response, motelrocks_item):
        motelrocks_item['image_urls'].append(self.parse_image_urls(response))
        motelrocks_item['description'].append(self.parse_description_info(response))
        product_id = response.css('input#product_id::attr(value)').extract_first()
        price = self.parse_item_price(response)
        color = response.css('#colourswatch .colswatch::attr(title)').extract_first()
        currency = 'GBP'

        all_sizes = response.css('div.Value ul li')
        for size in all_sizes:
            size_detail = size.css('.sizeli-unselected::text').extract()[1].strip()
            sku_size_id = '{0}_{1}'.format(product_id, size_detail)
            motelrocks_item['skus'][sku_size_id] = {'price': price, 'color': color,
                                                    'currency': currency, 'size': size_detail}
            if not int(size.css('.sizeli-unselected::attr(instock)').extract_first()):
                motelrocks_item['skus'][sku_size_id]['out_of_stock'] = True

    def request_another_color_or_yield_item(self, other_color_urls, motelrocks_item):
        if other_color_urls:
            yield scrapy.Request(other_color_urls.pop(), dont_filter=True, callback=self.parse_sku_info, meta={
                                                                            'other_color_urls': other_color_urls,
                                                                            'motelrocks_item': motelrocks_item})
        else:
            yield motelrocks_item

    def parse_sku_info(self, response):
        other_color_urls = response.meta['other_color_urls']
        motelrocks_item = response.meta['motelrocks_item']
        self.parse_sku_color_info(response,  motelrocks_item)
        return self.request_another_color_or_yield_item(other_color_urls, motelrocks_item)

    def parse_motelrocks_item(self, response):
        motelrocks_item = MotelRocksItem()
        motelrocks_item['brand'] = self.parse_brand_name()
        motelrocks_item['care'] = []
        motelrocks_item['category'] = []
        motelrocks_item['description'] = []
        motelrocks_item['image_urls'] = []
        motelrocks_item['name'] = self.parse_item_name(response)
        motelrocks_item['url'] = self.parse_item_url(response)
        motelrocks_item['retailer_sku'] = self.parse_retailer_sku_info(response)
        motelrocks_item['gender'] = self.parse_gender()
        other_color_urls = self.parse_item_other_color_urls(response)
        motelrocks_item['skus'] = {}
        self.parse_sku_color_info(response, motelrocks_item)
        return self.request_another_color_or_yield_item(other_color_urls, motelrocks_item)
