import re

from product_item import Product
from  scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SheegoSpider(CrawlSpider):
    name = 'Sheego.de'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de/', ]
    download_delay = 1
    rules = (

        Rule(LinkExtractor(deny=(
            'mein-konto.*', 'meine-bestellungen.*', 'meine-buchungen.*', 'meine-wunschliste.*', 'mein-newsletter.*',
            'mein-adressbuch.*'),
            restrict_css=['section.cj-mainnav.mainnav--top']), callback='parse_item_and_links'),
    )

    def parse_start_url(self, response):
        list(self.parse_item_and_links(response))
        list(self.parse_and_recurse(response))

    def parse_item_and_links(self, response):
        return self.parse_item(response)

    def parse_and_recurse(self, response):
        yield self.parse(response)

    def parse_item(self, response):
        if not response.meta.has_key('page_visited'):
            max_page_number = response.css('span.paging__btn+span.l-ph-10::text').extract()
            max_page_numbers = re.findall(r'\b\d+\b', str(max_page_number))
            if max_page_numbers:
                page_urls = ['{0}/?pageNr={1}'.format(response.url, page) for page in
                             range(1, int(max_page_numbers[0]) + 1)]
                for page in page_urls:
                    request = Request(page, callback=self.parse_item)
                    request.meta['page_visited'] = True
                    yield request

        urls = []
        selectors = response.css('section.c-product.js-product-box.js-ff-tracking.js-unveil-plbox.at-product-box')
        for selector in selectors:
            for item_url in selector.css('div.colorspots__wrapper a::attr(data-ads)').extract():
                urls.append("https://www.sheego.de{0}".format(item_url))
            if urls:
                url = urls.pop(0)
                request = Request(url, callback=self.parse_product)
                request.meta['next_color_urls'] = urls
                yield request

    def parse_product(self, response):
        item = Product()
        item['brand'] = self.parse_brand(response)
        item['care'] = self.parse_care(response)
        item['category'] = self.parse_category(response)
        item['description'] = self.parse_description(response)
        item['gender'] = self.parse_gender(response)
        item['image_urls'] = []
        item['skus'] = dict()
        item['name'] = self.parse_name(response)
        item['retailer_sku'] = self.parse_retailer_sku(response)
        item['url_original'] = self.parse_url(response)
        response.meta['item'] = item
        item['image_urls'] = self.update_image_urls(item['image_urls'], response)
        item['skus'] = self.get_skus(response)

        next_color_urls = response.meta['next_color_urls']
        if not next_color_urls:
            yield item
        else:
            next_color_page_url = next_color_urls.pop(0)
            request = Request(next_color_page_url, callback=self.parse_next_color_items, dont_filter=True, priority=10)
            request.meta['item'] = item
            request.meta['next_color_urls'] = next_color_urls
            yield request

    def parse_next_color_items(self, response):
        next_color_urls = response.meta['next_color_urls']
        item = response.meta['item']
        item['url'] = self.parse_url(response)
        item['image_urls'] = self.update_image_urls(item['image_urls'], response)
        item['skus'] = self.get_skus(response)
        print(item)
        if not next_color_urls:
            yield item
        else:
            next_color_page_url = next_color_urls.pop(0)
            request = Request(next_color_page_url, callback=self.parse_next_color_items, dont_filter=True, priority=10)
            request.meta['item'] = item
            request.meta['next_color_urls'] = next_color_urls
            yield request

    def parse_brand(self, response):
        return "Sheego"

    def parse_care(self, response):
        return self.remove_whitespace(response.css('div.l-mt-10 template::text').extract())

    def parse_category(self, response):
        return response.css('input.js-econda-breadcrumb::attr(data-econda-categorypath)').extract_first()

    def parse_description(self, response):
        return response.css('div.at-dv-artDes.l-pr-10 p::text').extract_first()

    def parse_gender(self, response):
        return self.remove_whitespace(response.css('td.p-details__material__left+td::text').extract_first())

    def parse_image_urls(self, response):
        return response.css('div.p-details__image__main.l-hidden-xs.l-hidden-s.l-hidden-sm a::attr(href)').extract()

    def parse_name(self, response):
        return response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first().split(',')[2].split(":")[1]

    def parse_retailer_sku(self, response):
        return response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first().split(',')[1].split(":")[1]

    def check_if_out_of_stock(self, response):
        return response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first().split(',"')[4].find("Not")

    def parse_color(self, response):
        return self.remove_whitespace(response.css(
            'span.colorspots__item.cj-active.js-click-variant.at-qs-color-sel::attr(title)').extract_first())

    def parse_currency(self, response):
        return "Euro"

    def parse_price(self, response):
        return self.remove_whitespace(
            response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first().split(',"')[6].split(':')
            [1])

    def parse_available_sizes(self, response):
        sizes = response.css('section.js-variantSelector.size div.l-hidden-xs.l-hidden-s div::text').extract()
        disable_sizes = response.css(
            'section.js-variantSelector.size div.l-hidden-xs.l-hidden-s div[class$="disabled "]::text').extract()
        return [size for size in sizes if size not in disable_sizes]

    def get_skus(self, response):
        skus = response.meta['item']['skus']
        color_key_part = self.parse_color(response)
        sizes_of_item = self.parse_available_sizes(response)
        for size in sizes_of_item:
            item_characterstics = dict(
                colour=color_key_part,
                currency=self.parse_currency(response),
                price=self.parse_price(response)
            )
            if self.check_if_out_of_stock(response) > 0:
                item_characterstics['OutOfStock'] = "True"
            key = self.get_key(color_key_part, size)
            item_characterstics['size'] = size
            skus[key] = item_characterstics
        return skus

    def get_key(self, key_part, size):
        return u"{0}_{1}".format(key_part, size)

    def parse_url(self, response):
        return response.url

    def update_color_field(self, skus, response):
        for value in skus.values():
            value['colour'].append(self.parse_color(response))
        return skus

    def update_image_urls(self, image_urls, response):
        image_urls.append(self.parse_image_urls(response))
        return image_urls

    def remove_whitespace(self, d_text):
        clean_text = ""
        for text in d_text:
            text = text.replace(" ", "")
            text = text.replace("\\n", "")
            clean_text += text
        return clean_text
