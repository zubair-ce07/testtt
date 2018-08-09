import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import HugoBossItem


class HugoBossSpider(CrawlSpider):
    name = 'hugoboss'
    allowed_domains = ['hugoboss.com']
    start_urls = ['https://www.hugoboss.com/uk/']

    DOWNLOAD_DELAY = 0.5

    listing_css = ['.nav-list--third-level', '.pagingbar__item--arrow']
    product_sel = '.product-tile__product-name'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=('/inspiration/'))),
        Rule(LinkExtractor(restrict_css=product_sel), callback='parse_item'),
    )

    def parse_item(self, response):
        raw_product = self._extract_raw_product(response)

        item = HugoBossItem()
        item['retailer_sku'] = raw_product['productID']
        item['gender'] = raw_product['productGender']
        item['category'] = raw_product['productCategory']
        item['brand'] = raw_product['productBrand']
        item['name'] = raw_product['productName']
        item['url'] = response.url
        item["description"] = self._extract_description(response)
        item['care'] = self._extract_care(response)
        item['image_urls'] = self._extract_image_urls(response)
        item['skus'] = self._extract_skus(response)

        color_links = response.css('.swatch-list__button--is-empty a::attr(href)').extract()
        return  self._process_colors(response, color_links, item)

    def _process_colors(self, response, color_links, item):
        if color_links:
            return response.follow(color_links.pop(), callback=self._extract_color,\
                                  meta={'item': item, 'color_links': color_links})
        return item

    def _extract_color(self, response):
        item = response.meta.get('item')
        color_links = response.meta.get('color_links')

        item['image_urls'] += self._extract_image_urls(response)
        item['skus'] += self._extract_skus(response)

        return self._process_colors(response, color_links, item)

    def _extract_description(self, response):
        description = response.css('.product-container__text__description::text').extract()
        return [self.clean_text(d.strip()) for d in description]

    def _extract_care(self, response):
        xpath = 'descendant-or-self::*/text()'
        care_css = '.materialCare .product-container__text'
        raw_care = response.css(care_css).xpath(xpath).extract()

        care = [self.clean_text(c) for c in raw_care if len(c.strip()) > 1]
        return list(set(care))
    
    def _extract_image_urls(self, response):
        img_urls = response.css('.slider-item__image::attr(src)').extract()[:-1]
        return list(map(lambda c: c.replace('wid=70&hei=106', 'wid=461&hei=698'), img_urls))

    def _extract_skus(self, response):
        raw_item = self._extract_sku_pricing(response)
        raw_item['color'] = self._extract_color_name(response)

        skus = []
        size_selectors = response.css('a.product-stage__choose-size__select-size')
        for sku_sel in size_selectors:
            sku_item = raw_item.copy()
            sku_item['size'] = sku_sel.css('a::attr(title)').extract_first()

            if not sku_item['size']:
                sku_item['size'] = 'ONE-SIZE'
                
            sku_item['id'] = '{}_{}'.format(sku_item['color'], sku_item['size'])

            if sku_sel.css('a::attr(disabled)').extract():
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus
    
    def _extract_sku_pricing(self, response):
        return {
            'price': self._extract_price(response),
            'previous price': self._extract_prev_price(response),
            'currency': self._extract_currency(response)
        }

    def _extract_color_name(self, response):
        raw_product = response.css('.product-variations::attr(data-current)').extract_first()
        raw_product = json.loads(raw_product)

        return raw_product['color']['displayValue']
    
    def _extract_currency(self, response):
        return response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()

    def _extract_price(self, response):
        return response.xpath('//meta[@itemprop="price"]/@content').extract_first()

    def _extract_prev_price(self, response):
        previous_price = response.css('span.product-price--price-standard s::text').extract_first()
        if previous_price:
            return previous_price.strip()[1:]
    
    def _extract_raw_product(self, response):
        script = response.xpath('//script[contains(., "productCurrency")]').extract_first()

        raw_product = re.search(r"({.*?})", script).group(1)
        return json.loads(raw_product)

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)
