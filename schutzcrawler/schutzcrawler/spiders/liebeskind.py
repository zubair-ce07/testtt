import scrapy
import copy
import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import schutzcrawler.items as items
from schutzcrawler.PriceExtractor import PriceExtractor
from schutzcrawler.DescriptionExtractor import DescriptionExtractor


class ParseSpider(CrawlSpider):
    name = "liebeskind-parse"
    allowed_domains = ['liebeskind-berlin.com']
    price_extractor = PriceExtractor()
    description_extractor = DescriptionExtractor()

    def parse(self, response):
        product = items.LiebeskindProductItem()

        product["url"] = response.url.split('?')[0]
        product["retailer_sku"] = self.retailer_sku(response)
        product["lang"] = self.lang(response)
        product["gender"] = "women"
        product["retailer"] = "leibskind-de"
        product["category"] = self.category(response)
        product["url"] = response.url.split('?')[0]
        product["market"] = self.market(response)
        product["url_original"] = response.url
        product["name"] = self.product_name(response)
        product["price"] = self.price(response)
        product["spider_name"] = self.name
        product["description"] = self.description_extractor.description(response)
        product["care"] = self.description_extractor.care(response)
        product["trail"] = response.meta.get('trail' , [])
        product["skus"] = self.skus(response)
        product["image_urls"] = []
        product["requests"] = []

        color_range_css = '.filter__colors__boxes input'
        color_range = response.css(color_range_css)
        for color in color_range:
            quantity = response.xpath('//input[@name="Quantity"]/@value').extract_first()
            rendering_type = response.xpath('//input[@name="renderingType"]/@value').extract_first()
            page_type = response.xpath('//input[@name="pageType"]/@value').extract_first()
            fit_guide_name = response.xpath('//input[@name="fitguideName"]/@value').extract_first()
            fit_guide_use = response.xpath('//input[@name="fitguideUse"]/@value').extract_first()
            vogel_data = response.xpath('//input[@name="stickvogelData"]/@value').extract_first()
            variant_name = color.css('input::attr(name)').extract_first()
            variant_value = color.css('input::attr(value)').extract_first()
            pid = response.xpath('//input[@name="pid"]/@value').extract_first()
            cgid = response.xpath('//input[@name="cgid"]/@value').extract_first()
            data_action = color.css('input::attr(data-action)').extract_first()

            url_next = (f"https://de.liebeskind-berlin.com/on/demandware.store/Sites-liebeskindEU-Site/en/SPV-Dispatch?"
                        + f"view=ajax&Quantity={quantity}&renderingType={rendering_type}&pageType={page_type}&"
                        + f"fitguideName={fit_guide_name}&fitguideUse={fit_guide_use}&stickvogelData={vogel_data}&"
                        + f"{variant_name}={variant_value}&pid={pid}&cgid={cgid}&{data_action}={data_action}")
            product["requests"].append(scrapy.Request(url=url_next, callback=self.parse_image_urls, dont_filter=True, meta={'item':product}))

        if product["requests"]:
            yield product["requests"].pop()
        else:
            yield product

    def parse_image_urls(self, response):
        item = response.meta['item']
        image_css = '.pdp__media__slider__pager img::attr(src)'
        images = response.css(image_css).extract()
        images.extend(item["image_urls"])
        item["image_urls"] = set(images)
        if item["requests"]:
            yield item["requests"].pop()
        else:
            yield item
    
    def retailer_sku(self, response):
        retailer_sku_css = '.js-productvariations-swatchbase::attr(data-product)'
        return response.css(retailer_sku_css).extract_first()

    def lang(self, response):
        lang_xpath = '//div[@class="Lnewsletterbox__inputwrapper"]/input[@name="locale"]/@value'
        return response.xpath(lang_xpath).extract_first()

    def category(self, response):
        categories_css = '.breadcrumbs__category_name::text'
        return response.css(categories_css).extract()

    def market(self,response):
        market_xpath = '//div[@class="Lnewsletterbox__inputwrapper"]/input[@name="countryCode"]/@value'
        return response.xpath(market_xpath).extract_first()

    def product_name(self, response):
        return response.css('.ta_productName::text').extract_first()

    def price(self, response):
        priceextractor = PriceExtractor()
        return priceextractor.prices(response.css('.pdp__product-price ::text').extract())

    def skus(self, response):
        raw_colors = response.css('.filter__colors__boxes span::text').extract()
        colors = [c for c in raw_colors if re.match('^[a-zA-Z]+', c)]
        common_sku = self.price(response)
        skus = {}
        sizes = response.css('.js-productvariations-swatchbase-color a::attr(data-sizes)').extract_first()
        sizes = json.loads(sizes)

        for color, size in [(color,size) for color in colors for size in sizes]:
            sku = copy.deepcopy(common_sku)
            sku['color'] = color
            sku['size'] = size
            skus[f"{color}{size}"] = sku
        return skus


class LiebeskindSpider(CrawlSpider):
    name = 'liebeskind-crawl'
    allowed_domains = ['liebeskind-berlin.com']
    start_urls = ['http://de.liebeskind-berlin.com/']

    parser = ParseSpider()
    category_css = 'div.mainnav__level'
    pagination_css = '.pagination__btn--next'
    products_css = 'div.productlist__product .pdlist__image'

    rules = [Rule(LinkExtractor(restrict_css=[category_css, pagination_css]), callback='parse'),
             Rule(LinkExtractor(restrict_css=products_css), callback=parser.parse)]

    def parse(self, response):
        requests = list(super(LiebeskindSpider, self).parse(response))
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        
        #append all pagination links
        url = response.url.split('?')[0]
        pagination_xpath = '//span[@class="pagination__btn pagination__btn--next fakelink"]/@data-pagingparams'
        pagination = response.xpath(pagination_xpath).extract_first()
        if pagination:
            pagination = json.loads(pagination)
            for key, value in pagination.items():
                next_url = f"{url}?{key}={value}"
                requests.append(scrapy.Request(url=next_url, callback=self.parse))

        for request in requests:
            trail = copy.deepcopy(trail)
            request.meta['trail'] = trail
            yield request
