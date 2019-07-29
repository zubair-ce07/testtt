import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()
    return ''


class WeItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()


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

    page_urls_template = '{}?sz=9&start={}'
    sku_key_template = '{}_{}'
    listings_css = '.level-top-1'
    categories_css = '.refinement-link'
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=categories_css), callback='load_pages'),
    )

    def load_pages(self, response):
        total_products = response.css('.plp-progress-bar ::attr(max)').get()

        if total_products:
            for products_count in range(0, int(total_products), 30):
                yield response.follow(self.page_urls_template.format(response.url, products_count),
                                      callback=self.extract_products_url)
        else:
            return response.follow(response.url, callback=self.extract_products_url)

    def extract_products_url(self, response):
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
        item['skus'] = {}
        item['requests'] = self.colour_urls(response)

        return self.next_request_or_item(item)

    def parse_sku(self, response):
        item = response.meta['item']
        color = self.product_color(response)
        price = response.css('.pdp-price .price-sales ::attr(data-price)').get()
        previous_price = clean(response.css('.price-standard ::text').get())
        sizes = self.product_sizes(response)

        common_sku = {'color': color,
                      'price': price,
                      'previous_price': previous_price}

        for size in sizes:
            common_sku.update({'size': size})
            item['skus'].update({self.sku_key_template.format(color, size): common_sku.copy()})

        return self.next_request_or_item(item)

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

    def colour_urls(self, response):
        colour_urls = response.css('.swatches color ::attr(href)').getall()
        if not colour_urls:
            colour_selectors = response.css('#va-color')[0]
            colour_urls = colour_selectors.css('option ::attr(value)').getall()

        return [response.follow(color_url, callback=self.parse_sku) for color_url in colour_urls]

    def product_color(self, response):
        color = response.css('.variant-attribute--list.variant-attribute--color span ::text').get()

        if color:
            return clean(re.sub('Farbe', '', color))
        return clean(re.sub('- Ausverkauft', '', response.css('[selected="selected"] ::text').get()))

    def product_sizes(self, response):
        size_selector = response.css('#va-size')[0]
        sizes = size_selector.css('option ::text').getall()[1:]

        return clean([re.sub('- Ausverkauft', '', size) for size in sizes])

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            return request
        item.pop('requests', None)
        return item

