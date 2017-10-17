from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SurfStitch(CrawlSpider):

    name = "surfstitch"
    start_urls = ['https://www.surfstitch.com/']
    product_css = ['.product-tile a']
    navigation_css = [
        'ul.menu-category.level-1 a',
        '#category-level-1 a',
        '#paging-bar-header .page-next',
        '.infinite-scroll-placeholder[data-loading-state="unloaded"]'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=navigation_css, tags=('a', 'div'), attrs=('href', 'data-grid-url')),),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

    def parse_product(self, response):
        garment = {}
        result = None
        garment['requests'] = []
        garment['skus'] = {}
        garment['name'] = self.product_name(response)
        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = self.product_image_urls(response)
        garment['features'] = self.product_features(response)
        selected_color_url, unselected_color_urls = self.selected_unselected_color(response)
        if selected_color_url:
            response.meta['garment'] = garment
            self.size_or_sku(response)
        if unselected_color_urls:
            garment['requests'] += self.color_request(garment, unselected_color_urls)
            result = self.request_or_garment(garment)
        return result if result else self.request_or_garment(garment)

    def color_request(self, garment, unselected_color_urls):
        requests = []
        for url in unselected_color_urls:
            requests.append(Request(url=url, callback=self.parse_color, meta={'garment': garment}))
        return requests

    def parse_color(self, response):
        return self.size_or_sku(response)

    def size_request(self, garment, unselected_size_urls):
        requests = []
        for url in unselected_size_urls:
            requests.append(Request(url=url, callback=self.parse_size, meta={'garment': garment}))
        return requests

    def parse_size(self, response):
        return self.update_sku(response)

    def size_or_sku(self, response):
        result = None
        selected_size_url, unselected_size_urls = self.selected_unselected_size(response)
        if selected_size_url:
            result = self.update_sku(response)
        if unselected_size_urls:
            response.meta['garment']['requests'] += self.size_request(response.meta['garment'], unselected_size_urls)
            result = self.request_or_garment(response.meta['garment'])
        return result if result else self.update_sku(response)

    def update_sku(self, response):
        selected_color, selected_size, price_standard, price_sales = self.sku_values(response)
        if selected_size:
            sku_id = selected_color.strip() + "_" + selected_size.strip()
        else:
            sku_id = selected_color.strip() + "_" + "ONE_SIZE"
        response.meta['garment']['skus'][sku_id] = {
            'size': selected_size,
            'color': selected_color.strip(),
            'price': price_sales.strip() if price_sales else price_standard.strip()
        }

        return self.request_or_garment(response.meta['garment'])

    def product_name(self, response):
        return response.css('.product-name::text').extract_first().strip()

    def product_brand(self, response):
        return response.css('.brand-name::text').extract_first().strip()

    def product_image_urls(self, response):
        return [response.urljoin(image_url) for image_url in response.css('#thumbnails a::attr(href)').extract()]

    def product_features(self, response):
        return response.css('.tab:first-child li::text').extract()

    def request_or_garment(self, garment):
        if garment['requests']:
            return garment['requests'].pop()
        return garment

    def selected_unselected_color(self, response):
        selected_color_url = response.css('li.selectable.selected.swiper-slide a::attr(href)').extract()
        unselected_color_urls = response.css('li.selectable.swiper-slide a::attr(href)').extract()
        unselected_color_urls = set(unselected_color_urls) - set(selected_color_url)
        return selected_color_url, unselected_color_urls

    def selected_unselected_size(self, response):
        selected_size_url = response.css('.selectable.selected.variation-group-value a::attr(href)').extract()
        unselected_size_urls = response.css('.selectable.variation-group-value a::attr(href)').extract()
        unselected_size_urls = set(unselected_size_urls) - set(selected_size_url)
        return selected_size_url, unselected_size_urls

    def sku_values(self, response):
        selected_color = response.css('ul.swatches.swatchcolour .selected-value::text').extract_first()
        selected_size = response.css('ul.swatches.size .selected-value::text').extract_first()
        price_standard = response.css('.product-price .price-standard::text').extract_first()
        price_sales = response.css('.product-price .price-sales::text').extract_first()
        return selected_color, selected_size, price_standard, price_sales
