import json

from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameter

from ..items import Product
from ..utils import map_gender, format_price


class ParseSpider():
    one_size = 'One Size'

    def parse_product(self, response):
        product = Product()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = []
        product['skus'] = self.get_skus(response)
        product['out_of_stock'] = self.get_availability(response)
        product['image_urls'] = self.get_image_urls(response)
        product['requests'] = self.color_requests(response)

        return self.request_or_product(product)

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'].update(self.get_skus(response))
        return self.request_or_product(product)

    def get_retailer_sku(self, response):
        return response.css('#product-sku::attr(value)').get()

    def get_brand(self, response):
        return response.css('span.brand_name::text').get()

    def get_category(self, response):
        return response.css('.cms_page::text').getall()

    def get_gender(self, response):
        raw_gender = response.css(':contains("Gender :") + span::text, title::text').getall()
        soup = ' '.join(raw_gender + self.get_description(response))
        return map_gender(soup)

    def get_url(self, response):
        return response.url

    def get_description(self, response):
        return response.css('div.description p::text, div.description div::text').getall()

    def get_name(self, response):
        return response.css('.product_name::text').get()

    def get_image_urls(self, response):
        css = 'script:contains("Magento_Catalog/js/product")'
        raw_images = response.css(css).re_first(r'"images":(.*\]),"url"')
        return [i['url'] for i in json.loads(raw_images)]

    def get_availability(self, response):
        availability = response.css('[itemprop="availability"]::attr(value)').get()
        return availability != 'In Stock'

    def get_price(self, raw_sku, sku_id):
        return format_price(
            raw_sku['currencyFormat'].split()[0],
            raw_sku['optionPrices'][sku_id]['finalPrice']['amount'],
            raw_sku['optionPrices'][sku_id]['oldPrice']['amount']
        )

    def get_sizes(self, raw_sku):
        sizes_map = {}
        attribute_id = list(raw_sku['attributes'].keys())[0]
        sizes = raw_sku['attributes'][attribute_id]['options']

        for size in sizes:
            sizes_map[size['products'][0]] = size['label']

        return sizes_map

    def get_skus(self, response):
        skus = {}
        colour = response.css(':contains("Color :") + span::text').get()
        common_sku = {'colour': colour} if colour else {}

        sku_css = 'script:contains("optionPrices")'
        raw_sku = json.loads(response.css(sku_css).re_first(r'var spConfig = ({.*);'))

        css = 'script:contains("sizeOptionArr")'
        raw_sizes = response.css(css).re_first(r"sizeOptionArr = JSON.parse\('(.*)'\);")
        sizes = self.get_sizes(raw_sku) if raw_sizes else {}

        for sku_id in list(raw_sku['optionPrices'].keys()):
            sku = common_sku.copy()
            sku.update(self.get_price(raw_sku, sku_id))
            sku['size'] = sizes.get(sku_id) or self.one_size
            skus[f"{sku['colour']}_{sku['size']}" if colour else sku['size']] = sku

        return skus

    def color_requests(self, response):
        color_urls = response.css('.plus_color_box a::attr(href)').getall()
        return [response.follow(url, callback=self.parse_skus) for url in color_urls]

    def request_or_product(self, product):
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product


class CrawlSpider(CrawlSpider):
    name = 'sixthstreet_spider'
    allowed_domains = ['en-ae.6thstreet.com', 'algolianet.com']
    start_urls = ['https://en-ae.6thstreet.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    product_parser = ParseSpider()

    api_url_t = 'https://{application_id}-3.algolianet.com/1/indexes/*/' \
                'queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.27.0%3Binstantsearch.js' \
                '%202.10.2%3BMagento2%20integration%20(1.10.0)%3BJS%20Helper%202.26.0&' \
                'x-algolia-application-id={app_id}&x-algolia-api-key={api_key}'

    params_t = "query={query}&hitsPerPage=60&maxValuesPerFacet=60"
    formdata = {
        "requests": [
            {
                "indexName": "enterprise_magento_english_products",
                "params": ''
            }
        ]
    }

    listings_css = 'li.second-sub'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_listings'),
    )

    def parse_listings(self, response):
        raw_formdata = response.css('script:contains("apiKey")').re_first('window\.algoliaConfig = (.*);</script>')
        raw_category = response.css('body::attr(class)').re_first('categorypath-(.*) category').split('-')
        query = '%20'.join([c.capitalize() for c in raw_category])

        payload = json.loads(raw_formdata)
        application_id = payload['applicationId']
        formdata = self.formdata.copy()

        category_url = self.api_url_t.format(
            application_id=application_id.lower(),
            app_id=application_id,
            api_key=payload["apiKey"]
        )

        formdata['requests'][0]['params'] = add_or_replace_parameter(self.params_t.format(query=query), 'page', 0)

        yield Request(category_url, method="POST", body=json.dumps(formdata),
                      meta={'query': query}, callback=self.parse_pagination)

    def parse_pagination(self, response):
        formdata = self.formdata.copy()

        for page_number in range(1, int(json.loads(response.text)['results'][0]['nbPages']) + 1):
            formdata['requests'][0]['params'] = add_or_replace_parameter(
                self.params_t.format(query=response.meta['query']), 'page', page_number)

            yield Request(response.url, method="POST", body=json.dumps(formdata), callback=self.parse_products)

    def parse_products(self, response):
        return [response.follow(p['url'], callback=self.parse_item)
                for p in json.loads(response.text)['results'][0]['hits']]

    def parse_item(self, response):
        return self.product_parser.parse_product(response)
