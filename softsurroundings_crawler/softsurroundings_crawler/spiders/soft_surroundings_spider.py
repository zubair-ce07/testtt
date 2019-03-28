import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import datetime
from urllib.parse import urljoin
from softsurroundings_crawler.items import SoftsurroundingsCrawlerItem, ProductLoader


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
        request = []
        product = self.parse_info(response)
        size_ids = self.category_size(response)
        product['skus'] = []

        for size in size_ids:
            page_request = scrapy.Request(urljoin(response.url, size), callback=self.parse_skus)
            request.append(page_request)

        product['requests'] = request

        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request

        return product

    def parse_info(self, response):
        item = ProductLoader(item=SoftsurroundingsCrawlerItem(), response=response)
        item.add_css('pid', 'span[itemprop="productID"]::text')
        item.add_value('gender', 'women')
        item.add_css('category', '.pagingBreadCrumb > a::text')
        item.add_value('brand', 'Soft Surroundings')
        item.add_value('url', response.url)
        item.add_css('name', 'span[itemprop="name"]::text')
        item.add_css('description', '.productInfo::text')
        item.add_css('description', '.productInfo > p::text')
        item.add_css('care', '.tabContent.sel::text')
        item.add_css('image_urls', '.alt_dtl::attr(href)')
        return item.load_item()

    def category_size(self, response):
        size_ids = response.css('#sizecat > a::attr(id)').getall()
        size = [size.split('_')[1] for size in size_ids]
        return size

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'].append(self.skus(response))

        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request

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
