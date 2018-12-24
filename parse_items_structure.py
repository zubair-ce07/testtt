import json


class ParseItems(object):
    def __init__(self):
        self.seen_ids = {}

    def extract_item(self, response):
        item = {}
        retailer_sku = self.extract_id(response)

        if self.is_new_item(retailer_sku):
            item['name'] = self.extract_name(response)
            item['retailer_sku'] = self.extract_id(response)
            item['care'] = self.extract_care(response)
            item['url'] = response.url
            item['spider_name'] = 'drmartens_au'
            item['market'] = self.extract_market()
            item['retailer'] = self.extract_retailer()
            item['brand'] = self.extract_brand()
            item['category'] = self.extract_category(response)
            item['description'] = self.extract_description(response)
            item['image_urls'] = self.extract_image_urls(response)
            item['trail'] = self.extract_trail(response)

            price_details = self.extract_price_details(response)
            item['price'] = self.extract_price(price_details)
            item['currency'] = self.extract_currency(price_details)
            item['skus'] = self.extract_skus(item, response)
            self.seen_ids[retailer_sku] = item

        return item

    def is_new_item(self, item):
        return item and item not in self.seen_ids

    def extract_trail(self, response):
        return response.meta.get('trail', [])

    def extract_currency(self, price_details):
        return price_details[1] if price_details else None

    def extract_price(self, price_details):
        return float(price_details[0]) * 100 if price_details else None

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] if title else title

    def extract_id(self, response):
        return response.css('.extra-product::attr(data-sku)').extract_first()

    def extract_name(self, response):
        return response.css('.product-info-main .page-title span::text').extract_first()

    def extract_care(self, response):
        care_content = response.css('.additional-attributes .large-4 .content-short-description p::text').extract()
        return [care.strip() for care in care_content if care.strip()]

    def extract_price_details(self, response):
        return response.css('.price-final_price meta::attr(content)').extract()

    def extract_category(self, response):
        category = response.css('.breadcrumbs .item strong::text').extract_first()
        return category.strip() if category else []

    def extract_description(self, response):
        description = []
        content = response.css('.additional-attributes .large-8 .content::text').extract_first()
        if content:
            description = [x.strip() for x in content.split('.') if x.strip()]

        return description

    def extract_image_urls(self, response):
        image_urls = []
        pattern = "//script[contains(., 'mage/gallery/gallery')]/text()"
        images_data = response.xpath(pattern).re('"data":.*}]')
        if images_data:
            images_data = json.loads(images_data[0].strip('"data": '))
            image_urls = [image['img'] for image in images_data]

        return image_urls

    def extract_skus(self, product, response):
        skus = []
        pattern = "//script[contains(.,'sizeRangesSort')]/text()"
        record = response.xpath(pattern).re('jsonConfig:{"attributes":({.*?}})')
        if not record:
            return record

        record = json.loads(record[0])
        options = [record[key]['options'] for key in record if record[key]['code'] == 'size']

        for option in options[0]:
            item = {}
            item['price'] = product['price']
            item['currency'] = product['currency']
            item['size'] = option['label']
            item['sku_id'] = f"{product['name']}_{option['label']}"
            item['size_available'] = True if option['products'] else False
            skus.append(item)

        return skus

    def extract_market(self):
        return 'AU'

    def extract_retailer(self):
        return 'drmartens-au'

    def extract_brand(self):
        return 'Dr. Martens'
