import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import datetime
from urllib.parse import urljoin
from softsurroundings_crawler.items import SoftSurroundingsCrawlerItem, ProductLoader


class SoftSurroundingSpider(CrawlSpider):
    name = 'soft_surroundings_spider'
    start_urls = ['https://www.softsurroundings.com/']

    category_css = '.clMn'
    product_css = '.product'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        product = self.parse_info(response)
        product['skus'] = []
        product['requests'] = self.size_requests(response)

        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product

    def parse_info(self, response):
        product = ProductLoader(item=SoftSurroundingsCrawlerItem(), response=response)
        product.add_css('pid', 'span[itemprop="productID"]::text')
        product.add_value('gender', 'women')
        product.add_css('category', '.pagingBreadCrumb > a::text')
        product.add_value('brand', 'Soft Surroundings')
        product.add_value('url', response.url)
        product.add_css('name', 'span[itemprop="name"]::text')
        product.add_css('description', '.productInfo::text')
        product.add_css('description', '.productInfo > p::text')
        product.add_css('care', '.tabContent.sel::text')
        product.add_css('image_urls', '.alt_dtl::attr(href)')
        return product.load_item()

    def category_size(self, response):
        size_ids = response.css('#sizecat > a::attr(id)').getall()
        size = [size.split('_')[1] for size in size_ids]
        return size

    def size_requests(self, response):
        request = []
        size_ids = self.category_size(response)
        for size in size_ids:
            page_request = scrapy.Request(urljoin(response.url, size),
                                          callback=self.parse_skus)
            request.append(page_request)

        return request

    def parse_skus(self, response):
        product = response.meta['product']
        product_skus = self.skus(response)

        if product_skus:
            product['skus'].append(product_skus)

        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product

    def skus(self, response):
        product_detail = []

        previous_price = response.css('.ctntPrice::text').get()
        price = response.css('span[itemprop="price"]::text').get()
        currency = response.css('span[itemprop="priceCurrency"]::attr(content)').get()

        size_options = response.css('#size a::text ,#size >div > .basesize::text').getall()
        colour_options = response.css('#color > .swatchlink > img::attr(alt) ,#color > div > .basesize::text').getall()

        for sku_id in size_options[1:]:
            for color in colour_options:
                product = {
                    'color': color,
                    'size': sku_id,
                    'sku_id': color + "_" + sku_id,
                    'currency': currency,
                    'price': price,
                }

                if previous_price:
                    product.update({'previous price': previous_price.split(' ')[1]})

                product_detail.append(product)
        return product_detail

