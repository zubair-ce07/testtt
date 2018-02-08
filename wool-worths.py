import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor


class WoolWorths(CrawlSpider):
    name = "wool-worths"
    allowed_domains = ["woolworths.co.za"]
    start_urls = ['http://www.woolworths.co.za']

    rules = (
        Rule(LinkExtractor(restrict_css=(['#main-nav', '.pagination__nav']), deny=('/Food', '/Homeware'))),
        Rule(LinkExtractor(restrict_css=('.product-card__visual')), callback='parse_detail'),
    )

    def parse_detail(self, response):
        data = {
            'currency': self.get_currency(response),
            'price': self.get_price(response),
            'brand': self.get_brand(response),
            'catagory': self.get_category(response),
            'description': self.get_description(response),
            'care': self.get_care(response),
            'name': self.get_name(response),
            'url': self.get_url(response),
            'retailor_sk': self.get_reteilor_sk(response),
            'spider_name': WoolWorths.__name__,
            'retailor': "WoolWorths",
            'crawler_start_time': self.crawler.stats.get_value('start_time'),
        }
        color_urls_data = self.get_color_urls_data(response)
        request_urls = []
        for color_data in color_urls_data:
            color_data = color_data.split(',')
            img_url = self.get_url_for_images(color_data[0], color_data[1], color_data[3])
            request_urls.append(scrapy.Request(url=img_url, callback=self.parse_images))
            item_url = self.get_product_item_url(color_data[0], color_data[1])
            request_urls.append(scrapy.Request(url=item_url, callback=self.parse_item_sizes))
        if len(request_urls):
            request = request_urls.pop(0)
            request.meta['images_url'] = []
            request.meta['skus'] = {}
            request.meta['request_urls'] = request_urls
            request.meta['data'] = data
            yield request

    def parse_images(self, response):
        images_urls = self.get_images_urls(response)
        request_urls = response.meta['request_urls']
        if len(request_urls):
            request = request_urls.pop(0)
            request.meta['images_url'] = response.meta['images_url'] + images_urls
            request.meta['skus'] = response.meta['skus']
            request.meta['request_urls'] = request_urls
            request.meta['data'] = response.meta['data']
            yield request

    def parse_item_sizes(self, response):
        request_urls = response.meta['request_urls']
        color = response.css('input::attr(value)').extract_first()
        sizes = response.css('.product__size-selector a::text').extract()
        size_urls_data = response.css('.product__size-selector a::attr(onclick)').re('\((.+)\)')
        for size_data, size in zip(size_urls_data, sizes):
            size_data = size_data.split(',')
            size_prce_url = self.get_size_price_urls(size_data[0], size_data[1], size_data[2])
            price_request = scrapy.Request(url=size_prce_url, callback=self.parse_size_price)
            price_request.meta['colour'] = color
            price_request.meta['size_skuid'] = size_data[1]
            price_request.meta['size'] = size
            request_urls.append(price_request)
        request = request_urls.pop(0)
        request.meta['images_url'] = response.meta['images_url']
        request.meta['skus'] = response.meta['skus']
        request.meta['request_urls'] = request_urls
        request.meta['data'] = response.meta['data']
        yield request

    def parse_size_price(self, response):
        price = response.css('span[itemprop="price"]::attr(content)').extract_first()
        currency = response.css('span[itemprop="priceCurrency"]::attr(content)').extract_first()
        sku_id = '{}_{}'.format(response.meta['size_skuid'], response.meta['size'])
        sku_data = {
            "size": response.meta['size'],
            "colour": response.meta['colour'],
            "price": price,
            "currency": currency,
        }
        skus = response.meta['skus']
        skus[sku_id] = sku_data
        request_urls = response.meta['request_urls']
        if len(request_urls):
            request = request_urls.pop(0)
            request.meta['images_url'] = response.meta['images_url']
            request.meta['skus'] = skus
            request.meta['request_urls'] = request_urls
            request.meta['data'] = response.meta['data']
            yield request
        else:
            yield {
                "images_url": response.meta['images_url'],
                "skus": skus,
                "product_info": response.meta['data'],
            }

    def get_url_for_images(self, colorSKUId, productId, productPageType):
        productPageType = productPageType.replace("'", "")
        url_template = r'http://www.woolworths.co.za/store/fragments/product-common/ww/image-shots.jsp?' \
                       r'colourSKUId={colour_skuid}&productId={product_id}&productPageType={product_page_type}'
        url = url_template.format(colour_skuid=colorSKUId, product_id=productId, product_page_type=productPageType)
        return url

    def get_product_item_url(self, colorSKUId, productId):
        url_template = r'http://www.woolworths.co.za/store/fragments/product-common/ww/product-item.jsp?' \
                       r'colourSKUId={colour_skuid}&productItemId={product_id}'
        url = url_template.format(colour_skuid=colorSKUId, product_id=productId)
        return url

    def get_size_price_urls(self, colorSKUId, sizeSKUId, productId):
        url_template = r'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp?' \
                       r'productItemId={product_id}&colourSKUId={colour_skuid}&sizeSKUId={size_skuid}'
        url = url_template.format(product_id=productId, colour_skuid=colorSKUId, size_skuid=sizeSKUId)
        return url

    def get_description(self, response):
        return response.css('meta[itemprop="description"]::attr(content)').extract_first()

    def get_name(self, response):
        return response.css('meta[itemprop="name"]::attr(content)').extract_first()

    def get_color_urls_data(self, response):
        return response.css('.nav-list-x--wrap img::attr(onclick)').re('\((.+)\)')

    def get_images_urls(self, response):
        return response.css(
               'div[data-js="pdp-carousel"] a::attr(href),a::attr(data-gallery-full-size)').extract()

    def get_reteilor_sk(self, response):
        return response.css('meta[itemprop="productId"]::attr(content)').extract_first()

    def get_url(self, response):
        return response.css('meta[itemprop="url"]::attr(content)').extract_first()

    def get_brand(self, response):
        return response.css('meta[itemprop="brand"]::attr(content)').extract_first()

    def get_price(self, response):
        return response.css('meta[itemprop="price"]::attr(content)').extract_first()

    def get_currency(self, response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    def get_category(self, response):
        return response.css('.breadcrumb a::text').extract()

    def get_care(self, response):
        return response.css('div[data-js="accordion-content"] img::attr(src)').extract()
