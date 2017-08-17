import re

import scrapy
from  scrapy.http import Request, FormRequest
from scrapy.linkextractors import LinkExtractor

from product_item import Product


class MotelSpider(scrapy.Spider):
    name = 'motelrocks'
    allowed_domains = ['motelrocks.com']
    start_urls = ['http://www.motelrocks.com', ]
    download_delay = 1

    def parse(self, response):
        if 'category_link_visited' not in response.meta:
            links = LinkExtractor(deny=['http://www.motelrocks.com/pages/Instagram.html'],
                                  restrict_css=['ul[id^="nav-menu"]']).extract_links(response)
            for link in links:
                request = Request(link.url, callback=self.parse)
                request.meta['category_link_visited'] = True
                yield request

        if 'page_link_visited' not in response.meta:
            catid = re.findall('catid.*,', response.text)
            if catid:
                categoryid = re.findall('\d+', catid[0])[0]
                pages = response.css(
                    'div.hide-for-small.show-for-medium-up.paging-title.large-3.medium-3.columns.left.text-left::text').extract_first()
                Totalpages = int(re.findall('\d+', pages)[0]) / 20 + 1
                for page in range(2, Totalpages + 1):
                    formdata = {
                        'isajax': '1',
                        'categoryid': categoryid,
                        'catid': categoryid,
                        'search_query': '',
                        'sortby': 'etailpreferred',
                        'invocation': 'page',
                        'page': u'' + str(page),
                        'pagesize': '20'
                    }
                    formrequest = FormRequest('http://www.motelrocks.com/categories_ajax.php', callback=self.parse,
                                              formdata=formdata)
                    formrequest.meta['page_link_visited'] = True
                    yield formrequest
        links = LinkExtractor(restrict_css=['div.Block.Panel']).extract_links(response)
        for link in links:
            yield Request(link.url, callback=self.parse_product)

    def parse_product(self, response):
        item = Product()
        item['brand'] = self.parse_brand(response)
        item['category'] = self.parse_category(response)
        item['description'] = self.parse_description(response)
        item['gender'] = self.parse_gender(response)
        item['image_urls'] = []
        item['skus'] = dict()
        item['name'] = self.parse_name(response)
        item['url'] = self.parse_url(response)
        item['url_original'] = self.parse_url(response)
        response.meta['item'] = item
        item['image_urls'] = self.update_image_urls(item['image_urls'], response)
        item['skus'] = self.get_skus(response)
        response.meta['next_color_urls'] = response.css('div[id^="colourswatch"] a::attr(href)').extract()
        next_color_urls = response.meta['next_color_urls']
        if response.url in next_color_urls:
            next_color_urls.remove(response.url)
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
        if not next_color_urls:
            yield item
        else:
            next_color_page_url = next_color_urls.pop(0)
            request = Request(next_color_page_url, callback=self.parse_next_color_items, dont_filter=True, priority=10)
            request.meta['item'] = item
            request.meta['next_color_urls'] = next_color_urls
            yield request

    def parse_brand(self, response):
        return "Motel Rocks"

    def parse_category(self, response):
        category = response.css('ul.breadcrumbs span:not([style])::text').extract()
        if category:
            return "/".join(category)

    def parse_description(self, response):
        description = response.css('div.content.active[id^="Details"] span::text').extract()
        if description:
            return "\n".join(description)

    def parse_gender(self, response):
        return "Female"

    def parse_image_urls(self, response):
        return response.css('meta[property^="og:image"]::attr(content)').extract_first()

    def parse_name(self, response):
        return response.css('ul.breadcrumbs span[style]::text').extract_first()

    def parse_color(self, response):
        raw_color = response.css('ul.breadcrumbs span[style]::text').extract_first()
        if raw_color:
            color = re.findall(r'in (.*?) by', raw_color, re.IGNORECASE)
            if color:
                return color[0]
            color = re.findall(r'in .*', raw_color, re.IGNORECASE)[0]
            if color:
                return color[0]

    def parse_currency(self, response):
        return response.css('form.custom.currency.large-2.left option[selected]::text').extract_first().split(' :')[0]

    def parse_price(self, response):
        price = response.css('em.ProductPrice.VariationProductPrice::text').extract_first()
        if price:
            return re.findall(r'\b\d+\b', price)[0]
        price = response.css('span.SalePrice::text').extract_first()
        return re.findall(r'\b\d+\b', price)[0]

    def parse_available_sizes(self, response):
        sizes = {'595': 'XXS', '593': 'XS', '586': 'S', '587': 'M', '594': 'L', '596': 'XL', '242': 'XS', '222': 'S',
                 '262': 'M', '282': 'L', '605': 'S/M', '606': 'M/L', '592': 'OS', '462': 'L', '583': 'XXS', '322': 'XS',
                 '342': 'S', '362': 'M', '302': 'XL'}
        all_sizes = [sizes[size] for size in response.css('li.sizeli::attr(rel)').extract() if size in sizes]
        unavailable_sizes = [sizes[size] for size in response.css('li.sizeli[instock^="0"]::attr(rel)').extract() if size in sizes]
        return all_sizes, unavailable_sizes

    def get_skus(self, response):
        skus = response.meta['item']['skus']
        color_key_part = self.parse_color(response)
        sizes_of_item, disable_sizes = self.parse_available_sizes(response)
        for size in sizes_of_item:
            item_characterstics = dict(
                colour=color_key_part,
                currency=self.parse_currency(response),
                price=self.parse_price(response)
            )
            if size in disable_sizes:
                item_characterstics['OutOfStock'] = True
            key = self.get_key(color_key_part, size)
            item_characterstics['size'] = size
            skus[key] = item_characterstics
        return skus

    def get_key(self, key_part, size):
        return u"{0}_{1}".format(key_part, size)

    def parse_url(self, response):
        return response.url

    def update_image_urls(self, image_urls, response):
        image_urls.append(self.parse_image_urls(response))
        return image_urls
