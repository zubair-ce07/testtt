# from urllib import urlencode
from urllib.parse import urlencode
import urllib

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from men_at_work.items import MenAtWorkItem


class MenAtWorkSpider(CrawlSpider):
    name = "men_at_work"
    allowed_domains = ["menatwork.nl"]
    start_urls = ["https://www.menatwork.nl"]

    rules = (
        Rule(LinkExtractor(restrict_css=['a.headerlist__link'])),
        Rule(LinkExtractor(restrict_css=['[rel="next"]'], tags=['link'])),
        Rule(LinkExtractor(restrict_css='.thumb-link'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = MenAtWorkItem()
        item['url'] = response.url
        item['brand'] = self.get_brand(response)
        item['name'] = self.get_name(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)

        skus = self.get_skus(response)
        color_urls = response.css('.swatches.color>li:not(.selected)>a ::attr(href)').extract()
        if color_urls:
            return self.get_color_request(color_urls, skus, item)
        else:
            item['skus'] = skus
            return item

    def parse_colors(self, response):
        color_urls = response.meta['color_urls']
        item = response.meta['item']
        skus = response.meta['skus']
        selected_color_skus = self.get_skus(response)
        skus.extend(selected_color_skus)
        if color_urls:
            return self.get_color_request(color_urls, skus, item)
        else:
            item['skus'] = skus
            return item

    def get_color_request(self, color_urls, skus, item):
        return Request(color_urls.pop(0), callback=self.parse_colors,
                meta={'color_urls': color_urls, 'item': item, 'skus': skus})

    def get_brand(self, response):
        return urllib.parse.unquote(response.css('div#productData ::attr(data-brand)').extract_first())

    def get_name(self, response):
        return response.css('[itemprop=name] ::text').extract_first()

    def get_image_urls(self, response):
        return response.css('.thumbnail-link ::attr(href)').extract()

    def get_description(self, response):
        desc = []
        desc_tab1 = self.clean_object(response.css('div#tab1::text').extract())
        desc_tab2 = self.clean_object(response.css('div#tab2::text').extract())
        desc_tab3 = self.clean_object(response.css('div.product-main-attributes span ::text').extract())
        desc_tab4 = self.clean_object(response.css('ul.list-usp_pdp li ::text').extract())
        desc = desc_tab1 + desc_tab2 + desc_tab3 + desc_tab4
        return desc

    def get_skus(self, response):
        selected_color = response.css('li.selected-value::text').extract_first()
        variants = response.css('select.variation-select option')
        price = response.css('span.price-standard::text').extract_first()
        sale_price = response.css('span.price-sales::text').extract_first()
        skus = []
        for variant in variants:
            size = self.clean_object(variant.css('option::text').extract_first())[0]
            sku = {
                "sku_id": selected_color+'_'+size,
                "currency": "EUR",
                "size": size,
                "colour": selected_color,
            }
            if len(sale_price):
                sku['price'] = sale_price
                sku['previous_prices'] = [price]
            else:
                sku['price'] = price
            skus.append(sku)
        return skus

    def clean_object(self, object):
        clean_obj = [x.strip('\t\n ') for x in object]
        return [x for x in clean_obj if x != u'']

