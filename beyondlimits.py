import scrapy
from scrapy_spider.items import BeyondLimitItem


class BeyondlimitsSpider(scrapy.Spider):
    name = 'beyondlimitspider'
    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/Sales/Men/#bb_artlist',
                  'https://www.beyondlimits.com/Sales/Women/']

    def get_product_name(self, response):
        return response.css('header > h1::text').getall()

    def get_product_size(self, response):
        product_size = response.css('option::text').getall()
        if product_size:
            del[product_size[0]]
        return product_size

    def get_product_gender(self, response):
        return response.css('a > strong::text').getall()

    def get_product_description(self, response):
        return response.css(' header > p::text').getall()

    def get_retailer_sku(self, response):
        return response.css('header > small > span::text').getall()

    def get_image_urls(self, response):
        product_images = response.css('ul a::attr(href)').extract()
        return [image for image in product_images if 'jpg' in image]

    def get_product_care(self, response):
        return response.css('#description > ul > li::text').extract()

    def get_product_url(self, response):
        return response.css('div > a.flag.en.selected::attr(href)').extract()

    def get_language(self, response):
        return response.css('a.flag.en.selected::attr(title)').extract_first()

    def get_product_brand(self, response):
        return response.css('a > img::attr(title)').extract_first()

    def get_product_category(self, response):
        return response.css('a > strong::text').extract_first()

    def parse_size(self, response):

        complete_product = response.meta["complete_product"]
        skus = response.meta.get("skus", [])
        current_sku = {}
        price_currency = response.css('div.bb_art--pricecontent > div > span::text').extract_first()
        price_currency_data = price_currency.split(" ")
        current_sku["price"] = price_currency_data[0]
        current_sku["currency"] = price_currency_data[1]
        current_sku["sku"] = response.css('#bb-variants--0 > option[selected]::text').extract_first()
        current_sku["sku_id"] = response.css('header > small > span::text').extract_first()

        skus.append(current_sku)

        next_size = response.xpath('//select[@name="varselid[0]"]/option[@selected]/following-sibling::option[1]/@value').get()
        if next_size:
            yield scrapy.FormRequest.from_response(
                response=response,
                formxpath='//form[@class="js-oxWidgetReload"]',
                formdata={
                    'varselid[0]': response.xpath('//select[@name="varselid[0]"]/option[@selected]/following-sibling::option[1]/@value').get()
                },
                callback=self.parse_size,
                meta={'complete_product': complete_product, 'skus': skus},
                dont_filter=True,
                headers={
                    'X-Requested-With': "XMLHttpRequest",
                },
            )
        else:
            complete_product["skus"] = skus
            yield complete_product

    def parse(self, response):
        complete_product = BeyondLimitItem(
            name=self.get_product_name(response),
            size=self.get_product_size(response),
            gender=self.get_product_gender(response),
            description=self.get_product_description(response),
            retailer_sku=self.get_retailer_sku(response),
            image=self.get_image_urls(response),
            care=self.get_product_care(response),
            lang=self.get_language(response),
            brand=self.get_product_brand(response),
            category = self.get_product_category(response),
            url=self.get_product_url(response),
        )

        links = response.css('div.pictureBox.gridPicture.bb_product--imgwrap > a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse)

        next_page = response.css('a.bb_pagination--item::attr(href)').getall()
        for link in next_page:
            yield scrapy.Request(link, callback=self.parse)

        yield scrapy.FormRequest.from_response(
            response=response,
            formxpath='//form[@class="js-oxWidgetReload"]',
            formdata={
                'varselid[0]': response.xpath('//select[@name="varselid[0]"]/option[position() > 1]/@value').get()
            },
            callback=self.parse_size,
            meta={'complete_product': complete_product},
            dont_filter=True,
            headers={
                'X-Requested-With': "XMLHttpRequest",
            }
        )
