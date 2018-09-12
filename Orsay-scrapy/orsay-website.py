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
        Rule(LinkExtractor(allow=[r".*/produkte/", r".*/neuheiten/", r".*/sale/", r".*/trends/"]),
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
        item['url'] = response.url
        item['image_urls'] = []
        item['retailer_sku'] = data_json.get('idListRef6')
        item['skus'] = {}

        color_urls = response.css('.swatches.color>li:not(.selected) a::attr(href)').extract()

        # Initial values for response
        meta_data = {}
        meta_data['item'] = item
        meta_data['color_urls'] = color_urls
        response.meta.update(meta_data)

        for func in self.iterate_over_colors(response):
            yield func

    def iterate_over_colors(self, response):
        color_urls = response.meta.get('color_urls')
        size_links = response.meta.get('size_links', [])
        item = response.meta.get('item')
        item['image_urls'] += self.get_images(response)

        product_color = self.get_size_color(response)
        product_sku = self.get_size_sku(response)
        for size_tag in response.css('ul.swatches.size>li'):
            size_tag_info = {}
            size_tag_info['product_color'] = product_color
            size_tag_info['product_sku'] = product_sku
            size_tag_info['size_tag'] = size_tag
            size_tag_info['size_name'] = self.get_size_name(size_tag)
            size_tag_info['size_available'] = self.is_size_available(size_tag)
            size_links.append(size_tag_info)

        meta_data = {}
        meta_data['size_links'] = size_links
        meta_data['item'] = item

        if color_urls:
            color_url = color_urls.pop(0)
            meta_data['color_urls'] = color_urls
            yield Request(url=color_url, meta=meta_data, callback=self.iterate_over_colors)
        else:
            response.meta.update(meta_data)
            for func in self.iterate_over_sizes(response, True):
                yield func

    def iterate_over_sizes(self, response, first_iter=False):
        """A recursive function to parse sizes of product"""
        size_links = response.meta.get('size_links')
        item = response.meta.get('item')

        if not first_iter:
            item = self.append_sizes_info(response)

        if size_links:
            next_size = size_links.pop(0)
            meta_data = {}
            meta_data['size_links'] = size_links
            meta_data['item'] = item
            meta_data['size_data'] = next_size

            if next_size.get('size_available'):
                size_url = next_size.get('size_tag').css('::attr(href)').extract_first()
                next_url = f"{size_url}&Quantity=1&format=ajax&productlistid=undefined"

                yield Request(url=next_url, meta=meta_data, dont_filter=True,
                              callback=self.iterate_over_sizes)
            else:
                response.meta.update(meta_data)
                for func in self.iterate_over_sizes(response):
                    yield func
        else:
            yield item

    def append_sizes_info(self, response):
        """This function takes a response object and finds and return product item"""
        data = response.css('::attr(data-product-details)').extract_first()
        data_json = json.loads(data)

        size_data = response.meta.get('size_data')
        item = response.meta.get('item')

        size_info = SizeInfo()
        size_info['out_of_stock'] = not size_data.get('size_available')
        size_info['colour'] = size_data.get('product_color')
        size_info['size'] = size_data.get('size_name')
        size_info['price'] = data_json.get('grossPrice')
        size_info['currency'] = data_json.get('currency_code')

        sku_id = f"{size_data.get('product_sku')}_{size_info.get('size')}"
        item['skus'][sku_id] = size_info

        return item

    def is_size_available(self, size_tag):
        """Returns true if the size is available"""
        return True if size_tag.css('.selectable').extract() else False

    def get_size_sku(self, response):
        """Extracts and returns Sku of product"""
        return response.css('isapplepay::attr(sku)').extract_first()

    def get_size_color(self, response):
        """Extracts and returns color of product"""
        return response.css('.selected-value::text').extract_first()

    def get_size_name(self, response):
        """Extracts and returns Size of product"""
        try:
            size_name = response.css('::text').extract()[1].replace('\n', '')
        except IndexError:
            size_name = ''

        return size_name

    def get_care(self, response):
        """Extracts and returns Care of product"""
        return response.css('div.product-info-block p::text').extract_first()

    def get_detail(self, response):
        """Extracts and returns Details of product"""
        description = response.css('.with-gutter::text').extract()
        return description

    def get_images(self, response):
        """Extracts and returns Images of product"""
        return response.css('.productthumbnail::attr(src)').extract()

    def get_product_count(self, response):
        """ It returns total number of products present in a specific category"""
        try:
            count = int(response.css('::attr(data-count)').extract_first())
        except TypeError:
            count = 0
        return count

