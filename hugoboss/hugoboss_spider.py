import scrapy
import json
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from items import HugoBossItem


class MySpider(CrawlSpider):
    name = 'hugoboss'
    allowed_domains = ['hugoboss.com']
    start_urls = ['https://www.hugoboss.com/uk/']
    restricted_css = ['ul.nav-list--third-level', 'li.pagingbar__item--arrow']

    DOWNLOAD_DELAY = 0.2

    rules = (
        Rule(LinkExtractor(restrict_css=restricted_css, deny=('/inspiration/'))),
        Rule(LinkExtractor(restrict_css=('div.product-tile__product-name')), callback='parse_item'),
    )

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

        color_links = response.css('div.swatch-list__button--is-empty a::attr(href)').extract()

        if color_links:
            yield response.follow(color_links.pop(), callback=self._extract_colors,\
                                 meta={'item': item, 'color_links': color_links})
        else:
            yield item     

    def _extract_colors(self, response):
        print("Extracting color:", response.url)
        item = response.meta.get('item')
        color_links = response.meta.get('color_links')

        item['image_urls'] += self._extract_image_urls(response)
        item['skus'] += self._extract_skus(response)

        if color_links:
            yield response.follow(color_links.pop(), callback=self._extract_colors,\
                                 meta={'item': item, 'color_links': color_links})
        else:
            yield item

    
    def _extract_json(self, json_str):
        return json.loads(json_str)
    
    def _extract_care(self, response):
        care = response.css('svg.accordion__item__icon title::text').extract()

        return list(map(str.strip, care))

    def _extract_description(self, response):
        description = response.css('div.product-container__text__description::text').\
                                    extract_first()
        if description:
            return list(map(str.strip, description.strip().split(".")))

        return []
    
    def _extract_image_urls(self, response):
        img_urls = response.css('img.slider-item__image::attr(src)').extract()[:-1]

        return list(map(lambda c: c.replace('wid=70&hei=106', 'wid=461&hei=698'), img_urls))


    def _extract_skus(self, response):
        color, currency, price, previous_price = self._extract_sku_static_attrs(response)
        
        skus = []
        size_selectors = response.css('a.product-stage__choose-size__select-size')
        for sku in size_selectors:
            sku_item = {}
            sku_item['color'] = color
            sku_item['price'] = price
            sku_item['currency'] = currency
            sku_item['size'] = sku.css('a::attr(title)').extract_first()

            if previous_price:
                sku_item['previous_price'] = previous_price.strip()[1:]
            
            if sku.css('a::attr(disabled)').extract_first():
                sku_item['out_of_stock'] = True
            
            if not sku_item['size']:
                sku_item['size'] = 'ONE SIZE'

            sku_item['id'] = '{}_{}'.format(color, sku_item['size'])

            skus.append(sku_item)

        return skus

    def _extract_sku_static_attrs(self, response):
        data_current = response.css('div.product-variations::attr(data-current)').extract_first()
        data_current = self._extract_json(data_current)

        color = data_current['color']['displayValue']
        currency = response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()
        price = response.xpath('//meta[@itemprop="price"]/@content').extract_first()
        previous_price = response.css('span.product-price--price-standard s::text').extract_first()

        return color, currency, price, previous_price
