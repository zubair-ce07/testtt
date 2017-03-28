import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from Sheego.items import SheegoItem
import urllib.parse as urlparse
from datetime import datetime
import json


class SheegoSpider(CrawlSpider):

    name = "sheego_spider"
    base_url = "https://www.sheego.de/"

    start_urls = [
            "https://www.sheego.de/index.php"
            "?cl=oxwCategoryTree&jsonly=true&staticContent=true&sOutputType=js&bShoppiless=true"
    ]

    def append_base_url(self, url):
        if url:
            return urlparse.urljoin(self.base_url, url)

    def get_subcategory_urls(self, urls, item_categories):
        if "sCat" in item_categories:
            for category in item_categories["sCat"]:
                if "url" in category and category["url"]:
                    urls.append(category["url"])

                self.get_subcategory_urls(urls, category)

    def get_category_urls(self, response):
        category_urls = []
        jsonresponse = json.loads(response.body_as_unicode())

        for category in jsonresponse:
            category_urls.append(category["url"])
            self.get_subcategory_urls(category_urls, category)

        return category_urls

    def parse(self, response):
        category_urls = self.get_category_urls(response)
        for category_url in category_urls:
            yield scrapy.Request(url=category_url, callback=self.parse_item_list)

    def get_next_page_url(self, response):
        return self.append_base_url(response.xpath("//a[@rel='next']/@href").extract_first())

    def request_next_page(self, response):
        next_page_url = self.get_next_page_url(response)
        if next_page_url:
            return scrapy.Request(url=next_page_url, callback=self.parse_item_list)

    @staticmethod
    def get_item_detail_urls(response):
        return response.xpath("//a[contains(@class,'product__top')]/@href").extract()

    def parse_item_list(self, response):
        item_detail_urls = self.get_item_detail_urls(response)
        for item_detail_url in item_detail_urls:
            item_detail_url = self.append_base_url(item_detail_url)
            yield scrapy.Request(item_detail_url, callback=self.parse_item_details,
                                 meta={'original_url': item_detail_url})

        yield self.request_next_page(response)

    def parse_item_details(self, item_details_response):
        item_loader = ItemLoader(item=SheegoItem(), response=item_details_response)
        self.populate_brand(item_loader)
        self.populate_care(item_loader)
        self.populate_category(item_loader)
        self.populate_date(item_loader)
        self.populate_description(item_loader)
        self.populate_gender(item_loader)
        self.populate_lang(item_loader)
        self.populate_name(item_loader)
        self.populate_retailer_sku(item_loader)
        self.populate_oos_request(item_loader)
        self.populate_url(item_loader, item_details_response)
        self.populate_url_original(item_loader, item_details_response.meta["original_url"])
        return self.populate_skus(item_loader, item_details_response)

    @staticmethod
    def populate_brand(item_loader):
        item_loader.add_xpath("brand",
                              "//meta[@itemprop='brand']/@content")

    @staticmethod
    def populate_care(item_loader):
        item_loader.add_xpath("care",
                              "//dt[contains(text(),'Pflegehinweise:')]//following-sibling::dd/text()")

    @staticmethod
    def populate_category(item_loader):
        item_loader.add_xpath("category",
                              "//input[contains(@class,'breadcrumb')]/@data-econda-categorypath")

    @staticmethod
    def populate_date(item_loader):
        item_loader.add_value("date", str(datetime.now()))

    @staticmethod
    def populate_description(item_loader):
        item_loader.add_xpath("description",
                              "//div[contains(@class,'productDetailBox--bullets')]//li/text() "
                              "| (//div[@itemprop='description'])[1]//text() "
                              "| //dl[contains(@class,'articlenumber')]/following-sibling::dl//text()"
                              "[normalize-space()]")

    @staticmethod
    def populate_gender(item_loader):
        item_loader.add_value("gender", "women")

    @staticmethod
    def get_current_color_image_urls(response):
        return response.xpath("//div[contains(@class,'product-thumbs-slider-main')]//a/@href").extract()

    def populate_image_urls(self, item_loader, response):
        current_color_image_urls = self.get_current_color_image_urls(response)
        item_loader.add_value("image_urls", current_color_image_urls)

    @staticmethod
    def populate_lang(item_loader):
        item_loader.add_xpath("lang",
                              "//html/@lang")

    @staticmethod
    def populate_name(item_loader):
        item_loader.add_xpath("name",
                              "normalize-space(//span[@itemprop='name']/text())")

    @staticmethod
    def populate_retailer_sku(item_loader):
        item_loader.add_xpath("retailer_sku",
                              "//dl[contains(@class,'articlenumber')]/dd/text()")

    @staticmethod
    def get_selected_color(response):
        color = response.xpath("//input[contains(@class,'current-color-name')]/@value").extract_first()
        if color:
            return color.upper()

    @staticmethod
    def is_size_out_of_stock(response, size):
        is_out_of_stock = response.xpath("//button[contains(@title,'{size}') "
                                         "and contains(@class,'size-button')]/@disabled".format(size=size)).extract()
        return is_out_of_stock

    @staticmethod
    def get_currency(response):
        return response.xpath("//meta[@itemprop='priceCurrency']/@content").extract_first()

    @staticmethod
    def get_current_price(response):
        return response.xpath("//input[contains(@class,'lastprice')]/@value").extract_first()

    @staticmethod
    def get_previous_prices(response):
        return response.xpath("//sub[contains(@class,'wrongprice')]/text()").re(r"([\d+\,]*\d+(?:\.\d+)?)")

    @staticmethod
    def get_color_sizes(response):
        return response.xpath("//button[contains(@class,'size-button')]/text()").extract()

    def append_skus(self, response, item_loader):
        skus = item_loader.get_output_value("skus")
        if not skus:
            skus = {}

        color = self.get_selected_color(response)
        currency = self.get_currency(response)
        price = self.get_current_price(response)
        previous_prices = self.get_previous_prices(response)

        sizes = self.get_color_sizes(response)
        for size in sizes:
            sku = "{color}_{size}".format(color=color, size=size)
            skus[sku] = {"color": color,
                         "currency": currency,
                         "previous_prices": previous_prices,
                         "price": price,
                         "size": size}

            if self.is_size_out_of_stock(response, size):
                skus[sku]["out_of_stock"] = True

        return skus

    def make_next_color_request(self, item_loader, color_urls):
        if not color_urls:
            return

        return scrapy.Request(color_urls.pop(), callback=self.populate_skus_of_next_color,
                              meta={'item_loader': item_loader, 'color_urls': color_urls})

    def request_skus_of_next_color(self, item_loader, color_urls):
        next_color_request = self.make_next_color_request(item_loader, color_urls)
        if next_color_request:
            return next_color_request
        else:
            return item_loader.load_item()

    def populate_skus_of_next_color(self, response):
        item_loader = response.meta["item_loader"]
        item_loader.add_value("skus", self.append_skus(response, item_loader))

        self.populate_image_urls(item_loader, response)

        color_urls = response.meta["color_urls"]
        return self.request_skus_of_next_color(item_loader, color_urls)

    @staticmethod
    def get_color_url(url, color_code):
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'color': color_code})
        url_parts[4] = urlparse.urlencode(query)
        return urlparse.urlunparse(url_parts)

    def get_color_urls(self, color_codes, base_url):
        color_urls = []
        for color_code in color_codes:
            color_urls.append(self.get_color_url(base_url, color_code))
        return color_urls

    @staticmethod
    def get_unselected_color_codes(response):
        colors = response.xpath("//a[contains(@class,'color-item') "
                                "and not (contains(@class,'active'))]/@class").re(r"(\d+)\s")
        return colors

    def populate_skus(self, item_loader, response):
        item_loader.add_value("skus", self.append_skus(response, item_loader))

        self.populate_image_urls(item_loader, response)

        colors = self.get_unselected_color_codes(response)
        color_urls = self.get_color_urls(colors, response.url)
        return self.request_skus_of_next_color(item_loader, color_urls)

    def populate_oos_request(self, item_loader):
        item_loader.add_value("oos_request", self.__str__())

    @staticmethod
    def populate_url(item_loader, response):
        item_loader.add_value("url", response.url)

    @staticmethod
    def populate_url_original(item_loader, original_url):
        item_loader.add_value("url_original", original_url)
