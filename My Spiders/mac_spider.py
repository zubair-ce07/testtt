from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import FormRequest

from ..items import Product
from ..utils import map_gender, format_price


class Mixin:
    retailer = 'mac'


class MixinAT(Mixin):
    retailer = Mixin.retailer + '-at'

    allowed_domains = ['mac-jeans.com']
    start_urls = ['https://mac-jeans.com/at-de/csrftoken']
    retailer_url = 'https://mac-jeans.com/at-de'

    default_brand = 'Mac'
    one_size = 'One Size'
    one_sizes = ['OS']


class MacParseSpider(MixinAT):
    csrf_token = None
    
    def parse_product(self, response):
        product = Product()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = self.get_care(response)
        product['skus'] = {}
        product['image_urls'] = self.get_image_urls(response)
        product['trail'] = add_trail(response)
        product['meta'] = {'requests': self.color_requests(response)}

        return self.request_or_product(product)

    def parse_colours(self, response):
        product = response.meta['product']
        product['meta']['requests'] += self.sku_requests(response)
        return self.request_or_product(product)

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'].update(self.get_skus(response))
        return self.request_or_product(product)

    def get_retailer_sku(self, response):
        return response.css('[itemprop="sku"]::text').getall()[1].strip()

    def get_brand(self, response):
        return response.css('[itemprop="brand"]::attr(content)').get() or self.default_brand

    def get_gender(self, response):
        title_text = response.css('title::text').get()
        categories = self.get_category(response)
        description = self.get_description(response)
        gender_soup = ' '.join(categories + description) + title_text

        return map_gender(gender_soup)

    def get_care(self, response):
        care_s = response.css('.product-links li::attr(data-content)').get()
        selector = Selector(text=care_s)
        return [care.strip() for care in selector.css('td div::text').getall()]

    def get_category(self, response):
        return response.css('.breadcrumb--list [itemprop="name"]::text').getall()

    def get_description(self, response):
        return response.css('[itemprop="description"] li::text').getall()

    def get_url(self, response):
        return response.url

    def get_name(self, response):
        return response.css('.product--title::text').get().strip()

    def get_image_urls(self, response):
        return response.css('.image-slider--container [itemprop="image"]::attr(srcset)').getall()

    def get_skus(self, response):
        colour = response.css('.color-images--article-switcher .selected--option a::attr(title)').get()
        size = response.css('[checked="checked"] + [for="group[1]"]::text').get().strip()
        len = response.css('[checked="checked"] + [for="group[2]"]::text').get().strip()

        sku = {'colour': colour} if colour else {}
        sku.update(self.get_price(response))
        sku['size'] = self.one_size if size in self.one_sizes else f"{size}_{len}"
        sku['out_of_stock'] = bool(response.css('#notifyHideBasket'))

        return {f"{sku['colour']}_{sku['size']}" if colour else sku['size']: sku}

    def get_price(self, response):
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_price = response.css('.content--discount span::text').re_first(r'EUR\xa0(.*)')
        previous_price = previous_price.split(',') if previous_price else []
        current_price = response.css('[itemprop="price"]::attr(content)').get()

        return format_price(currency, current_price, '.'.join(previous_price))

    def color_requests(self, response):
        color_urls = response.css('.color-images--article-switcher a::attr(href)').getall()
        return [response.follow(url, callback=self.parse_colours, dont_filter=True) for url in color_urls]

    def sku_requests(self, response):
        sku_requests = []
        size_ids = response.css('div:not(.is--disabled)>[name="group[1]"]::attr(value)').getall()
        length_ids = response.css('div:not(.is--disabled)>[name="group[2]"]::attr(value)').getall()

        for size_id in size_ids:
            for length_id in length_ids:
                formdata = {
                    "group[1]": size_id,
                    "group[2]": length_id,
                    "__csrf_token": self.csrf_token
                }

                sku_requests.append(FormRequest(url=response.url, formdata=formdata,
                                                callback=self.parse_skus, dont_filter=True))

        return sku_requests

    def request_or_product(self, product):
        if product['meta']['requests']:
            request = product['meta']['requests'].pop()
            request.meta['product'] = product
            request.cookies = {'__csrf_token-3': self.csrf_token}
            return request
        else:
            del product['meta']

        return product


def add_trail(response):
    trail = [(response.meta.get('link_text', ''), response.url)]
    return response.meta.get('trail', []) + trail


class MacCrawlSpider(Spider):

    product_parser = MacParseSpider()

    def parse(self, response):
        self.product_parser.csrf_token = response.headers['X-Csrf-Token'].decode('utf-8')
        return response.follow(self.retailer_url, callback=self.parse_category,
                               meta=add_trail(response))

    def parse_category(self, response):
        urls = response.css('.navigation--link:contains("men")::attr(href)').getall()
        trail = add_trail(response)
        return [response.follow(url, callback=self.parse_subcategory, meta={'trail': trail})
                for url in urls]

    def parse_subcategory(self, response):
        category_urls = response.css('div.sidebar--categories-navigation a::attr(href)').getall()[:-2]
        trail = add_trail(response)
        return [response.follow(url, callback=self.parse_pagination, meta={'trail': trail})
                for url in category_urls]

    def parse_pagination(self, response):
        total_pages = response.css('.paging--display strong::text').get()
        trail = add_trail(response)
        if total_pages:
            return [response.follow(f'{response.url}?p={p}', callback=self.parse_listings,
                                    meta={'trail': trail}) for p in range(1, int(total_pages)+1)]

        return response.follow(response.url, callback=self.parse_listings)

    def parse_listings(self, response):
        product_urls = response.css('.product--info a::attr(href)').getall()
        trail = add_trail(response)
        return [response.follow(url, callback=self.parse_item,
                                meta={'trail': trail}) for url in product_urls]

    def parse_item(self, response):
        return self.product_parser.parse_product(response)


class MacATcrawlSpider(MacCrawlSpider, MixinAT):
    name = MixinAT.retailer + '-crawl'


class MacATparseSpider(MacParseSpider, MixinAT):
    name = MixinAT.retailer + '-parse'
