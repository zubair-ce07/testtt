import scrapy
from orsay.items import OrsayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import re


class OrsaySpider(CrawlSpider):
    name = "Orsay"
    start_urls = ["http://www.orsay.com/"]

    rules = (
        Rule(LinkExtractor(allow=r".*/produkte/"), callback='parse_product_pages'),
    )

    def parse_product_pages(self, response):
        max_product_items = response.css('div.load-more-progress::attr(data-max)').extract_first()
        for items in range(72, int(max_product_items), 72):
            yield scrapy.Request("http://www.orsay.com/de-de/produkte/?sz={}".format(items), callback=self.parse_products)

    def parse_products(self, response):
        products_href = response.css('a.name-link::attr(href)').extract()
        for href in products_href:
            yield scrapy.Request("http://www.orsay.com/de-de" + href, callback=self.parse_item)

    def parse_item(self, response):
        # remove selected color from the list of selectable colors
        all_color_hrefs = response.css('.swatches.color > .selectable ::attr(href)').extract()
        selected_color_href = response.css('.swatches.color > .selectable.selected ::attr(href)').extract()
        color_hrefs = [x for x in all_color_hrefs if x not in selected_color_href]
        item = OrsayItem()
        item['brand'] = self.parse_brand()
        item['url'] = self.parse_url(response)
        item['name'] = self.parse_name(response)
        item['description'] = self.parse_description(response)
        item['retailer_sku'] = self.parse_retailer_sku(response)
        item['care'] = self.parse_care(response)
        item['category'] = self.parse_category(response)
        item['skus'] = {}
        return self.parse_sku(response, item, color_hrefs)

    def parse_brand(self):
        return "Orsay"

    def parse_care(self, response):
        care_class_names = response.xpath('//li[contains(@class, "material-care-icon")]').extract()
        care = []
        for care_class_name in care_class_names:
            care_type = re.search(r".+material-care-icon\s(.+)-", care_class_name).group(1)
            care.append(care_type)
        return care

    def parse_img_urls(self, response):
        return response.css('img[class*=primary-image]::attr(src)').extract()

    def parse_url(self, response):
        return response.url

    def parse_name(self, response):
        return response.css('h1[class=product-name]::text').extract_first()

    def parse_description(self, response):
        return response.css('div.with-gutter::text').extract()

    def parse_retailer_sku(self, response):
        return response.css('div.product-sku::text').extract_first()

    def parse_category(self, response):
        return response.css('span.breadcrumb-element::text').extract_first()

    def parse_color(self, response):
        return response.css('span.selected-value::text').extract_first()

    def parse_sizes(self, response):
        sizes = response.css('li.selectable a::text').extract()
        sizes_clean = []
        for size in sizes:
            sizes_clean.append(size.strip())
        sizes_clean = list(filter(None, sizes_clean))
        return sizes_clean

    def parse_price_currency(self, response):
        price_currency = response.css('span.price-sales::text').extract_first()
        price_currency = price_currency.strip()
        price_currency = price_currency.split(" ")
        price = price_currency[0]
        currency = price_currency[1]
        return price, currency

    def parse_sku(self, response, item, color_hrefs):
        color = self.parse_color(response)
        sizes = self.parse_sizes(response)
        img_urls = self.parse_img_urls(response)
        price, currency = self.parse_price_currency(response)
        for size in sizes:
            sku = {}
            sku['color'] = color
            sku['size'] = size
            sku['currency'] = currency
            sku['price'] = price
            sku['img_urls'] = img_urls
            item['skus']["{}_{}".format(color, size)] = sku
        if color_hrefs:
            href = color_hrefs.pop()
            yield scrapy.Request(href, callback=self.parse_sku_response, meta={"item": item, "hrefs": color_hrefs})
        else:
            yield item

    def parse_sku_response(self, response):
        item = response.meta['item']
        color_hrefs = response.meta['hrefs']
        color = self.parse_color(response)
        sizes = self.parse_sizes(response)
        img_urls = self.parse_img_urls(response)
        price, currency = self.parse_price_currency(response)
        for size in sizes:
            sku = {}
            sku['color'] = color
            sku['size'] = size
            sku['currency'] = currency
            sku['price'] = price
            sku['img_urls'] = img_urls
            item['skus']["{}_{}".format(color, size)] = sku
        if color_hrefs:
            href = color_hrefs.pop()
            yield scrapy.Request(href, callback=self.parse_sku_response, meta={"item": item, "hrefs": color_hrefs})
        else:
            yield item
