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
        garment['requests'] = []
        garment['skus'] = {}
        garment['name'] = self.product_name(response)
        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = self.product_image_urls(response)
        garment['features'] = self.product_features(response)
        color_urls = response.css('li.attribute:first-child a::attr(href)').extract()
        garment['requests'] += self.color_request(response,garment, color_urls)
        return self.request_or_garment(garment)

    def color_request(self,response, garment, color_urls):
        sizes = response.css('.selectable.variation-group-value a::attr(href)').extract()
        if sizes:
            return self.product_requests(urls=color_urls, callback_=self.parse_size, garment=garment)
        else:
            return self.product_requests(urls=color_urls, callback_=self.parse_skus, garment=garment)

    def size_request(self, response):
        size_urls = response.css('.selectable.variation-group-value a::attr(href)').extract()
        return self.product_requests(urls=size_urls, callback_=self.parse_skus, garment=response.meta['garment'])

    def parse_size(self, response):
        response.meta['garment']['requests'] += self.size_request(response)
        return self.request_or_garment(response.meta['garment'])

    def parse_skus(self, response):
        selected_color = response.css('ul.swatches.swatchcolour .selected-value::text').extract_first().strip()
        selected_size = response.css('ul.swatches.size .selected-value::text').extract_first()
        price = response.css('.product-price .price-standard::text').extract_first().strip()
        if selected_size:
            sku_id = selected_color + "_" + selected_size
        else:
            sku_id = selected_color
        response.meta['garment']['skus'][sku_id] = {
            'size': selected_size,
            'color': selected_color,
            'price': price
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

    def product_requests(self, urls, callback_, garment):
        requests = []
        for url in urls:
            requests.append(Request(url=url, callback=callback_, meta={'garment': garment}))
        return requests
