from six.moves.urllib_parse import urljoin

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from softsurroundings.items import Product


class SoftSurroundingsSpider(CrawlSpider):
    name = 'softsurroundings'
    seen_ids = set()

    allowed_domains = ['softsurroundings.com']

    start_urls = ['https://www.softsurroundings.com/p/erno-laszlo-hydratherapy-memory-sleep-mask/']

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
            yield Request(urljoin(response.url, f'page-{next_page}/'), callback=self.parse_product)

    def parse_product(self, response):
        if self.extract_retailer_sku(response) in self.seen_ids:
            return
        self.seen_ids.add(self.extract_retailer_sku(response))
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
        product['requests_queue'] += self.extract_category_request(response)

        return self.request_or_product(product)

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

    def parse_skus(self, response):
        product = response.meta['item']
        product["skus"].append(self.extract_sku(response))
        return self.request_or_product(product)

    def extract_category_request(self, response):
        requests_to_follow = []
        for category_id in response.css('#sizecat a:not(.sel)::attr(id)').extract():
            self.seen_ids.add(category_id.split('_')[1])
            request = response.follow(f"/p/{category_id.split('_')[1]}/", callback=self.parse_category)
            requests_to_follow.append(request)
        return requests_to_follow

    def parse_category(self, response):
        product = response.meta['item']
        product['requests_queue'] += self.extract_skus_requests(response)
        return self.request_or_product(product)

    def request_or_product(self, product):
        next_requests = product.get("requests_queue")

        if next_requests:
            request = next_requests.pop()
            request.meta['item'] = product
            return request

        del product["requests_queue"]
        return product

    def extract_color_map(self, response):
        raw_id = response.css('[name="uniqid"]::attr(value)').extract_first()
        color_id_css = f'input[name="specOne-{raw_id}"]::attr(value)'
        color_value_css = '#color .sizetbs .basesize::text'

        colors_map = {}
        for sel in response.css('#color .swatchlink img.color'):
            color_id = sel.css('::attr(data-value)').extract_first()
            colors_map[color_id] = sel.css('::attr(alt)').extract_first()

        return colors_map or {response.css(color_id_css).extract_first():
                              response.css(color_value_css).extract_first(default='')}

    def extract_size_map(self, response):
        size_value_css = '#size .sizetbs .basesize::text'

        sizes_map = {}
        for size_sel in response.css('#size a.size'):
            size_id = size_sel.css('::attr(id)').extract_first().split('_')[1]
            sizes_map[size_id] = size_sel.css('::text').extract_first()

        return sizes_map or {'000': response.css(size_value_css).extract_first(default='One Size')}

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
