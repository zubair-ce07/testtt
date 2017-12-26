import scrapy


class ItemSpider(scrapy.Spider):
    name = 'item_spider'
    allowed_domains = ['joseph-fashion.com']
    start_urls = ['http://joseph-fashion.com/']

    def parse(self, response):
        data = response.meta["product"]
        data_catalogue = data["skus"]
        data_catalogue.update(self.item_catalogue(response))
        return data

    def item_catalogue(self, response):
        items = dict()
        data = response.meta["product"]
        data["trail"].append(response.url)
        size_list = response.xpath(
            "//ul[contains(@class, 'size')]//li")
        for size in size_list:
            details = self.item_size(response, size)
            if size.xpath("self::node()[contains(@class, 'unselectable')]"):
                details["out_of_stock"] = True

            item_key = f'{details["colour"]}_{details["size"]}'
            items[item_key] = details

        return items

    def item_size(self, response, item):
        details = dict()
        price = response.xpath("//meta[@itemprop='price']/@content")
        currency = response.xpath("//meta[@itemprop='priceCurrency']/@content")
        color = response.xpath(
            "//ul[contains(@class, 'color')]//li[contains(@class, 'selected')]//img/@alt")
        size = item.xpath("//a/@title").extract_first().strip("Select Size: ")
        details["colour"] = color.extract_first()
        details["currency"] = currency.extract_first()
        details["price"] = price.extract_first()
        details["size"] = size
        return details
