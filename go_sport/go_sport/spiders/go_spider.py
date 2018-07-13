import scrapy
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from go_sport.items import GoSportItem


class GoSpiderSpider(CrawlSpider):
    name = 'go_spider'
    allowed_domains = ['go-sport.pl']
    start_urls = ['https://www.go-sport.pl/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='level-top']",)),
             follow=True),
        Rule(LinkExtractor(restrict_css=("a.action.next",)),
             follow=True),
        Rule(LinkExtractor(restrict_css=("div.product-item h2 > a.product_url",)),
            callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        item = GoSportItem()

        item['retailer_sku'] = response.css('span.product_id::text').extract_first()
        item['gender'] = response.xpath('//span[@class="tags1"]/span[contains(@class, "tag")\
                         and contains(., "gender")]/text()').extract_first().split(":")[1]
        item['category'] = response.css('span.categories span.category::text').extract()[0].split('/')[1:]
        item['brand'] = response.css('span.nosto_product span.brand::text').extract_first()
        item['url'] = response.css('span.nosto_product span.url::text').extract_first()
        item['name'] = response.css('span.nosto_product span.name::text').extract_first()
        description = response.css('div.product.attribute.description div::text').extract_first()

        if description:
            item['description'] = description.split(".")
        else:
            item['description'] = "No Description Avaliable"

        item['image_urls'] = response.css('span.alternate_image_url::text').extract()
        item['skus'] = self._get_skus(response)

        yield item

    def _get_skus(self, response):
        skus_selector = response.css('span.skus span.nosto_sku')
        skus = []

        if not skus_selector:
            sku_item = {}
            sku_item['color'] = response.css('span.custom_fields span.color_web::text').extract_first()
            sku_item['price'] = response.css('span.nosto_product span.price::text').extract_first()
            sku_item['currency'] = response.css('span.nosto_product span.price_currency_code::text').extract_first()
            sku_item['size'] = "Single Size"
            sku_item['previous_price'] = response.css('span.nosto_product span.list_price::text').extract_first()
            sku_item['id'] = response.css('span.nosto_product span.product_id::text').extract_first()

            return [sku_item]
        
        megento_json = response.xpath('//script[contains(., "Magento_Swatches/js/swatch-renderer-custom")]/text()').extract_first()
        megento_json = json.loads(megento_json)
        skus_in_stock = megento_json["[data-role=swatch-options]"]\
                                    ["Magento_Swatches/js/swatch-renderer-custom"]\
                                    ["jsonConfig"]["optionPrices"]

        for sku in skus_selector:
            sku_item = {}
            sku_item['color'] = sku.css('span.color_web::text').extract_first()
            sku_item['price'] = sku.css('span.price::text').extract_first()
            sku_item['currency'] = response.css('span.nosto_product span.price_currency_code::text').extract_first()
            sku_item['size'] = sku.css('span.size::text').extract_first()
            sku_item['previous_price'] = sku.css('span.list_price::text').extract_first()
            sku_item['id'] = sku.css('span.id::text').extract_first()

            if sku_item['id'] not in skus_in_stock:
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus
