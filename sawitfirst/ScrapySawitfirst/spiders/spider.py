import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ScrapySawitfirst.parser import Parser
from ScrapySawitfirst.items import Item


class SawItFirstSpider(CrawlSpider, Parser):
	name = 'sawitfirst'
	allowed_domains = ['isawitfirst.com', 'amazonaws.com', 'fsm-isif.attraqt.com']
	start_urls = ['https://www.isawitfirst.com/']
	categories_css = [
		".category-links", ".megamenu-mobile-categories", ".megamenu-mobile__subcat-tabs",
		".megamenu-mobile-secondary-wrapper", ".refinement__pagination", ".mobile-pagination-new",
		".desktop-pagination-new", ".collection-container", ".megamenu-mobile-collection",
		".megamenu-mobile-subcats", "megamenu-categories", "list-group", ".nav", ".sub-menu",
		".megamenu-mobile-collection__items-wrapper"
	]

	rules = (
		Rule(LinkExtractor(deny_extensions=['html'], restrict_css=categories_css), callback="parse"),
	)

	def parse(self, response):
		if response.css(".product-listing"):
			product_urls = re.findall(r'"url": "(.+)"', response.text)
			for href in product_urls:
				yield scrapy.Request(response.urljoin(href), callback=self.parse_item)
		hrefs = []
		for category in self.categories_css:
			hrefs.extend(response.css(category + " a::attr(href)").extract())
		if re.findall(r"page=\d+$", response.url):
			params = self.prepare_params(response)
			request = scrapy.Request(
				"https://fsm-isif.attraqt.com/zones-ajax.aspx?" + urlencode(params), callback=self.next_page)
			request.meta["url"] = response.url
			yield request
		for href in hrefs:
			yield scrapy.Request(response.urljoin(href), callback=self.parse)

	def parse_item(self, response):
		product = Item()
		product['retailer_sku'] = self.retailer_sku(response)
		product['gender'] = self.gender(response)
		product['category'] = self.category(response)
		product['brand'] = self.brand(response)
		product['url'] = self.url(response)
		product['name'] = self.product_name(response)
		product['description'] = self.description(response)
		product['care'] = self.care(response)
		product['image_urls'] = self.image_urls(response)
		product['price'] = self.price(response)
		product['old_price'] = self.old_price(response)
		product['currency'] = self.currency(response)
		product['skus'] = {}
		headers = {
			"Accept": "*/*",
			"Content-Type": "application/json; charset=UTF-8",
			"Origin": "https://www.isawitfirst.com",
			"Referer": response.url,
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.99"
		}
		form_data = {"jl_numbers": re.findall(r"-(jl\d+-?\d*)$", response.url), "site": "isawitfirst.com"}
		request = scrapy.Request("https://4uiusmis27.execute-api.eu-central-1.amazonaws.com/isaw/get-colours",
								 callback=self.skus, method="POST", body=json.dumps(form_data), headers=headers
								 )
		request.meta["product"] = product
		yield request




