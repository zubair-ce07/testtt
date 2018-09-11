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
        Rule(LinkExtractor(allow=(r".*/produkte/", r".*/neuheiten/", r".*/sale/", r".*/trends/")),
             callback='parse_categories'),
        Rule(LinkExtractor(restrict_css=".product-image>a"), callback='parse_products')
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

        colors = response.css('.swatches.color a::attr(href)').extract()

        if len(colors) > 0:
            del colors[0]

        # initial values for response
        response.meta.update({'item': item, 'colors': colors, 'li': []})
        for func in self.iterate_over_colors(response):
            yield func

    def iterate_over_colors(self, response):
        colors = response.meta.get('colors')
        li = response.meta.get('li')
        item = response.meta.get('item')
        if len(colors) >= 0:
            li += response.css('ul.swatches.size>li')
        if len(colors) > 0:
            color_url = colors[0]
            del colors[0]
            yield Request(url=color_url, callback=self.iterate_over_colors,
                          meta={'li': li, 'item': item, 'colors': colors})
        else:
            response.meta.update({'li': li, 'item': item})
            for func in self.iterate_over_sizes(response, True):
                yield func

    def iterate_over_sizes(self, response, first_iter=False):
        """A recursive function to parse sizes of product"""
        lis = response.meta.get('li', [])
        item = response.meta.get('item')

        if len(lis) >= 0 and not first_iter:
            size_info = self.get_size_info(response)
            size = size_info.get('info')
            sku = size_info.get('sku')
            item['skus'][str(sku) + '_' + size.get('size')] = size

        if len(lis) > 0:
            next_size = lis[0]
            del lis[0]

            try:
                size_name = next_size.css('::text').extract()[1].replace('\n', '')
            except IndexError:
                size_name = ''

            if len(next_size.css('.selectable').extract()) > 0:
                yield Request(url=next_size.css(
                    '::attr(href)').extract_first() + '&Quantity=1&format=ajax&productlistid=undefined',
                              callback=self.iterate_over_sizes,
                              meta={'li': lis, 'item': item, 'out_of_stock': False, 'size': size_name})
            else:
                response.meta.update({'li': lis, 'item': item, 'out_of_stock': True, 'size': size_name})
                for func in self.iterate_over_sizes(response):
                    yield func
        else:
            yield item

    def get_size_info(self, response):
        """This function takes a response object and finds and return product info"""
        data = response.css('::attr(data-product-details)').extract_first()
        data_json = json.loads(data)
        current_size = response.meta.get('size', '')
        size_info = SizeInfo()
        size_info['out_of_stock'] = response.meta.get('out_of_stock')
        size_info['price'] = data_json.get('grossPrice')
        size_info['colour'] = data_json.get('color')
        size_info['currency'] = data_json.get('currency_code')
        size_info['size'] = current_size

        sku = data_json.get('idListRef12')

        size_response = {}
        size_response['info'] = size_info
        size_response['sku'] = sku
        return size_response

    def get_care(self, response):
        """Extracts and returns Care of product"""

        return response.css('div.product-info-block p::text').extract_first()

    def get_detail(self, response):
        """Extracts and returns Details of product"""

        try:
            description = response.css('.with-gutter::text').extract()
        except IndexError:
            description = ''

        return description

    def get_images(self, response):
        """Extracts and returns Images of product"""

        return response.css('.productthumbnail::attr(src)').extract()

    def get_product_count(self, response):
        """ It returns total number of products present in a specific category"""

        return int(response.css('::attr(data-count)').extract_first())

