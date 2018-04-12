import json
import re
from collections import OrderedDict
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from fatface_scrapy.items import Product


class FatFaceSpider(CrawlSpider):

    name = "fatface"
    allowed_domains = ['fatface.com', 'i1.adis.ws']
    start_urls = ['https://www.fatface.com']

    blogs = 'blog'
    competition = 'competition'

    required_categories = "a.b-main-menu__link"
    required_products = "a.b-product-image__link, a.b-product-name__link"

    genders = OrderedDict([
        (u'girls', 'girls'),
        (u'boys', 'boys'),
        (u'women', 'women'),
        (u'men', 'men'),
        (u'kids', 'unisex-kids')
    ])

    rules = (
        Rule(LinkExtractor(
            restrict_css=required_categories,
            deny=[blogs, competition]),
             callback='parse_all_products_page',
             follow=True
            ),
        Rule(LinkExtractor(
            restrict_css=required_products,
            deny=[blogs, competition]),
             callback='parse_product'
            ),
    )

    def parse_all_products_page(self, response):
        total_products = response.css('div.b-products-counter::text').re_first(r'(\d+) ')

        if not total_products:
            return

        products_left = int(total_products)
        products_without_pagination = 24
        limit = 99
        starting = 0

        if products_left <= products_without_pagination:
            return

        while products_left > limit:
            max_products_url = response.urljoin('?sz={}&start={}'.format(limit, starting))
            yield Request(max_products_url, callback=self.parse)
            products_left -= limit
            starting += limit

        products_list_url = response.urljoin('?sz={}&start={}'.format(products_left, starting))
        yield Request(products_list_url, callback=self.parse)

    def parse_product(self, response):

        product = Product()
        product['retailer_sku'] = self.get_retailer_sku(response)
        product['category'] = self.get_category(response)
        product['gender'] = self.get_gender(product['category'])
        product['brand'] = self.get_brand()
        product['url'] = response.url.split('?')[0]
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = self.get_care(response)
        product['skus'] = self.get_skus(response)
        product['image_urls'] = []

        images_containers = [self.get_images_link(response)]
        next_colors = response.css('a.b-variation__link.color::attr(href)').extract()

        if next_colors:
            yield Request(next_colors.pop(0),
                          callback=self.parse_skus,
                          meta={'product': product,
                                'next': next_colors,
                                'images': images_containers})
        else:
            yield Request(images_containers.pop(0),
                          callback=self.parse_images,
                          meta={'product': product,
                                'images': images_containers})

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'] += self.get_skus(response)

        next_colors = response.meta['next']
        images_containers = response.meta['images'] + [self.get_images_link(response)]

        if next_colors:
            yield Request(next_colors.pop(0),
                          callback=self.parse_skus,
                          meta={'product': product,
                                'next': next_colors,
                                'images': images_containers})
        else:
            yield Request(images_containers.pop(0),
                          callback=self.parse_images,
                          meta={'product': product,
                                'images': images_containers})

    def parse_images(self, response):
        product = response.meta['product']
        images_containers = response.meta['images']

        images = json.loads(response.text)
        for image in images['items']:
            product['image_urls'].append(image['src'])

        if images_containers:
            yield Request(images_containers.pop(0),
                          callback=self.parse_images,
                          meta={'product': product,
                                'images': images_containers})
        else:
            yield product

    @staticmethod
    def get_images_link(response):
        return response.css('ul.b-product-preview::attr(data-imageset)').extract_first()

    @staticmethod
    def get_retailer_sku(response):
        retailer_sku = response.css('p.b-content-upc::text').re_first(r'Product code: (\d+)')
        return clean(retailer_sku)

    @staticmethod
    def get_category(response):
        category = clean(response.css('span[itemprop="name"]::text').extract())
        if category[0] == 'Home':
            category = category[1:]
        return category

    def get_gender(self, categories):
        for gender_key in self.genders:
            for category in categories:
                if gender_key in category.lower():
                    return self.genders[gender_key]
        return 'unisex-adults'

    @staticmethod
    def get_brand():
        return 'FatFace'

    @staticmethod
    def get_name(response):
        name = response.css('h1.b-product-title ::text').extract_first()
        return clean(name)

    @staticmethod
    def get_description(response):
        desc = response.css('h2.b-product-short-description::text, '
                            'span.b-product-promo__message::text, p.b-content-longdesc::text, '
                            'div.b-content-bullets ::text').extract()
        return clean(desc)

    @staticmethod
    def get_care(response):
        care = response.css('section.b-content-care li::text').extract()
        return clean(care)

    @staticmethod
    def get_prices(response):
        price = response.css('span.b-price__digit ::text').re(r'(\d+)')
        price = int(float('.'.join(price))*100)
        previous = []
        return price, previous

    @staticmethod
    def get_colour(response):
        colour = response.css('span.b-product-variations__value ::text').extract_first()
        return clean(colour)

    @staticmethod
    def get_currency(response):
        currency = response.css('script ::text').re_first(r'"currencyCode":"(\w+)"')
        return clean(currency)

    def get_skus(self, response):
        sizes = response.css('ul.b-variation__list.size li')
        skus = []
        for size in sizes:
            sku = {}
            sku['price'], sku['previous_prices'] = self.get_prices(response)
            sku['currency'] = self.get_currency(response)
            sku['colour'] = self.get_colour(response)
            sku['size'] = size.css('span::text').extract_first()
            if size.css('.unselectable'):
                sku['out_of_stock'] = True
            sku['sku_id'] = '{}_{}'.format(sku['colour'], sku['size'])
            skus.append(sku)
        return skus


def clean(formatted):
    if not formatted:
        return formatted
    if isinstance(formatted, list):
        cleaned = [re.sub(r'\s+', ' ', each).strip() for each in formatted]
        return list(filter(None, cleaned))
    return re.sub(r'\s+', ' ', formatted).strip()
