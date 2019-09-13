from json import loads
from re import findall
from urllib.parse import urljoin
from urllib.parse import urlsplit
from w3lib.url import add_or_replace_parameter
from w3lib.url import add_or_replace_parameters
from w3lib.url import url_query_parameter

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from ScrapySawitfirst.parser import SawItFirstParser


class SawItFirstCrawler(CrawlSpider):
    name = 'sawitfirst'
    allowed_domains = ['isawitfirst.com', 'amazonaws.com', 'fsm-isif.attraqt.com']
    start_urls = ['https://www.isawitfirst.com/']
    categories_css = [".category-links", ".megamenu-mobile-secondary-wrapper"]
    rules = (
        Rule(
            LinkExtractor(
                deny_extensions=['html'],
                restrict_css=categories_css),
            callback="parse"
        ),
    )
    parser = SawItFirstParser()
    attraqt_url = "https://fsm-isif.attraqt.com/zones-ajax.aspx"
    product_request_url = "https://www.isawitfirst.com/products/"
    uid = "ATT_1564987309510_06771628066488389"
    sid = "db4jx5c7ut"
    CATEGORY_HITSPERPAGE = 60
    PRODPAGE_BOTTOM_HITSPERPAGE = 15
    fields = "id,handle,image,title,tags,FSM_compare_at_price,FSM_price,FSM_OnSale"

    def parse(self, response):
        for request in super().parse(response):
            yield request
        if response.css(".product-listing"):
            product_urls = findall(r'"url": "(.+)"', response.text)
            for href in product_urls:
                yield Request(response.urljoin(href), callback=self.parser.parse)

        url = response.css("[property=og\:url]::attr(content)").extract_first()
        if "collections" in url and "page" not in url:
            url = add_or_replace_parameter(url, 'page', '1')
        page = url_query_parameter(url, "page", None)
        if not page:
            return

        params = self.prepare_params(response, url)
        request_url = add_or_replace_parameters(self.attraqt_url, params)
        request = Request(
            request_url, callback=self.parse_next_page)
        request.meta["url"] = response.url
        return request

    def parse_next_page(self, response):
        page_data = loads(response.text)
        page_data = page_data["zones"][0]["data"]["metadata"]
        url = response.meta["url"]
        next_page = self.next_page(page_data)
        url = urlsplit(url).geturl()
        url = add_or_replace_parameter(url, 'page', str(next_page))
        return Request(url, callback=self.parse)

    def next_page(self, page_data):
        hits = int(page_data["hits"])
        hitsperpage = int(page_data["hitsperpage"])
        first = int(page_data["first"])
        if (first + hitsperpage) < hits:
            if first == 0:
                return 2
            return (first / hitsperpage) + 2

    def prepare_params(self, response, url):
        category = response.css("[id=attraqt-settings]::attr(data-attraqt-category)").extract_first()
        page = url_query_parameter(url, "page", None)
        page = (int(float(page)) + 1) if (page and page != 'none') else 1
        params = {
            "siteid": response.css(".page-collection::attr(data-attraqt-site-id)").extract_first(),
            "pageurl": add_or_replace_parameter(url, 'page', '1'),
            "zone0": response.css("[id=attraqt-settings]::attr(data-attraqt-page-type)").extract_first(),
            "sid": self.sid,
            "uid": self.uid,
            "config_category": category,
            "config_categorytree": category
        }
        if params["zone0"] == "category":
            params["fields_category"] = self.fields
            params["category_hitsperpage"] = self.CATEGORY_HITSPERPAGE
            params["category_page"] = page
        else:
            params["fields_prodpage_bottom"] = self.fields
            params["prodpage_bottom_hitsperpage"] = self.PRODPAGE_BOTTOM_HITSPERPAGE
            params["sku"] = response.css(".page-product::attr(data-product-id)").extract_first()
        return params
