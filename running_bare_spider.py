import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from RunningBare.items import RunningBareItem
import urllib.parse as urlparse


class RunningBareSpider(CrawlSpider):

    name = "running_bare_spider"

    start_urls = [
        "http://www.runningbare.com.au/"
    ]
    rules = [
        Rule(LinkExtractor(restrict_xpaths="//div[@id='slidemenu']"),
             process_links='process_category_links', follow=True),

        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class,'productName')]/a"),
             process_links='process_item_details_links',
             process_request='process_item_details_request',
             callback="parse_item_details")
    ]

    def append_base_url(self, url):
        return urlparse.urljoin(self.start_urls[0], url)

    def process_category_links(self, links):
        for link in links:
            link.url = self.append_base_url(link.url)
            link.url = self.get_complete_item_list_url(link.url)
            yield link

    def process_item_details_links(self, links):
        for link in links:
            link.url = self.append_base_url(link.url)
            yield link

    @staticmethod
    def process_item_details_request(item_details_request):
        item_details_request.meta["original_url"] = item_details_request.url
        return item_details_request

    @staticmethod
    def get_complete_item_list_url(category_url):
        url_parts = list(urlparse.urlparse(category_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'page': -1})  # passing page = -1 to get all the items
        url_parts[4] = urlparse.urlencode(query)
        return urlparse.urlunparse(url_parts)

    def parse_item_details(self, item_details_response):
        item_loader = ItemLoader(item=RunningBareItem(), response=item_details_response)
        self.populate_brand(item_loader)
        self.populate_care(item_loader)
        self.populate_currency(item_loader)
        self.populate_description(item_loader)
        self.populate_gender(item_loader)
        self.populate_image_urls(item_loader)
        self.populate_industry(item_loader)
        self.populate_market(item_loader)
        self.populate_name(item_loader)
        self.populate_price(item_loader)
        self.populate_retailer(item_loader)
        self.populate_retailer_sku(item_loader)
        self.populate_spider_name(item_loader)
        self.populate_url(item_loader, item_details_response.url)
        self.populate_url_original(item_loader, item_details_response.meta["original_url"])
        return self.populate_skus(item_loader, item_details_response)

    @staticmethod
    def populate_brand(item_loader):
        item_loader.add_value("brand", "Running Bare")

    @staticmethod
    def populate_care(item_loader):
        item_loader.add_xpath("care",
                              "//div[contains(@id,'collapseFive')]//text()[normalize-space()]")

    @staticmethod
    def populate_currency(item_loader):
        item_loader.add_xpath("currency",
                              "normalize-space(//div[@class='row top']"
                              "//button[contains(@class,'currencyselectorButton')]/text())")

    @staticmethod
    def populate_description(item_loader):
        item_loader.add_xpath("description",
                              "normalize-space(//div[contains(@id,'collapseOne')]/descendant::*/text())")

    @staticmethod
    def populate_gender(item_loader):
        item_loader.add_value("gender", "women")

    @staticmethod
    def populate_image_urls(item_loader):
        item_loader.add_xpath("image_urls",
                              "//li[contains(@class,'fullscreen-thumbnails')]//img/@src")

    @staticmethod
    def populate_industry(item_loader):
        item_loader.add_value("industry", "Garment")

    @staticmethod
    def populate_market(item_loader):
        item_loader.add_value("market", "AU")

    @staticmethod
    def populate_name(item_loader):
        item_loader.add_xpath("name",
                              "//h1[contains(@class,'productTitle')]/text()")

    @staticmethod
    def populate_price(item_loader):
        item_loader.add_xpath("price",
                              "substring-after(//div[contains(@class,'price')]//span[@class='is']/text(),'$')")

    @staticmethod
    def populate_retailer(item_loader):
        item_loader.add_value("retailer", "runningbare-au")

    @staticmethod
    def populate_retailer_sku(item_loader):
        item_loader.add_xpath("retailer_sku",
                              "substring-after(//p[@class='productCode']/text(), 'Product code: ')")

    @staticmethod
    def get_color_from_url(url):
        parsed_url = urlparse.urlparse(url)
        parsed_path = parsed_url.path.split("/")
        if parsed_path:
            color = parsed_path[len(parsed_path) - 1]
            return color.upper()

    @staticmethod
    def get_unselected_colors_from_response(item_details_response):
        colors = item_details_response.xpath("//div[contains(@class,'selectcolour') and "
                                             "not (contains(@class,'selected'))]/@data-value").extract()
        return colors

    @staticmethod
    def get_selected_color_from_response(item_details_response):
        color = item_details_response.xpath("//div[contains(@class,'selectcolour') and "
                                            "contains(@class,'selected')]/@data-value").extract_first().upper()
        return color

    @staticmethod
    def get_color_url(url, color):
        parsed_url = urlparse.urlparse(url)
        new_url_path = urlparse.urljoin(parsed_url.path, color)
        url_parts = list(parsed_url)
        url_parts[2] = new_url_path

        return urlparse.urlunparse(url_parts)

    def get_color_urls(self, colors, base_url):
        color_urls = []
        for color in colors:
            color_urls.append(self.get_color_url(base_url, color))
        return color_urls

    @staticmethod
    def is_size_out_of_stock(response, size):
        is_out_of_stock = response.xpath("//div[@title='{size}' and contains(@class,'Disabled')]".format(
            size=size)).extract()
        return is_out_of_stock

    def make_next_color_request(self, item_loader, color_urls):
        if not color_urls:
            return

        return scrapy.Request(color_urls.pop(), callback=self.populate_skus_of_next_color,
                              meta={'item_loader': item_loader, 'color_urls': color_urls})

    def append_skus(self, response, item_loader):
        skus = item_loader.get_output_value("skus")
        if not skus:
            skus = {}

        color = self.get_selected_color_from_response(response)
        currency = item_loader.get_output_value("currency")
        price = item_loader.get_output_value("price")

        sizes = response.xpath("//div[contains(@class,'selectsize')]/@title").extract()
        for size in sizes:
            sku = "{color}_{size}".format(color=color, size=size)
            skus[sku] = {"color": color, "currency": currency, "price": price, "size": size}
            if self.is_size_out_of_stock(response, size):
                skus[sku]["out_of_stock"] = True

        return skus

    def request_skus_of_next_color(self, item_loader, color_urls):
        next_color_request = self.make_next_color_request(item_loader, color_urls)
        if next_color_request:
            return next_color_request
        else:
            return item_loader.load_item()

    def populate_skus_of_next_color(self, response):
        item_loader = response.meta["item_loader"]
        item_loader.add_value("skus", self.append_skus(response, item_loader))
        color_urls = response.meta["color_urls"]

        return self.request_skus_of_next_color(item_loader, color_urls)

    def populate_skus(self, item_loader, response):
        item_loader.add_value("skus", self.append_skus(response, item_loader))
        colors = self.get_unselected_colors_from_response(response)
        color_urls = self.get_color_urls(colors, response.url)

        return self.request_skus_of_next_color(item_loader, color_urls)

    def populate_spider_name(self, item_loader):
        item_loader.add_value("spider_name", self.name)

    @staticmethod
    def populate_url(item_loader, url):
        item_loader.add_value("url", url)

    @staticmethod
    def populate_url_original(item_loader, original_url):
        item_loader.add_value("url_original", original_url)
