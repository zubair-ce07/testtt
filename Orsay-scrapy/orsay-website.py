import json
from scrapy import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from orsay.items import SizeInfo, OrsayItem


class OrsayCrawler(CrawlSpider):
    """This crawler crawls orsay website and extracts all the information from the website"""
    name = 'Orsay'
    allowed_domains = ["orsay.com"]
    start_urls = ['http://www.orsay.com']

    rules = (
        Rule(LinkExtractor(allow=r".*/produkte/"), callback='parse_categories'),
        Rule(LinkExtractor(restrict_css=".product-swatch-item"), callback='parse_products')
    )

    def parse_categories(self, response):
        """This method takes response of each category and iterate over all the products
         present in a category
        """

        total_products_count = self.get_product_count(response)

        for count in range(0, total_products_count, 72):
            yield Request(url=f"{response.url}?start={count}&format=page-element")

    def parse_products(self, response):
        """This function will extract information of products,it takes response of product page
        and besides extracting info it also traverses onto different pages associated with the
        product sizes
        """
        data = response.css('::attr(data-product-details)').extract_first()
        data_json = json.loads(data)
        item = OrsayItem()
        item['brand'] = 'Orsay'
        item['gender'] = 'women'
        item['name'] = data_json.get('name')
        item['category'] = data_json.get('categoryName')
        item['care'] = self.get_care(response)
        item['description'] = self.get_detail(response)
        item['image_urls'] = self.get_images(response)
        item['url'] = response.url
        item['retailer_sku'] = data_json.get('idListRef6')
        item['skus'] = {}

        price = data_json.get('grossPrice')
        color = data_json.get('color')
        currency = data_json.get('currency_code')

        for li in response.css('ul.swatches li'):
            size = str(li.css("a::text").extract_first()).replace('\n', '')
            if size:
                size_info = SizeInfo()
                size_info['out_of_stock'] = True
                class_selectable=li.css('.selectable').extract()
                if len(class_selectable) > 0:
                    size_info['out_of_stock'] = False

                size_info['price'] = price
                size_info['colour'] = color
                size_info['currency'] = currency
                size_info['size'] = size
                item['skus'][data_json.get('idListRef6') + '_' + size] = size_info
        yield item

    def get_care(self, response):
        """Extracts and returns Care of product"""

        return response.css('div.product-info-block p::text').extract_first()

    def get_detail(self, response):
        """Extracts and returns Details of product"""

        try:
            description = response.css('div.product-details>div>div::text').extract()[1:]
        except IndexError:
            description = ''

        return description

    def get_images(self, response):
        """Extracts and returns Images of product"""

        return response.css('img.productthumbnail::attr(src)').extract()

    def get_product_count(self, response):
        """ It returns total number of products present in a specific category"""

        return int(response.css('::attr(data-count)').extract_first())

