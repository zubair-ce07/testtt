import scrapy
from item import Product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import copy


class OrsaySpider(CrawlSpider):
    name = 'OrsaySpider'
    allowed_domains = ['www.orsay.com']
    start_urls = ['http://www.orsay.com/de-de/collection.html']
    rules = (
        Rule(LinkExtractor(restrict_css='a.i-next')),
        Rule(LinkExtractor(restrict_css='div.product-image-wrapper>a'), callback='parse_product'),
    )

    def parse_product(self, response):

        skus = {}
        care = get_care(response)
        brand = 'Orsay'
        description = get_description(response)
        url = response.request.url
        gender = 'Women'
        image_urls = get_image_urls(response)
        retailer_sku = get_retailer_sku(response)
        name = get_name(response)
        colors_links = get_color_links(response, url)
        color_titles = get_color_title(response)
        next_color_request = response.urljoin(colors_links.pop())
        next_color_request = scrapy.Request(next_color_request, callback=self.parse_colors, dont_filter=True)
        product = Product(care=care, url=url, gender=gender, name=name, retailer_sku=retailer_sku, brand=brand,
                          description=description, image_urls=image_urls, skus=skus)

        next_color_request.meta['product'] = product
        next_color_request.meta['colors_links'] = colors_links
        next_color_request.meta['color_titles'] = color_titles

        yield next_color_request

    def parse_colors(self, response):

        colors_links = response.meta['colors_links']
        color_titles = response.meta['color_titles']
        product = response.meta['product']

        product = get_color_sku(product, color_titles, response)

        if len(colors_links) > 0:

            next_color_request = response.urljoin(colors_links.pop())
            response.meta['colors_links'] = colors_links
            response.meta['color_titles'] = color_titles
            response.meta['product'] = product
            yield Request(next_color_request, callback=self.parse_colors, meta=response.meta, dont_filter=True)

        else:
            yield product


def get_care(response):
    return response.css('ul[class=caresymbols]').css('img::attr(src)').extract()


def get_description(response):
    return response.css('div.short-description::text').extract()


def get_image_urls(response):
    return response.css('div.product-image-gallery-thumbs').css('img::attr(src)').extract()


def get_retailer_sku(response):
    return response.css('ul[class=caresymbols]').css('img::attr(src)').extract()


def get_name(response):
    return response.css('h1.product-name::text').extract_first()


def get_color_links(response,url):
    color_links = response.css('div.related-products').css('a::attr(href)').extract()
    color_links[0] = url
    return color_links


def get_color_title(response):
    return response.css('div.related-products').css('img::attr(title)').extract()


def get_sizes(response):
    sizes = response.css('div.sizebox-wrapper').css('li::text').extract()
    sizes = [x.strip() for x in sizes]
    sizes = filter(None, sizes)
    return sizes


def get_color_retailer_sku(response):
    return response.css('input[id=sku]::attr(value)').extract_first()


def get_price_and_currency(response):
    pc = response.css('span.price::text').extract_first().split()
    if pc[1] == u'\u20ac':
        pc[1] = 'Euro'
    return pc


def get_quantity(response):
    return response.css('div.sizebox-wrapper').css('li::attr(data-qty)').extract()


def get_color_sku(product, color_titles, response):
    skus = copy.deepcopy(product['skus'])

    temp_retailer_sku = get_color_retailer_sku(response)
    sizes = get_sizes(response)
    price_and_currency = get_price_and_currency(response)
    price = price_and_currency[0]
    currency = price_and_currency[1]
    quantity = get_quantity(response)

    color = color_titles.pop()
    itera = 0
    for size in sizes:
        out_of_stock = True
        if int(quantity[itera]) > 0:
            out_of_stock = False

        skus[temp_retailer_sku + "_" + size] = {"size": size, 'price': price, 'currency': currency,
                                                'out_of_stock': out_of_stock, 'color': color}
        itera += 1

    product['skus'] = copy.deepcopy(skus)
    return product