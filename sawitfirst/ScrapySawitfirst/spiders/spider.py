import re
from w3lib.url import add_or_replace_parameters

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ScrapySawitfirst.parser import SawItFirstParser


class SawItFirstCrawler(CrawlSpider):
	name = 'sawitfirst'
	allowed_domains = ['isawitfirst.com', 'amazonaws.com', 'fsm-isif.attraqt.com']
	start_urls = ['https://www.isawitfirst.com/']
	categories_css = [".category-links", ".megamenu-mobile-secondary-wrapper"]

	parser = SawItFirstParser()
	attraqt_url = "https://fsm-isif.attraqt.com/zones-ajax.aspx"
	rules = (
		Rule(LinkExtractor(deny_extensions=['html'], restrict_css=categories_css), callback="parse"),
	)

	def parse(self, response):
		if response.css(".product-listing"):
			product_urls = re.findall(r'"url": "(.+)"', response.text)
			for href in product_urls:
				yield scrapy.Request(response.urljoin(href), callback=self.parser.parse_item)
		for category in self.categories_css:
			for href in response.css(f"{category} a::attr(href)").extract():
				yield scrapy.Request(response.urljoin(href), callback=self.parse)
		if re.findall(r"page=\d+$", response.url):
			params = self.parser.prepare_params(response)
			request = scrapy.Request(
				add_or_replace_parameters(self.attraqt_url, params), callback=self.parser.parse_next_page)
			request.meta["url"] = response.url
			yield request

