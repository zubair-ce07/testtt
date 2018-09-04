# -*- coding: utf-8 -*-
import scrapy
import w3lib.url as wurl
from ProductScrapper.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'spider'
    item_counter = 0
    start_urls = ['https://www.ernstings-family.de/']

    def parse(self, response):
        categories_path = ".main-navigation-inner-wrapper li a::attr(href)"
        categories = response.css(categories_path).extract()
        print(categories)
        # categories: maedchen, jungen, damen, wohnen, sale
        for cat in categories:
            yield scrapy.Request(url=cat, callback=self.parse_main_page)

    def parse_main_page(self, response):
        sub_categories_path = ".navigation-block-holder>ul>li>a::attr(href)"
        sub_categories = response.css(sub_categories_path).extract()
        #  remove duplicate sale links from other categories
        if "sale" not in response.url:
            sub_categories = [cat for cat in sub_categories if "sale" not in cat]

        for sub_cat in sub_categories:
            yield scrapy.Request(url=sub_cat, callback=self.parse_filter_page)

    def parse_filter_page(self, response):
        items_path = "a[class *='product-list-tile-holder']::attr(href)"
        items = response.css(items_path).extract()
        print("*" * 25)
        print("Page: "+response.url)
        print("Items: "+str(len(items)))
        print("*" * 25)
        for item in items:
            yield scrapy.Request(url=item, callback=self.parse_item_page)

        # if there are more than one pages,
        # traverse next pages unless finished
        total_items = response.css(".product-count-holder::text").extract_first()
        if total_items:
            total_item_count = int(total_items.split(" ")[0])
            max_page = int(total_item_count/24)+1
            curr_page_no = int(wurl.url_query_parameter(response.url,
                                                        "pageNo",
                                                        "1"))
            next_page_no = curr_page_no + 1
            if next_page_no <= max_page:
                next_page_url = wurl.add_or_replace_parameter(response.url,
                                                              "pageNo",
                                                              str(curr_page_no+1))
                yield scrapy.Request(url=next_page_url, callback=self.parse_filter_page)
        else:
            print("*" * 25)
            print("No more items")
            print("exiting: "+response.url)
            print("*" * 25)

    def parse_item_page(self, response):
        name_path = "h1.product-name::text"
        label_path = "span.label-text::text"
        price_path = "span.product-price::text"
        colors_path = "p[class *= 'product-color']::text"
        detail_path = "div#tab-id-1-content p::text"
        features_path = "div#tab-id-1-content ul>li::text"
        materials_path = "div#tab-id-2-content ul>li::text"
        image_path = "div[class *= 'product-view']>a::attr(href)"

        item = ProductItem()
        name = response.css(name_path).extract_first()
        item['name'] = name.split("\n")[1].split("\t")[4]
        item['url'] = response.url
        item['label'] = response.css(label_path).extract_first()
        price = response.css(price_path).extract_first()
        item['price'] = price.split("\t")[2].split("\xa0")[0]
        colors = response.css(colors_path).extract_first()
        item['colors'] = colors.split("\n")[1].split("\t")[8].split("/")
        item['detail'] = response.css(detail_path).extract_first()
        features = response.css(features_path).extract()
        if len(features) == 1:
            features[0] = features[0].split("\n")[1].split("\t")[4]
        item['features'] = features
        materials = response.css(materials_path).extract()
        if len(materials) == 1:
            materials[0] = materials[0].split("\n")[1].split("\t")[4]
        item['materials'] = materials
        item['image_urls'] = response.css(image_path).extract()
        yield item
