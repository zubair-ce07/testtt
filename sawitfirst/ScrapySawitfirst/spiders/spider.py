import re
from w3lib.url import add_or_replace_parameters
from w3lib.url import url_query_parameter

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ScrapySawitfirst.parser import SawItFirstParser


class SawItFirstCrawler(CrawlSpider):
    name = 'sawitfirst'
    allowed_domains = ['isawitfirst.com', 'amazonaws.com', 'fsm-isif.attraqt.com']
    start_urls = ['https://www.isawitfirst.com/']
    categories_css = [".category-links", ".megamenu-mobile-secondary-wrapper"]
    link_extractor = LinkExtractor(deny_extensions=['html'], restrict_css=categories_css)

    parser = SawItFirstParser()
    attraqt_url = "https://fsm-isif.attraqt.com/zones-ajax.aspx"
    uid = "ATT_1564987309510_06771628066488389"
    sid = "db4jx5c7ut"
    category_hitsperpage = 60
    prodpage_bottom_hitsperpage = 15
    fields_category = "id, handle, image, title, tags, FSM_compare_at_price, FSM_price, FSM_OnSale"
    fields_prodpage_bottom = "id, handle, image, title, tags, FSM_compare_at_price, FSM_price, FSM_OnSale"

    def parse(self, response):
        if response.css(".product-listing"):
            product_urls = re.findall(r'"url": "(.+)"', response.text)
            for href in product_urls:
                yield scrapy.Request(response.urljoin(href), callback=self.parser.parse)
        for href in self.link_extractor.extract_links(response):
            yield response.follow(href, callback=self.parse)

        page = url_query_parameter(response.url, "page", None)
        if page:
            params = self.prepare_params(response)
            request = scrapy.Request(
                add_or_replace_parameters(self.attraqt_url, params), callback=self.parse_next_page)
            request.meta["url"] = response.url
            yield request

    def parse_next_page(self, response):
        page_data = json.loads(response.text)
        page_data = page_data["zones"][0]["data"]["metadata"]
        url = response.meta["url"]
        hits = int(page_data["hits"])
        hitsperpage = int(page_data["hitsperpage"])
        first = int(page_data["first"])
        if (first + hitsperpage) < hits:
            url = urlsplit(url).geturl()
            if first == 0:
                next_page = 1
            else:
                next_page = (first / hitsperpage) + 1
            url = add_or_replace_parameter(url, 'page', str(next_page))
            yield scrapy.Request(url, callback=self.parse)

    def prepare_params(self, response):
        category = response.css("[id=attraqt-settings]::attr(data-attraqt-category)").extract_first()
        params = {
            "siteid": response.css(".page-collection::attr(data-attraqt-site-id)").extract_first(),
            "pageurl": response.url,
            "zone0": response.css("[id=attraqt-settings]::attr(data-attraqt-page-type)").extract_first(),
            "sid": self.sid,
            "uid": self.uid,
            "config_category": category,
            "config_categorytree": category
        }
        if params["zone0"] == "category":
            params["fields_category"] = self.fields_category
            params["category_hitsperpage"] = self.category_hitsperpage
            page = url_query_parameter(response.url, "page", None)
            params["category_page"] = int(page) + 1
        else:
            params["fields_prodpage_bottom"] = self.fields_prodpage_bottom
            params["prodpage_bottom_hitsperpage"] = self.prodpage_bottom_hitsperpage
            params["sku"] = response.css(".page-product::attr(data-product-id)").extract_first()
        return params
