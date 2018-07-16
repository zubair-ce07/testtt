import scrapy


class Task3Item(scrapy.Item):
    item = {}
    item['retailer_sku'] = scrapy.Field()
    item['gender'] = scrapy.Field()
    item['categories'] = scrapy.Field()
    item['brand'] = scrapy.Field()
    item['url'] = scrapy.Field()
    item['name'] = scrapy.Field()
    item['description'] = scrapy.Field()
    item['image_urls'] = scrapy.Field()
    item['skus'] = scrapy.Field()
