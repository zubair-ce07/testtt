import json

from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameter

from ..items import Product
from ..utils import map_gender, format_price


class ParseSpider():
    ONE_SIZE = 'oneSize'

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
        gender_text = response.css(':contains("Gender :") + span::text, title::text').getall()         
        description = self.get_description(response)
        gender_soup = ' '.join(gender_text + description) 

        return map_gender(gender_soup)

    def get_url(self, response):
        return response.url

    def get_description(self, response):
        return response.css('div.description p::text, div.description div::text').getall()

    def get_name(self, response):
        return response.css('.product_name::text').get()

    def get_image_urls(self, response):
        raw_image = response.css('script').re_first(r'"images":(.*),"index"')
        image_parsed = json.loads(raw_image)
        product_id = list(image_parsed.keys())[0]

        return [product['img'] for product in image_parsed[product_id]]

    def get_availability(self, response):
        availability = response.css('[itemprop="availability"]::attr(value)').get()
        return availability != 'In Stock'

    def get_size(self, response, size_parsed, sku_id, attribute_id):
        raw_sizes = response.css('script').re_first(r"sizeOptionArr = JSON.parse\('(.*)'\);")                                
        sizes = size_parsed['attributes'][attribute_id]['options']

        return [s['label'] for s in sizes if s['products'][0] == sku_id][0] if raw_sizes else self.ONE_SIZE

    def get_colour(self, response):
        return response.css(':contains("Color :") + span::text').get()

    def get_skus(self, response):
        skus = {}                
        colour = self.get_colour(response)        
        common_sku = {'colour': colour} if colour else {} 

        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        raw_price = response.css('script').re_first(r'var spConfig = {(.*);')
        price_parsed = json.loads('{' + raw_price)

        attribute_id = list(price_parsed['attributes'].keys())[0]
        sku_ids = list(price_parsed['optionPrices'].keys())

        for id in sku_ids:
            sku = common_sku.copy()
            sku.update(format_price(
                currency,
                price_parsed['optionPrices'][id]['finalPrice']['amount'],
                price_parsed['optionPrices'][id]['oldPrice']['amount']))
            sku['size'] = self.get_size(response, price_parsed, id, attribute_id)
            skus[f"{sku['colour']}_{sku['size']}" if sku.get('colour') else sku['size']] = sku

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

    custom_settings ={
        'DOWNLOAD_DELAY': 2
    }

    product_parser = ParseSpider()

    url_t = 'https://{application_id}-3.algolianet.com/1/indexes/*/' \
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
        raw_formdata = response.css('script').re_first('window\.algoliaConfig = (.*);</script>')
        raw_category = response.css('body::attr(class)').re_first('categorypath-(.*) category').split('-')
        query = '%20'.join([c.capitalize() for c in raw_category])

        formdata_parsed = json.loads(raw_formdata)
        application_id = formdata_parsed['applicationId']
        formdata = self.formdata.copy()
        params = self.params_t

        url = self.url_t.format(
            application_id=application_id.lower(),
            app_id=application_id,
            api_key=formdata_parsed["apiKey"]
        )

        formdata['requests'][0]['params'] = add_or_replace_parameter(
            params.format(query=query), 'page', 0)

        listings_formdata = {
            'formdata': formdata_parsed,
            'query': query
        }

        yield Request(url, method="POST", body=json.dumps(formdata),
                      meta=listings_formdata, callback=self.parse_pagination)

    def parse_pagination(self, response):
        formdata_parsed = response.meta['formdata']
        application_id = formdata_parsed['applicationId']
        products = json.loads(response.text)
        formdata = self.formdata.copy()
        params = self.params_t

        for page_number in range(1, int(products['results'][0]['nbPages'])+1):
            formdata['requests'][0]['params'] = add_or_replace_parameter(
                params.format(query=response.meta['query']), 'page', page_number)

            yield Request(response.url, method="POST", body=json.dumps(formdata), callback=self.parse_products)

    def parse_products(self, response):
        products = json.loads(response.text)

        for product in products['results'][0]['hits']:
            yield response.follow(product['url'], callback=self.parse_item)

    def parse_item(self, response):
        return self.product_parser.parse_product(response)
