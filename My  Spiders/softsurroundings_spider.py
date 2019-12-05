from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Product
from ..utils import map_gender, format_price


class ParseSpider():
    one_size = "One Size"

    def parse_product(self, response):
        product = Product()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = self.get_care(response)
        product['skus'] = {}
        product['image_urls'] = self.get_image_urls(response)
        product['requests'] = self.size_category_requests(response) or self.sku_requests(response)

        return self.request_or_product(product)

    def parse_size_category(self, response):
        product = response.meta['product']
        product['requests'] += self.sku_requests(response)
        return self.request_or_product(product)

    def parse_sku(self, response):
        product = response.meta['product']
        skus = self.get_skus(response)
        product['skus'].update(skus)

        return self.request_or_product(product)

    def get_retailer_sku(self, response):
        return response.css('#item::text').get()

    def get_brand(self, response):
        return response.css('[property="og:site_name"]::attr(content)').get()

    def get_gender(self, response):
        soup = response.css('#sizecat a::text, title::text').getall()
        gender_soup = ' '.join(self.get_description(response))
        return map_gender(' '.join(soup)) or map_gender(gender_soup)

    def get_care(self, response):
        return response.css('#careAndContentInfo::text').getall()

    def get_category(self, response):
        return response.css('.pagingBreadCrumb a::text').getall()

    def get_description(self, response):
        css = '[itemprop="description"] p::text, [itemprop="description"]::text'
        return response.css(css).getall()

    def get_url(self, response):
        return response.url

    def get_name(self, response):
        return response.css('[itemprop="name"]::text').get()

    def get_image_urls(self, response):
        return response.css('#detailAltImgs > li a::attr(href)').getall()

    def get_skus(self, response):
        colour = response.css('.dtlFormBulk #color b::text').get()
        size = response.css('.dtlFormBulk #size b::text').get() or self.one_size

        sku = {'colour': colour} if colour else {}
        sku.update(self.get_price(response))
        sku['size'] = size
        sku['out_of_stock'] = response.css('.stockStatus b::text').get() != 'In Stock'

        return {f'{colour}_{size}' if colour else size: sku}

    def get_price(self, response):
        previous_price = response.css('.ctntPrice::text').re_first(r'Was \$(.*);')
        current_price = response.css('[itemprop="price"]::text').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()

        return format_price(currency, current_price, previous_price)

    def size_category_requests(self, response):
        cat_ids = [i.split('_')[1] for i in response.css('#sizecat > a::attr(id)').getall()]
        return [response.follow(f'/p/{i.lower()}', callback=self.parse_size_category, dont_filter=True)
                for i in cat_ids]

    def sku_requests(self, response):
        sku_requests = []
        product_id = self.get_retailer_sku(response)

        color_css = '.swatchlink .color::attr(data-value), #color + input::attr(value)'
        color_ids = [i for i in response.css(color_css).getall() if i] \
            or response.css('[name^="specOne"]::attr(value)').getall()

        size_ids = [size.split('_')[1] for size in response.css('a.box.size::attr(id)').getall()] \
            or response.css('[name^="specTwo"]::attr(value)').getall()
        for color_id in color_ids:
            for size_id in size_ids:
                url = f'/p/{product_id.lower()}/{color_id}{size_id}'
                sku_requests.append(response.follow(url, callback=self.parse_sku))

        return sku_requests

    def request_or_product(self, product):
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product


class CrawlSpider(CrawlSpider):
    name = 'softsurroundings_spider'
    allowed_domains = ['softsurroundings.com']
    start_urls = ['https://www.softsurroundings.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    listings_css = ['ul#menubar']
    product_css = ['div.product']
    deny_re = ['gift-card']

    softsurroundings_parser = ParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css, deny=deny_re), callback='parse_item')
    )

    def parse_pagination(self, response):
        total_pages = response.css('.thumbscroll [name="page"]::attr(value)').getall()
        category_url = f"{response.url}/page-{int(total_pages[-1])}" if total_pages else response.url
        return response.follow(category_url, callback=self.parse)

    def parse_item(self, response):
        return self.softsurroundings_parser.parse_product(response)
