import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class QcrawlSpider(CrawlSpider):
    name = 'hypesp'
    allowed_domains = ['hypedc.com']
    start_urls = ['http://hypedc.com/brands/']

    rules = (
       Rule(LinkExtractor(allow=(), deny=('news')), follow=True, callback='parse_item'),
    )
    def parse_item(self, response):
        if(response.css('p.addtocart')):
            old_price, price = None, None
            is_discounted, currency = "", ""
            item_id = response.css('div.product-code::text').extract_first()
            name = response.css('h1.product-name::text').extract_first()
            brand = response.css('h2.product-manufacturer::text').extract_first()
            description = response.css('div.product-description.std::text').extract_first()
            description = description.strip()       
            image_urls = response.css('div.slider-inner.col-sm-13.col-sm-offset-11 > div.unveil-container > img.img-responsive::attr(data-src)').extract()
            colour_name = response.css('h3.h4.product-colour::attr(data-bf-color)').extract_first()
            
            if response.css('span.label.label-primary.label-tag.label-tag-lg.label-tag-discount'):
                old_price = response.css('[id^=old-pri]::text').extract_first()
                old_price = old_price.strip()
                price = response.css('[id^=product-pri]::text').extract_first()
                price = price.strip()
                currency = price[0]
                is_discounted = "Yes"
            
            else:
                price = response.css('span.price-dollars::text').extract_first() + response.css('span.price-cents::text').extract_first()
                is_discounted = "No"
                old_price = price
                currency = price[0]
                
            item = {
                    'item_id': item_id,
                    'url': response.url,
                    'name': name,
                    'brand': brand,
                    'description': description,
                    'colour_name' : colour_name,
                    'old_price': old_price,
                    'price': price,
                    'is_discounted' : is_discounted,
                    'currency': currency,
                    'image_urls' : image_urls,
                }

            yield item

