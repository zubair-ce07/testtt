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

    # def start_requests(self):
    #     (yield Request(
    #         url= 'http://www.orsay.com/de-de/t-shirt-mit-details-15009697.html',
    #         callback=self.parse_product
    #     )
    # )

    def parse_product(self, response):

        care = response.css('ul[class=caresymbols]').css('img::attr(src)').extract()
        brand = 'Orsay'
        description = response.css('div.short-description::text').extract()
        url = response.request.url
        gender = 'Women'
        image_urls = response.css('div.product-image-gallery-thumbs').css('img::attr(src)').extract()
        retailer_sku = response.css('input[id=sku]::attr(value)').extract_first()
        name = response.css('h1.product-name::text').extract_first()

        colors_links = response.css('div.related-products').css('a::attr(href)').extract()
        colors_links[0] = url
        color_titles = response.css('div.related-products').css('img::attr(title)').extract()

        skus = {}
        next_color = response.urljoin(colors_links.pop())
        next_color = scrapy.Request(next_color, callback=self.parse_colors, dont_filter= True )

        next_color.meta['colors_links'] = colors_links
        next_color.meta['color_titles'] = color_titles

        product = Product(care=care, url=url, gender=gender, name=name, retailer_sku=retailer_sku, brand=brand,
                          description=description, image_urls=image_urls, skus=skus)
        next_color.meta['product'] = product

        yield next_color


    def parse_colors(self, response):

        colors_links = response.meta['colors_links']
        color_titles = response.meta['color_titles']

        product = response.meta['product']

        skus = copy.deepcopy(product['skus'])
        temp_retailer_sku = response.css('input[id=sku]::attr(value)').extract_first()
        sizes = response.css('div.sizebox-wrapper').css('li::text').extract()
        sizes = [x.strip() for x in sizes]
        sizes = filter(None, sizes)
        price_and_currency = response.css('span.price::text').extract_first().split()
        price = price_and_currency[0]
        quantity = response.css('div.sizebox-wrapper').css('li::attr(data-qty)').extract()

        if price_and_currency[1] == u'\u20ac':
            currency = 'Euro'
        else:
            currency = price_and_currency[1]

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

        if len(colors_links) > 0:

            # print("asdadasd")
            next_color = response.urljoin(colors_links.pop())
            response.meta['colors_links'] = colors_links
            response.meta['color_titles'] = color_titles
            response.meta['product'] = product
            yield Request(next_color, callback=self.parse_colors, meta=response.meta, dont_filter=True)


        else:
            yield product