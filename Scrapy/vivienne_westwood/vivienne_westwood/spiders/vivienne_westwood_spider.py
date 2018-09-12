import scrapy
from scrapy.spider import CrawlSpider


class VivienneWestwoodSpider(CrawlSpider):
    name = "viviennewestwood"
    items_set = []

    start_urls = [
        'https://www.viviennewestwood.com'
    ]

    def parse(self, response):
        menu_items = response.css('.b-menu_category-item a::attr(href)').extract()

        for menu_item in menu_items:
            yield scrapy.Request(response.urljoin(menu_item), callback=self.parse_menu)

    def parse_menu(self, response):
        item_link_list = response.css('.b-product_tile_container a::attr(href)').extract()
        for item_link in item_link_list:
            yield scrapy.Request(response.urljoin(item_link), callback=self.parse_product)
        load_more_link = response.css('.l-search_result-paging-controls-links a::attr(href)').extract_first()
        if load_more_link:
            yield scrapy.Request(response.urljoin(load_more_link), callback=self.parse_menu)

    def parse_product(self, response):
        retailer_sku = response.css('.b-product_master_id::text').extract_first().strip().split(":")[1]
        if retailer_sku in self.items_set:
            return
        self.items_set.append(retailer_sku)
        text = response.css('.js-gtm-do_not_wrap::text').extract_first().split("=")[2].split(",")
        colors_list = response.css('.b-swatches_color-item  a::attr(href)').extract()
        requests = []
        if colors_list:
            for color in colors_list:
                requests.append(
                    scrapy.Request(response.urljoin(color + "&format=ajax"),
                    callback=self.parse_product_size)
                )
        else:
            requests.append(
                scrapy.Request(response.url + "&format=ajax",
                callback=self.parse_product_size)
            )
        item = {

            'retailer_sku': retailer_sku,
            'uuid': 'null',
            'gender': text[12].split(":")[1].strip('"'),
            'category': text[11].split(":")[1].strip('"').split("-"),
            'industry': 'null',
            'brand': text[16].split(":")[1].strip('"'),
            'url': response.url,
            'market': 'UK',
            'retailer': 'viviennewestwood-uk',
            'name': response.css('.b-product_container-title span::text').extract_first(),
            'description': self.get_product_description(response),
            'care': self.get_clean_data(response, '.b-product_material::text'),
            'image_urls': response.css('ul.js-thumbnails img::attr(src)').extract(),
            'skus': {},
            'price': response.css('div.b-product_price h4::text').extract_first().replace('\n', '').strip(),
            'currency': text[3].split(":")[1].strip('"'),
            'spider_name': self.name,
            'meta': {'requests': requests}
        }
        return self.next_request_or_item(item)

    def parse_product_size(self, response):
        item = response.meta.pop('item')
        currency = item['currency']
        size_list = response.css('.b-swatches_size a::text').extract()
        size_list = [size.strip() for size in size_list if size.strip()]
        unavailable_size_list = response.css('.js-unselectable a::text').extract()
        unavailable_size_list = [size.strip() for size in unavailable_size_list if size.strip()]
        color = response.css('.b-swatches_color-item-selected a::attr(title)').extract_first()
        color = color if color else ""
        price = response.css('.b-product_price h4::text').extract_first()
        price = price.replace('\n', '').strip()

        for size in size_list:
            item_sku_key = color + "_" + size if color else size
            item['skus'][item_sku_key] = {
                "price": price,
                "currency": currency,
                "size": size
            }
            if color:
                item['skus'][item_sku_key].update({"colour": color})

            if size in unavailable_size_list:
                item['skus'][item_sku_key].update({"out_of_stock": "true"})

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if item['meta'].get('requests', []):
            request = item['meta']['requests'].pop()
            request.meta.update({'item': item})
            return request
        elif 'requests' in item['meta']:
            item.pop('meta')

        return item

    def get_clean_data(self, response, selector):
        raw_data = response.css(selector).extract()
        clean_data = ','.join(map(str, raw_data)).strip("\n\t")

        return clean_data

    def get_product_description(self,response):
        description = self.get_clean_data(response, '.b-product_long_description::text')
        product_details = self.get_clean_data(response, '.b-care_details-content::text')
        retailer_sku = response.css('.b-product_master_id::text').extract_first().strip().split(":")[1]
        product_description = []
        product_description.append(description)
        product_description.append(retailer_sku)
        product_description.append(product_details)

        return product_description
