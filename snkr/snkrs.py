import scrapy
from ..items import SnkrsItem


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://snkrs.com/en/']

    def parse(self, response):
        men_link = response.css('li.li-niveau1.advtm_menu_2.sub > a.a-niveau1::attr(href)').extract_first()
        women_link = response.css('li.li-niveau1.advtm_menu_3.sub > a.a-niveau1::attr(href)').extract_first()
        skate = response.css('li.li-niveau1.advtm_menu_4.menuHaveNoMobileSubMenu' +
        ' > a.a-niveau1::attr(href)').extract_first()
        life_style = response.css('li.li-niveau1.advtm_menu_5.menuHaveNoMobileSubMenu' +
        ' > a.a-niveau1::attr(href)').extract_first() 
        if men_link:
        	print(men_link)
        	yield response.follow(men_link, callback=self.men_list_page)
        if women_link:
            print(women_link)
            yield response.follow(women_link, callback=self.women_list_page)
        if skate:
            print(skate)
            yield response.follow(skate, callback=self.skate_list_page)
        if life_style:
            print(life_style)
            yield response.follow(life_style, callback=self.life_style_list_page)

    def men_list_page(self,response):
    	urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
    	for url in urls:
    		print(url)
    		yield response.follow(url, callback=self.product_page)

    def women_list_page(self,response):
        urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
        for url in urls:
            print(url)
            yield response.follow(url, callback=self.product_page)

    def skate_list_page(self,response):
        urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
        for url in urls:
            print(url)
            yield response.follow(url, callback=self.product_page)

    def life_style_list_page(self,response):
        urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
        for url in urls:
            print(url)
            yield response.follow(url, callback=self.product_page)
    def get_retailer_sku(self,response):
        retailer_sku = response.css('div.nosto_product > span.product_id::text').get()
        return retailer_sku

    def get_brand(self,response):
        brand = response.css('div.nosto_product > span.brand::text').get()
        return brand

    def get_category(self,response):
        category = response.css('div.nosto_product > span.category::text').re(r'Men .*')
        return category

    def get_desciption(self,response):
        description = response.css('div.rte > p::text').extract()
        return description

    def get_gender(self,response):
        gender = response.css('div.nosto_product > span.category').re_first(r'Men')
        return gender

    def get_url(self,response):
        url = response.css('div.nosto_product > span.url::text').get()
        return url

    def get_name(self,response):
        name = response.css('div.nosto_product > span.name::text').get()
        return name
        
    def get_image_urls(self,response):
        image_urls = response.css('div.nosto_product > .image_url::text').extract()
        image_urls.extend(response.css('div.nosto_product > .alternate_image_url::text').extract())

    def product_page(self,response):
    	items = SnkrsItem()

        items['retailer_sku'] = self.get_retailer_sku(response)
        items['brand'] = self.get_brand(response)
        items['category'] = self.get_category(response)
        items['description'] = self.get_desciption(response)
        items['gender'] =  self.get_gender(response)
        items['url'] = self.get_url(response)
        items['name'] = self.get_name(response)
        items['image_urls'] = self.get_image_urls(response)
        shoes_name = items['name']
        for sizes in response.css('span.units_container > .size_EU::text').extract():
            items['skus'] = {shoes_name + "_" + sizes:
            {
                "colour" : shoes_name,
                "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                "price" : response.css('div.nosto_product > span.price::text').get(),
                "size" : sizes
            },
            }
    	yield items
