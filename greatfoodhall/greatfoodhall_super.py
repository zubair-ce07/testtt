import re

import scrapy
from Greatfoodhall.items import GreatfoodhallLoader
from scrapy.spiders import CrawlSpider


class GreatfoodhallSpider(CrawlSpider):
    name = "greatfoodhall"
    start_urls = ["http://www.greatfoodhall.com/"]

    def parse(self, response):
        category_links = response.xpath('//div[@class="item"]/a/@href').extract()
        for link in category_links:
            yield scrapy.Request("http://www.greatfoodhall.com/eshop/" + link, callback=self.parse_pages)

    def parse_pages(self, response):
        last_page_number = self.parse_last_page_number(response)
        for index in range(1, int(last_page_number)):
            yield scrapy.Request("http://www.greatfoodhall.com/eshop/ShowProductPage.do?curPage_1={}".format(index), callback=self.parse_products)

    def parse_products(self, response):
        product_links = response.xpath('//div[@class="productTmb"]/a/@href').extract()
        for link in product_links:
            yield scrapy.Request(link, callback=self.parse_item)

    def parse_item(self, response):
        loader = GreatfoodhallLoader(response=response)
        loader.add_xpath("price", '//div[@class="itemOrgPrice2"]/text()')
        loader.add_xpath("name", '//p[contains(@class, "description pB5")]/text()')
        loader.add_xpath("brand", '//h1[@class="pL6"]/text()')
        loader.add_xpath("unit", '//span[contains(@class, "ml pB5 pL6")]/text()')
        loader.add_xpath("categories", '//div[contains(@class, "breadCrumbArea")]/ul/text()')
        loader.add_xpath("image_url", '//div[@class="productPhoto"]/img/@src')
        loader.add_xpath("description", '//div[@id="nutrition"]/table/tbody/text()')
        loader.add_xpath("discounted_price", '//div[@class="newPrice pB5"]/text()')
        loader.add_value("availability", "in stock")
        loader.add_value("barcode", "N/A")
        loader.add_value("reviews_score", "N/A")
        loader.add_value("page_url", response.url)
        return loader.load_item()

    def parse_last_page_number(self, response):
        required_script_xpath = '//script[contains(text(), "totalpage =")]/text()'
        script = response.xpath(required_script_xpath).extract_first()
        last_page = re.search('(?<=totalpage\s=\s)\d+', script)
        last_page = last_page.group(0)
        return last_page
