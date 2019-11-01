import json
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

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
        product['image_urls'] = self.get_image_urls(response)

        return product 
     
    def get_retailer_sku(self, response):        
        return response.css('#product-sku::attr(value)').get()

    def get_brand(self, response):        
        return response.css('span.brand_name::text').get()

    def get_category(self, response):         
        return response.css('.cms_page::text').getall()

    def get_gender(self, response):
        xpath = '//span[contains(text(), "Gender")]/following-sibling::span/text()'
        gender = response.xpath(xpath).get()

        title_text = response.css('title::text').get()    
        description = self.get_description(response)

        raw_gender = f"{gender} {title_text} {' '.join(description)}" 

        return map_gender(raw_gender)

    def get_url(self, response):
        return response.url

    def get_description(self, response):                
        return response.css('div.description p::text').getall()

    def get_name(self, response):        
        return response.css('.product_name::text').get()

    def get_image_urls(self, response):
        image_raw = response.css('script').re_first(r'"images":(.*),"index"')
        image_parsed = json.loads(image_raw)
        product_id = list(image_parsed.keys())[0]
        
        return [product['img'] for product in image_parsed[product_id]]

    def get_availability(self, response):
        availability = response.css('[itemprop="availability"]::attr(value)').get()

        return availability != 'In Stock'

    def get_sizes(self, response):
        sizes_raw = response.css('script').re_first(r"sizeOptionArr = JSON.parse\('(.*)'\);")
        sizes_parsed = json.loads(sizes_raw) if sizes_raw else []
        sizes = [size['UK'] for size in sizes_parsed]
        
        return sizes if sizes else [self.ONE_SIZE]       

    def get_price(self, response):
        current_price = response.css('[itemprop="price"]::attr(content)').get()
        previous_price = response.css('.old-price span::attr(data-price-amount)').get()

        return format_price(previous_price, current_price)
                            
    def get_skus(self, response):
        skus = {}

        colour_xpath = '//span[contains(text(),"Color")]/following-sibling::span/text()'
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        
        for colour in response.xpath(colour_xpath).getall():
            for size in self.get_sizes(response):
                sku_attributes = {}
                sku_attributes.update(self.get_price(response))                
                sku_attributes['currency'] = currency 
                sku_attributes['colour'] = colour
                sku_attributes['size'] = size
                sku_attributes['out_of_stock'] = self.get_availability(response)

                skus[f'{colour}_{size}'] = sku_attributes
                            
        return skus


class CrawlSpider(CrawlSpider):
    name = 'sixthstreet_spider'
    allowed_domains = ['en-ae.6thstreet.com', 'algolianet.com']
    start_urls = ['https://en-ae.6thstreet.com']

    listings_css = 'li.second-sub'
    products_css = 'ais-hits--item'    

    product_parser = ParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_listings'),
    )   
    
    def parse_listings(self, response):
        formdata_raw = response.css('script').re_first('window\.algoliaConfig = (.*);</script>')
        category_raw = response.css('body::attr(class)').re_first('categorypath-(.*) category')

        query_raw = list(map(lambda category: category.capitalize(), category_raw))
        query = '%20'.join(query_raw)
        
        formdata_parsed = json.loads(formdata_raw)
        application_id = formdata_parsed['applicationId']    
              
        url = f'https://{application_id.lower()}-3.algolianet.com/1/indexes/*/' \
            'queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.27.0%3Binstantsearch.js' \
            '%202.10.2%3BMagento2%20integration%20(1.10.0)%3BJS%20Helper%202.26.0&' \
            f'x-algolia-application-id={application_id}&x-algolia-api-key={formdata_parsed["apiKey"]}'
        
        formdata = {
            "requests":[
                {
                "indexName": "enterprise_magento_english_products",
                "params": f"query={query}&hitsPerPage=60&maxValuesPerFacet=60&page=0"
                }
            ]
        }
            
        yield Request(url, method="POST", body=json.dumps(formdata), meta={'listings':response}, callback=self.parse_pagination)

    def parse_pagination(self, response):
        listings_response = response.meta['listings']

        formdata_raw = listings_response.css('script').re_first('window\.algoliaConfig = (.*);</script>')
        category_raw = listings_response.css('body::attr(class)').re_first('categorypath-(.*) category')

        query_raw = list(map(lambda category: category.capitalize(), category_raw))
        query = '%20'.join(query_raw)
        
        formdata_parsed = json.loads(formdata_raw)
        application_id = formdata_parsed['applicationId']
        products = json.loads(response.body_as_unicode()) 
        page_number = 0   
              
        url = f'https://{application_id.lower()}-3.algolianet.com/1/indexes/*/' \
            'queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.27.0%3Binstantsearch.js' \
            '%202.10.2%3BMagento2%20integration%20(1.10.0)%3BJS%20Helper%202.26.0&' \
            f'x-algolia-application-id={application_id}&x-algolia-api-key={formdata_parsed["apiKey"]}'

        while page_number <= int(products['results'][0]['nbPages']):
            formdata = {
                "requests":[
                    {
                    "indexName": "enterprise_magento_english_products",
                    "params": f"query={query}&hitsPerPage=60&maxValuesPerFacet=60&page={page_number}"
                    }
                ]
            }

            page_number += 1    

            yield Request(url, method="POST", body=json.dumps(formdata), callback=self.parse_urls)
        
    def parse_urls(self, response):
        products = json.loads(response.body_as_unicode())

        urls = [product['url'] for product in products['results'][0]['hits']]
       
        for url in urls:
            yield response.follow(url, callback=self.product_parser.parse_product)
