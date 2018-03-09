import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import UrbanLockerItem


class UrbanLocker(CrawlSpider):
    name = 'urbanlocker'
    allowed_domains = ['urbanlocker.com']
    start_urls = ['http://www.urbanlocker.com/']
    listings_xpath = ['//*[contains(@id, "adtm_menu_inner")]', '//li[contains(@id, "pagination_next_top")]//a']
    products_xpath = ['//*[contains(@class, "product_title")]//a']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_xpaths=products_xpath), callback='parse_item'),
    )

    def parse_item(self, response):
        item = UrbanLockerItem()
        item['url'] = response.url

        item['currency'] = self.product_currency(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['category'] = self.product_category(response)
        item['name'] = self.product_name(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.image_urls(response)
        item['skus'] = self.skus(response)

        self.parse_color_urls(response)
        return item

    def parse_color_urls(self, response):
        colour_urls = response.css('div.features_color_values a::attr(href)').extract()
        for url in colour_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_item)

    def product_currency(self, response):
        raw_currency = response.css('div#currencies_block_top a::text').extract_first()
        return raw_currency[:3].upper()

    def product_retailer_sku(self, response):
        retailer_sku = response.css('fieldset#product_supplier_reference span::text').re('[^\n|\t]+')
        return retailer_sku[0]

    def product_name(self, response):
        name = response.xpath('//span[contains(@itemprop , "name")]//text()').re('[^\n|\t]+')
        return ''.join(self.clean(name))

    def product_brand(self, response):
        return response.xpath('//*[contains(@class, "h4")]//span//text()').extract_first()

    def product_description_block(self, response):
        description_xpath = '//div[contains(@id, "short_description_block")]//text()'
        return "".join(self.clean(response.xpath(description_xpath).extract()))

    def product_care(self, response):
        care = re.findall("(Composition.*?\.|qualité.*?\.)", self.product_description_block(response))
        return self.clean(care)

    def product_description(self, response):
        description = self.product_description_block(response)
        return re.sub("(Composition.*?\.|qualité.*?\.)", "", description)

    def image_urls(self, response):
        image_url = response.css('span#view_full_size img::attr(src)').extract_first()

        image_ids_xpath = '//script[contains(text(), "combinationImages")]'
        image_ids = self.clean(response.xpath(image_ids_xpath).re('combinationImages\[\d\]?\[\d\] = (\d+);'))

        image_urls = [re.sub("(\d\d+)", image_id, image_url) for image_id in image_ids]
        return image_urls[1:]

    def product_colour(self, response):
        return response.css('span.features_color_value::attr(title)').extract_first()

    def product_sizes(self, response):
        size_stock = []
        sizes = response.css('ul.radio_list_attr li em::text').extract()
        sizes_in_stock = response.css('fieldset div li::attr(class)').extract()

        for size_in_stock in sizes_in_stock:
            for size in sizes:
                if not self.check_size_in_stock(size, size_in_stock):
                    continue
                raw_size_stock = {
                    'out_of_stock': 'zero_qty' in size_in_stock,
                    'size': size
                }
                size_stock.append(raw_size_stock)

        return size_stock

    def check_size_in_stock(self, size, size_in_stock):
        size_check = ''.join(size.split("/" if "/" in size else " ")).upper()
        size_check = ''.join(size.split(" ")).upper() if " " in size_check else size_check

        return ''.join(size_in_stock.split("_")[-1]).upper() == size_check

    def product_category(self, response):
        category = response.css('div.breadcrumb').xpath('//span[contains(@itemprop , "title")]//text()').extract()
        raw_category = response.css('div.breadcrumb div::text').re('[^\n|^\t]+')
        if raw_category:
            category.append(raw_category[0])
        return self.clean(category)

    def product_pricing(self, response):
        price_xpath = '//fieldset[contains(@class, "price_container")]//span[contains(@id, "price")]//text()'
        raw_prices = response.xpath(price_xpath).re('([\d,\d]+)')
        prices = [int(float(raw_price.replace(",", ".")) * 100) for raw_price in raw_prices]
        prices.sort()
        current_price = prices.pop(0)
        return current_price, prices

    def skus(self, response):
        skus = []

        stock_sizes = self.product_sizes(response)
        colour = self.product_colour(response)
        price, previous_prices = self.product_pricing(response)

        for stock_size in stock_sizes:
            size = "One Size" if "Taille Unique" in stock_size['size'] else stock_size['size']
            sku = {
                "colour": colour,
                "price": price,
                "previous_prices": previous_prices,
                "size": size,
                "sku_id": '{0}_{1}'.format(colour, size)
            }
            if stock_size['out_of_stock']:
                sku['out_of_stock'] = True
            skus.append(sku)
        return skus

    def clean(self, to_clean):
        cleaned = [per_entry.strip() for per_entry in to_clean] if to_clean else ""
        return list(filter(None, cleaned))
