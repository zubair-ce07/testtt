import scrapy
import json
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from items import HugoBossItem

class MySpider(CrawlSpider):
    name = 'hugoboss'
    allowed_domains = ['hugoboss.com']
    start_urls = ['https://www.hugoboss.com/uk/slim-fit-graph-check-suit-in-yarn-dyed-virgin-wool/hbeu50384104_461.html?cgid=21100#start=1']

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    # )
    def parse_start_url(self, response):
        self.parse_item(response)

    def parse_item(self, response):
        item = HugoBossItem()

        script = response.xpath('//script[contains(., "productCurrency")]').extract_first()
        prod_details = re.search(r"({.*?})", script).group(1)
        prod_details = self._extract_json(prod_details)

        item['retailer_sku'] = prod_details['productID']
        item['gender'] = prod_details['productGender']
        item['category'] = prod_details['productCategory']
        item['brand'] = prod_details['productBrand']
        item['url'] = response.url
        item['name'] = prod_details['productName']
        item["description"] = self._extract_description(response)
        item['care'] = self._extract_care(response)
        item['image_urls'] = self._extract_image_urls(response)
        item['skus'] = self._extract_skus(response)
        
        print(item) 
    
    def _extract_json(self, json_str):
        return json.loads(json_str)
    
    def _extract_care(self, response):
        care = response.css('svg.accordion__item__icon title::text').extract()

        return list(map(str.strip, care))

    def _extract_description(self, response):
        description = response.css('div.product-container__text__description::text').\
                                    extract_first().strip().split('.')

        return list(map(str.strip, description))
    
    def _extract_image_urls(self, response):
        img_urls = response.css('img.slider-item__image::attr(src)').extract()[:-1]

        return list(map(lambda c: c.replace('wid=70&hei=106', 'wid=461&hei=698'), img_urls))


    def _extract_skus(self, response):
        color, currency, price, previous_price = self._extract_sku_static_attr(response)
        
        skus = []
        size_selectors = response.css('a.product-stage__choose-size__select-size')
        for sku in size_selectors:
            sku_item = {}
            sku_item['color'] = color
            sku_item['price'] = price
            sku_item['currency'] = currency
            sku_item['size'] = sku.css('a::attr(title)').extract_first()
            sku_item['id'] = '{}_{}'.format(color, sku_item['size'])

            if previous_price:
                sku_item['previous_price'] = previous_price.strip()[1:]
            
            if sku.css('a::attr(disabled)').extract_first():
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus

    def _extract_sku_static_attr(self, response):
        data_current = response.css('div.product-variations::attr(data-current)').extract_first()
        data_current = self._extract_json(data_current)

        color = data_current['color']['displayValue']
        currency = response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()
        price = response.xpath('//meta[@itemprop="price"]/@content').extract_first()
        previous_price = response.css('span.product-price--price-standard s::text').extract_first()

        return color, currency, price, previous_price
