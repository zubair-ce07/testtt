import scrapy
import json

from go_sport.items import GoSportItem


class GoSpiderSpider(scrapy.Spider):
    name = 'go_sport'
    allowed_domains = ['go-sport.pl']
    start_urls = ['https://www.go-sport.pl/']

    def parse(self, response):
        category_links = response.xpath("//a[@class='level-top']/@href").extract()
        
        for link in category_links:
            yield response.follow(link, self.parse_products)

    def parse_products(self, response):
        item_links =  response.css("div.product-item h2 > a::attr(href)").extract()

        for link in item_links:
            yield response.follow(link, self.parse_item)
        
        next_page = response.css("a.action.next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_products)
        
    def parse_item(self, response):
        item = GoSportItem()

        item['retailer_sku'] = self._get_retailer_sku(response)
        item['gender'] = self._get_gender(response)
        item['category'] = self._get_category(response)
        item['brand'] = self._get_brand(response)
        item['url'] = self._get_url(response)
        item['name'] = self._get_name(response)
        item["description"] = self._get_description(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus'] = self._get_skus(response)

        return item

    def _get_retailer_sku(self, response):
        return response.css('span.product_id::text').extract_first()

    def _get_gender(self, response):
        genders = {'Mężczyzna': "Man", 'Kobieta': "Woman",
                   'Dziewczynka': "Girl", 'Chłopiec': "Boy",
                   'Dla dzieci': "Children"}
        gender = response.xpath('//span[@class="tags1"]\
                                /span[contains(., "gender")]/text()').extract_first().split(":")[-1]
        
        return genders.get(gender, "No")
    
    def _get_category(self, response):
        return response.css('span.categories span.category::text').extract()[0].split('/')[1:]
    
    def _get_brand(self, response):
        return response.css('span.nosto_product span.brand::text').extract_first()
    
    def _get_url(self, response):
        return response.css('span.nosto_product span.url::text').extract_first()
    
    def _get_name(self, response):
        return response.css('span.nosto_product span.name::text').extract_first()
    
    def _get_description(self, response):
        description = response.css('div.product.attribute.description div::text').extract_first()
        if description:
            return  description.split(".")

        return ["No Description"]
    
    def _get_image_urls(self, response):
        return response.css('span.alternate_image_url::text').extract()

    def _get_skus(self, response):
        skus_selector = response.css('span.skus span.nosto_sku')
        skus = []

        if not skus_selector:
            sku_item = {}
            sku_item['color'] = response.css('span.custom_fields span.color_web::text').extract_first()
            sku_item['price'] = response.css('span.nosto_product span.price::text').extract_first()
            sku_item['currency'] = response.css('span.nosto_product span.price_currency_code::text').extract_first()
            sku_item['size'] = "Single Size"
            sku_item['previous_price'] = response.css('span.nosto_product span.list_price::text').extract_first()
            sku_item['id'] = response.css('span.nosto_product span.product_id::text').extract_first()

            return [sku_item]
        
        megento_json = response.xpath('//script[contains(., "Magento_Swatches/js/swatch-renderer-custom")]/text()').extract_first()
        megento_json = json.loads(megento_json)
        skus_in_stock = megento_json["[data-role=swatch-options]"]\
                                    ["Magento_Swatches/js/swatch-renderer-custom"]\
                                    ["jsonConfig"]["optionPrices"]
        currency = response.css('span.nosto_product span.price_currency_code::text').extract_first()

        for sku in skus_selector:
            sku_item = {}
            sku_item['color'] = sku.css('span.color_web::text').extract_first()
            sku_item['price'] = sku.css('span.price::text').extract_first()
            sku_item['currency'] = currency
            sku_item['size'] = sku.css('span.size::text').extract_first()
            sku_item['previous_price'] = sku.css('span.list_price::text').extract_first()
            sku_item['id'] = sku.css('span.id::text').extract_first()

            if sku_item['id'] not in skus_in_stock:
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus
