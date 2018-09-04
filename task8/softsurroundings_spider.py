from six.moves.urllib_parse import urljoin

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from softsurroundings.items import Product


class SoftSurroundingsSpider(CrawlSpider):
    name = 'softsurroundings'
    seen_ids = set()

    allowed_domains = ['softsurroundings.com']

    start_urls = ['https://www.softsurroundings.com/']

    listing_css = '#menuNav'
    product_css = '.product'
    pagination_css = '.thumbscroll [name="page"]::attr(value)'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        yield from super().parse(response)
        for next_page in response.css(self.pagination_css).extract():
            yield Request(urljoin(response.url, f'page-{next_page}/'), callback=self.parse)

    def parse_product(self, response):
        if not self.validate_product(response):
            return
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
        product['requests_queue'].extend(self.extract_category_request(response))

        return self.request_or_product(product)

    def validate_product(self, response):
        if self.extract_retailer_sku(response) in self.seen_ids:
            return False
        self.seen_ids.add(self.extract_retailer_sku(response))
        return True

    def extract_skus_requests(self, response):
        colors_map = self.extract_color_map(response)
        sizes_map = self.extract_size_map(response)
        requests_to_follow = []
        for color_id, color_value in colors_map.items():
            for size_id, size_value in sizes_map.items():
                meta = {}
                meta['color'] = color_value
                meta['size'] = size_value
                sku_request_url = urljoin(response.url, f'{color_id}{size_id}/')
                request = Request(sku_request_url, meta=meta, callback=self.parse_skus)
                requests_to_follow.append(request)
        return requests_to_follow

    def extract_category_request(self, response):
        requests_to_follow = []
        for prod_category_id in response.css('#sizecat a:not(.sel)::attr(id)').extract():
            prod_category_url = urljoin('https://www.softsurroundings.com/p/',
                                        f"{prod_category_id.split('_')[1]}/")
            request = Request(prod_category_url, callback=self.parse_category)
            requests_to_follow.append(request)
        return requests_to_follow

    def request_or_product(self, product):
        next_requests = product.get("requests_queue")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product
            return request

        del product["requests_queue"]
        return product

    def parse_skus(self, response):
        product = response.meta['item']
        product["skus"].append(self.extract_sku(response))
        return self.request_or_product(product)

    def parse_category(self, response):
        product = response.meta['item']
        if self.validate_product(response):
            raw_retailer_sku = set(self.extract_retailer_sku(response)) & set(product['retailer_sku'])
            if raw_retailer_sku:
                product['retailer_sku'] = ''.join(raw_retailer_sku)
            product['requests_queue'].extend(self.extract_skus_requests(response))
        return self.request_or_product(product)

    def extract_color_map(self, response):
        raw_id = response.css('[name="uniqid"]::attr(value)').extract_first()

        color_id_css = f'#color .swatchlink img::attr(data-value),' \
                       f'input[name="specOne-{raw_id}"]::attr(value)'
        color_ids = response.css(color_id_css).extract()
        return {c_id: self.extract_color(response, c_id) for c_id in color_ids if c_id}

    def extract_size_map(self, response):
        size_ids = response.css('#size a.size::attr(id)').extract() or ['size_000']
        size_ids = [s.split('_')[1] for s in size_ids]
        return {s_id: self.extract_size(response, s_id) for s_id in size_ids}

    def extract_color(self, response, color_id):
        color_css = f'img[data-value="{color_id}"]::attr(alt),#color .sizetbs .basesize::text'
        return response.css(color_css).extract_first(default='')

    def extract_size(self, response, size_id):
        size_css = f'a[id="size_{size_id}"]::text,#size .sizetbs .basesize::text'
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

        if response.css('#orderProcessError ::text'):
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
