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
        Rule(LinkExtractor(restrict_css=['a.headerlist__link', '[rel="next"]'], tags=['a', 'link'])),
        Rule(LinkExtractor(restrict_css='.thumb-link'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = MenAtWorkItem()
        item['url'] = response.url
        item['brand'] = self.get_brand(response)
        item['name'] = self.get_name(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)

        item['skus'] = self.get_skus(response)
        color_urls = response.css('.swatches.color>li:not(.selected)>a ::attr(href)').extract()
        if color_urls:
            return self.get_color_request(color_urls, item)
        else:
            return item

    def parse_colors(self, response):
        color_urls = response.meta['color_urls']
        item = response.meta['item']
        selected_color_skus = self.get_skus(response)
        item['skus'].extend(selected_color_skus)
        if color_urls:
            return self.get_color_request(color_urls, item)
        else:
            return item

    def get_color_request(self, color_urls, item):
        return Request(color_urls.pop(0),
                       callback=self.parse_colors,
                       meta={'color_urls': color_urls,
                             'item': item})

    def get_brand(self, response):
        return urllib.parse.unquote(response.css('div#productData ::attr(data-brand)').extract_first())

    def get_name(self, response):
        return response.css('[itemprop=name] ::text').extract_first()

    def get_image_urls(self, response):
        return response.css('.thumbnail-link ::attr(href)').extract()

    def get_description(self, response):
        desc_css = 'div#tab1::text, div#tab2::text, div.product-main-attributes span ::text, ul.list-usp_pdp li ::text'
        desc = self.clean_object(response.css(desc_css).extract())
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
            if sale_price:
                sku['price'] = sale_price
                sku['previous_prices'] = [price]
            else:
                sku['price'] = price
            skus.append(sku)
        return skus

    def clean_object(self, obj):
        clean_obj = [x.strip('\t\n ') for x in obj]
        return [x for x in clean_obj if x]
