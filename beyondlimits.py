from datetime import datetime
from scrapy import Spider
from scrapy import Request
from scrapy_spider.items import BeyondLimitItem


class CrawlSpider(Spider):
    name = 'beyondlimitspider'
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/Sales/Men/#bb_artlist',
        'https://www.beyondlimits.com/Sales/Women/'
    ]
    retailer = 'beyondlimits-gb'

    def get_product_name(self, response):
        return response.css('.bb_art--header h1::text').get()

    def get_product_description(self, response):
        return response.css('header.bb_art--header p::text').get()

    def get_retailer_sku(self, response):
        return response.css('small.bb_art--artnum span::text').get()

    def get_image_urls(self, response):
        return response.css('a.bb_pic--navlink::attr(href)').getall()

    def get_product_care(self, response):
        return response.css('.bb_boxtxt--content ul>li:not(:first-child)::text').getall()

    def get_product_category(self, response):
        return response.css('span.bb_breadcrumb--item.is-last strong::text').get()

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d')}" \
               f"-{int(datetime.timestamp(datetime.now()))}-medp"

    def get_product_sku(self, response):
        male_size_id = {'S': 1, 'M': 2, 'L': 3, 'XL': 4, 'XXL': 5}
        female_size_id = {'XS': 1, 'S': 2, 'M': 3, 'L': 4}
        sku = {}
        product_size = response.css('option:not(:first-child)::text').getall()
        if product_size:
            product_price = response.css('.price span::text').get()
            product_currency = response.css('div.price meta::attr(content)').get()
            product_sku = response.css('small.bb_art--artnum span::text').get()
            color_extracted = response.css('.bb_boxtxt--content ul > li:first-child::text').get()
            color = color_extracted.split(" ", 1)
            for sizes in product_size:
                if self.get_gender(response) == 'Women':
                    color_size = int(product_sku[3:]) + female_size_id[sizes]
                else:
                    color_size = int(product_sku[3:]) + male_size_id[sizes]
                current_sku = {str(product_sku[:3]) + str(color_size): {'price': product_price,
                                                                        'currency': product_currency,
                                                                        'size': sizes,
                                                                        'color': color[1]}}
                sku.update(current_sku)
        return sku

    def get_gender(self, response):
        product_url = response.css('a.flag.en.selected::attr(href)').get()
        if 'Men' in product_url:
            return 'Men'
        else:
            return 'Women'

    def parse(self, response):
        links = response.css('.bb_product--imgwrap > a::attr(href)').getall()
        for link in links:
            yield Request(link, callback=self.parse_of_clothing_item)
        next_page = response.css('a.bb_pagination--item::attr(href)').getall()

        for link in next_page:
            yield Request(link, callback=self.parse)

    def parse_of_clothing_item(self, response):
        garment = BeyondLimitItem()
        garment['name'] = self.get_product_name(response)
        garment["sku"] = self.get_product_sku(response)
        garment["gender"] = self.get_gender(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = self.get_image_urls(response)
        garment["care"] = self.get_product_care(response)
        garment["lang"] = response.css('a.flag.en.selected::attr(title)').get()
        garment["brand"] = response.css('.ft_logo--inner img::attr(title)').get()
        garment["category"] = self.get_product_category(response)
        garment["url"] = response.css('a.flag.en.selected::attr(href)').get()
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = 'GB'
        garment["retailer"] = self.retailer
        yield garment
