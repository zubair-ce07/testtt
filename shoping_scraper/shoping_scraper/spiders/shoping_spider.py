import scrapy

from shoping_scraper.items import ShopingItem


class ShopingSpider(scrapy.Spider):
    name = "shop"

    def start_requests(self):
        men_site_url = 'https://kith.com'
        kids_page_url = 'https://kith.com/collections/kids-latest'
        yield scrapy.Request(url=men_site_url, callback=self.parse_men_site)
        yield scrapy.Request(url=kids_page_url, callback=self.parse_page_containing_item)

    def parse_men_site(self, response):
        for brand_url in response.css('body ul:nth-child(2) li:nth-child(3) >ul>li>a::attr(href)').extract():
            yield response.follow(url=brand_url, callback=self.parse_page_containing_item)

    def parse_page_containing_item(self, response):
        for item_url in response.css('.product-card-image-wrapper::attr(href)').extract():
            yield response.follow(url=item_url, callback=self.parse_page_contains_sigle_item)

    def parse_page_contains_sigle_item(self, response):
        item = ShopingItem()
        item['colors'] = response.css('span.product-header-title.-variant::text').extract_first().strip()
        item['name'] = response.css('h1.product-header-title span::text').extract_first().strip()
        item['price'] = response.css('span.product-header-title.-price::text').extract_first().strip()
        yield item
