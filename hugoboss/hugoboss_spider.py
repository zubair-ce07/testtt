import scrapy
import json
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from items import HugoBossItem


class HugoBossSpider(CrawlSpider):
    name = 'hugoboss'
    allowed_domains = ['hugoboss.com']
    start_urls = ['https://www.hugoboss.com/uk/']

    DOWNLOAD_DELAY = 0.2

    listing_css = ['.nav-list--third-level', '.pagingbar__item--arrow']
    product_sel = '.product-tile__product-name'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=('/inspiration/'))),
        Rule(LinkExtractor(restrict_css=product_sel), callback='parse_item'),
    )

    def parse_item(self, response):
        prod_details = self._extract_prod_details(response)

        item = HugoBossItem()
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

        color_links = response.css('.swatch-list__button--is-empty a::attr(href)').extract()
        yield from self._check_col_links(response, color_links, item)

    def _check_col_links(self, response, color_links, item):
        if color_links:
            yield response.follow(color_links.pop(), callback=self._extract_color,\
                                 meta={'item': item, 'color_links': color_links})
        else:
            yield item

    def _extract_color(self, response):
        item = response.meta.get('item')
        color_links = response.meta.get('color_links')

        item['image_urls'] += self._extract_image_urls(response)
        item['skus'] += self._extract_skus(response)

        yield from self._check_col_links(response, color_links, item)
    
    def _extract_prod_details(self, response):
        script = response.xpath('//script[contains(., "productCurrency")]').extract_first()

        raw_product = re.search(r"({.*?})", script).group(1)
        return self._extract_json(raw_product)

    def _extract_description(self, response):
        description = response.css('.product-container__text__description::text').extract()
        return [self.clean_text(d.strip()) for d in description]

    def _extract_care(self, response):
        care = response.css('.accordion__care-icon__text::text').extract()
        return list(map(str.strip, care))
    
    def _extract_image_urls(self, response):
        img_urls = response.css('.slider-item__image::attr(src)').extract()[:-1]
        return list(map(lambda c: c.replace('wid=70&hei=106', 'wid=461&hei=698'), img_urls))


    def _extract_skus(self, response):
        item = {}
        item['color'] = self._extract_color(response)
        item['price'] = self._extract_price(response)
        item['currency'] = self._extract_currency(response)
        previous_price = self._extract_prev_price(response)

        if previous_price:
            item['previous price'] = previous_price.strip()[1:]
        
        skus = []
        size_selectors = response.css('a.product-stage__choose-size__select-size')
        for sku in size_selectors:
            sku_item = item.copy()
            sku_item['size'] = sku.css('a::attr(title)').extract_first()
            
            if not sku_item['size']:
                sku_item['size'] = 'ONE-SIZE'
                
            sku_item['id'] = '{}_{}'.format(sku_item['color'], sku_item['size'])

            if sku.css('a::attr(disabled)').extract_first():
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus

    def _extract_color(self, response):
        data_current = response.css('.product-variations::attr(data-current)').extract_first()
        data_current = self._extract_json(data_current)

        return data_current['color']['displayValue']
    
    def _extract_currency(self, response):
        return response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()

    def _extract_price(self, response):
        return response.xpath('//meta[@itemprop="price"]/@content').extract_first()

    def _extract_prev_price(self, response):
        return response.css('span.product-price--price-standard s::text').extract_first()

    def _extract_json(self, json_str):
        return json.loads(json_str)
    
    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)
