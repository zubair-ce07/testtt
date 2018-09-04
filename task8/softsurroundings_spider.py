from itertools import product

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from softsurroundings.items import Product


class SoftSurroundingsSpider(CrawlSpider):
    name = 'softsurroundings'
    allowed_domains = ['softsurroundings.com']

    start_urls = ['https://www.softsurroundings.com/']

    listing_css = '#menuNav'
    product_css = '.product'
    pagination_css = '.thumbscroll [name="page"]::attr(value)'
    retailer_skus = set()

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        yield from super().parse(response)
        yield from self.parse_listing(response)

    def parse_listing(self, response):
        next_pages = response.css(self.pagination_css).extract()
        for next_page in next_pages:
            yield Request(f'{response.url}page-{next_page}/', callback=self.parse)

    def parse_product(self, response):
        if self.extract_retailer_sku(response) in self.retailer_skus:
            return
        self.retailer_skus.add(self.extract_retailer_sku(response))
        product = Product()

        product['gender'] = self.extract_gender(response)
        product['name'] = self.extract_product_name(response)
        product['image_urls'] = self.extract_image_urls(response)
        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['description'] = self.extract_description(response)
        product['category'] = self.extract_categories(response)
        product['url'] = self.extract_product_url(response)
        product['brand'] = self.extract_brand(response)
        product['care'] = self.extract_care(response)
        product['skus'] = []
        product['requests_queue'] = self.extract_skus_requests(response)

        yield self.requests_to_follow(product)

        yield from self.category_request(response)

    def category_request(self, response):
        prod_category_ids = response.css('#sizecat a:not(.sel)::attr(id)').extract()
        for prod_category_id in prod_category_ids:
            prod_category_url = f"https://www.softsurroundings.com/p/{prod_category_id.split('_')[1]}/"
            yield Request(prod_category_url, callback=self.parse_product)

    def requests_to_follow(self, product_item):
        next_requests = product_item.get("requests_queue")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product_item
            return request

        del product_item["requests_queue"]

        return product_item

    def extract_skus_requests(self, response):
        color_ids = self.extract_color_ids(response)
        size_ids = self.extract_size_ids(response)
        requests_to_follow = []
        for color_id, size_id in product(color_ids, size_ids):
            meta = {}
            meta['color'] = self.extract_color(response, color_id)
            meta['size'] = self.extract_size(response, size_id)

            size_id = size_id.split("_")[1]
            sku_request_url = f'{response.url}{color_id}{size_id}'
            request = Request(sku_request_url, meta=meta, callback=self.parse_skus)

            requests_to_follow.append(request)

        return requests_to_follow

    def parse_skus(self, response):
        product_item = response.meta['item']
        product_item["skus"].append(self.extract_sku(response))
        return self.requests_to_follow(product_item)

    def extract_color_ids(self, response):
        raw_id = response.css('[name="uniqid"]::attr(value)').extract_first()

        color_id_css = f'#color .swatchlink img::attr(data-value),' \
                       f'input[name="specOne-{raw_id}"]::attr(value)'
        color_ids = response.css(color_id_css).extract()
        return set(filter(None, color_ids))

    def extract_size_ids(self, response):
        size_ids = response.css('#size a.size::attr(id)').extract() or ['size_000']
        return set(filter(None, size_ids))

    def extract_color(self, response, color_id):
        color_css = f'img[data-value="{color_id}"]::attr(alt),#color .sizetbs .basesize::text'
        return response.css(color_css).extract_first(default='')

    def extract_size(self, response, size_id):
        size_css = f'a[id="{size_id}"]::text,#size .sizetbs .basesize::text'
        return response.css(size_css).extract_first(default='One Size')

    def extract_sku(self, response):
        sku = {}
        sku['currency'] = response.css('.dtlHeader [itemprop="priceCurrency"]::text').extract_first()
        sku['price'] = response.css('.dtlHeader [itemprop="price"]::text').extract_first()
        sku['color'] = response.meta['color']
        sku['size'] = response.meta['size']
        sku['sku_id'] = f"{response.meta['color']}_{response.meta['size']}"
        raw_prev_price = response.css('.dtlHeader .ctntPrice::text').re('Was([^;]+)')

        if raw_prev_price:
            sku['previous_price'] = [raw_prev_price[0].strip()[1:]]

        prod_stock_status = response.css('#orderProcessError ::text')

        if prod_stock_status:
            sku['out_of_stock'] = True

        return sku

    def extract_gender(self, response):
        if 'bedding' in ' '.join(self.extract_categories(response)).lower():
            return "unisex-adults"
        return "Women"

    def extract_image_urls(self, response):
        raw_image_urls = response.css('#detailAltImgs ::attr(src)').extract()
        return [url.replace('/80x120/', '/1200x1802/') for url in raw_image_urls]

    def extract_product_name(self, response):
        return response.css('.dtlHeader [itemprop="name"]::text').extract_first()

    def extract_care(self, response):
        return response.css('#careAndContentInfo span::text, #directionsInfo ::text').extract()

    def extract_description(self, response):
        return response.css('.productInfo ::text').extract()

    def extract_retailer_sku(self, response):
        return response.css('.dtlHeader [itemprop="productID"]::text').extract_first()

    def extract_brand(self, response):
        brand_css = '.productInfoDetails li:contains("Designed by")::text,' \
                    '#aboutbrandInfo img::attr(alt)'
        return response.css(brand_css).extract_first(default='Soft Surroundings')

    def extract_product_url(self, response):
        return response.url

    def extract_categories(self, response):
        return response.css('.pagingBreadCrumb ::text').extract()
