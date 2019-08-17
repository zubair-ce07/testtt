from scrapy.spiders import CrawlSpider, Rule
from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from ..items import ClothesItem


class ClothesSpider(CrawlSpider):
    name = "soft_surroundings"
    allowed_domains = ['softsurroundings.com']
    start_urls = [
        'https://www.softsurroundings.com/clothing/sleepwear-robes/'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='.thmNm'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.mblMenuBar a')),
    )
    visited_retailer_skus = set()

    def parse_item(self, response):
        retailer_sku = self.extract_retailer_sku(response)
        if self.check_if_parsed(retailer_sku):
            return

        item = ClothesItem()
        item['url'] = response.url
        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand(response)
        item['currency'] = self.extract_currency(response)
        item['price'] = self.extract_price(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['requests'] = self.get_category_requests(response)
        yield self.get_request_or_item(item)

    def check_if_parsed(self, retailer_sku):
        if retailer_sku in self.visited_retailer_skus:
            return True
        else:
            self.visited_retailer_skus.add(retailer_sku)
            return False

    def get_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request
        else:
            del item['requests']
            return item

    def extract_retailer_sku(self, response):
        return response.css('#item::text').get()

    def extract_name(self, response):
        return response.css('#productName span::text').get()

    def extract_category(self, response):
        return response.css('.pagingBreadCrumb a::text').getall()

    def extract_brand(self, response):
        return response.css('title::text').get().split('| ')[-1]

    def extract_currency(self, response):
        return response.css('span[itemprop="priceCurrency"]::attr(content)').get()

    def extract_price(self, response):
        price = response.css('span[itemprop="price"]::text').get()
        return float(price) * 100 if price else None

    def extract_image_urls(self, response):
        return response.css('.alt_dtl img::attr(src)').getall()

    def extract_description(self, response):
        desc_all = response.css('.productInfo span[itemprop="description"] ::text').getall()
        description = []
        for desc in desc_all:
            description += [d.strip() for d in desc.split('.') if d.strip() != '']
        return description

    def extract_care(self, response):
        return response.css('#careAndContentInfo::text').getall()

    def get_category_requests(self, response):
        category_ids = response.css('#sizecat a::attr(id)').re('\d.+\d')
        cat_requests = []
        for cat_id in category_ids:
            self.visited_retailer_skus.add(cat_id)
            cat_requests.append(FormRequest(f'https://www.softsurroundings.com/p/{cat_id}',
                                            formdata={'sizecat_desc': cat_id}, callback=self.color_requests,
                                            dont_filter=True))
        if not cat_requests:
            cat_requests.append(
                FormRequest(f"https://www.softsurroundings.com/p/{self.extract_retailer_sku(response)}",
                            method='POST', callback=self.color_requests, dont_filter=True))
        return cat_requests

    def color_requests(self, response):
        item = response.meta['item']
        color_ids = response.css('.swatchlink img::attr(data-value)').getall()
        color_requests = []
        for c_id in color_ids:
            color_requests.append(FormRequest(f'{response.url}{c_id}', method='POST',
                                              callback=self.extract_skus, dont_filter=True))
        if not color_requests:
            color_requests.append(FormRequest(response.url, method='POST', callback=self.extract_skus,
                                              dont_filter=True))
        item['requests'] += color_requests
        yield self.get_request_or_item(item)

    def extract_skus(self, response):
        item = response.meta['item']
        skus = item.get('skus', [])
        skus += self.find_skus_selected(response)
        item['skus'] = skus
        yield self.get_request_or_item(item)

    def find_skus_selected(self, response):
        skus = []
        category = response.css('#sizecat a.sel::text').get() or 'ONE-CAT'
        selected_colour = response.css('.swatchlink img.sel') or response.css('#color .basesize ::text')
        colour_id = selected_colour.xpath('./@data-value').get() or selected_colour.get()
        common_sku = {
            'category': category,
            'colour': selected_colour.xpath('./@alt').get() or selected_colour.get(),
        }

        sizes_css = response.css('a.box.size') or response.css('#size .basesize')
        for size in sizes_css:
            sku = common_sku.copy()
            sku['size'] = size.xpath('./text()').get()
            sku['sku_id'] = f"{category}_{colour_id}_{sku['size']}"
            if size.css('.notavail'):
                sku['out-of-stock'] = True
            skus.append(sku)
        return skus
