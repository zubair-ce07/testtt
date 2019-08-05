import re

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()


class WeItem(Item):
    retailer_sku = Field()
    gender = Field()
    name = Field()
    category = Field()
    url = Field()
    brand = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    requests = Field()


class WeSpider(CrawlSpider):
    name = 'weFashion'
    allowed_domains = ['wefashion.de']
    start_urls = [
        'https://www.wefashion.de/',
    ]

    gender_dict = {'Damen': 'Women',
                   'Herren': 'Men',
                   'Kinder': 'kids'
                   }

    page_urls_t = '{}?sz=9&start={}'
    sku_key_t = '{}_{}'
    listings_css = '.level-top-1'
    categories_css = '.refinement-link'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=categories_css), callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        total_products = response.css('.plp-progress-bar ::attr(max)').get()

        if total_products:
            for products_count in range(0, int(total_products), 30):
                yield response.follow(self.page_urls_t.format(response.url, products_count),
                                      callback=self.parse_products)
        else:
            return response.follow(response.url, callback=self.parse_products)

    def parse_products(self, response):
        return [response.follow(product_url, callback=self.parse_item)
                for product_url in response.css('.name-link ::attr(href)').getall()]

    def parse_item(self, response):
        item = WeItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = self.product_skus(response)

        item['requests'] = self.colour_requests(response)
        return self.next_request_or_item(item)

    def product_skus(self, response):
        color = self.product_color(response)
        price = response.css('.pdp-price .price-sales ::attr(data-price)').get()
        previous_price = clean(response.css('.price-standard ::text').get())
        sizes = self.product_sizes(response)

        common_sku = {'color': color,
                      'price': price,
                      'previous_price': previous_price}

        skus = {}
        for size in sizes:
            out_of_stock, size = self.check_stock_status(size)
            common_sku.update({
                'out_of_stock': out_of_stock,
                'size': size,

            })
            skus[self.sku_key_t.format(color, size)] = common_sku.copy()

        return skus

    def product_color(self, response):
        color = response.css('.variant-attribute--color span ::text').get()
        return clean(re.sub('Farbe:|\s+', '', color))

    def product_sizes(self, response):
        size_sel = response.css('#va-size')[0]
        sizes = size_sel.css('option ::text').getall()[1:]
        return clean([size for size in sizes])

    def colour_requests(self, response):
        colour_urls = response.css('.color .emptyswatch ::attr(href)').getall()
        return [response.follow(color_url, callback=self.parse_color) for color_url in colour_urls]

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.images_url(response))
        item['skus'].update(self.product_skus(response))

        return self.next_request_or_item(item)

    def check_stock_status(self, size):
        if 'Ausverkauft' in size:
            return True, re.sub('- Ausverkauft', '', size)
        return False, size

    def retailer_sku(self, response):
        return response.css('.variation-select ::attr(data-product-id)').get()

    def product_gender(self, response):
        return self.gender_dict.get(response.css('.breadcrumb span::text').getall()[1])

    def product_name(self, response):
        return response.css('.breadcrumb span::text').getall()[-1]

    def product_category(self, response):
        return response.css('[itemprop="itemListElement"] span ::text').getall()[1:]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('#productEcommerceObject ::attr(value)').re_first('\"brand\":\"(.+?)\"')

    def product_description(self, response):
        return clean(response.css('[itemprop="description"] span ::text').getall())

    def product_care(self, response):
        return [response.css('.washingInstructions ::text').get()]

    def images_url(self, response):
        return response.css('.pdp-figure__image ::attr(data-image-replacement)').getall()

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            return request

        item.pop('requests', None)
        return item

