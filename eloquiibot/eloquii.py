# -*- coding: utf-8 -*-
import re
import scrapy
from eloquiibot.items import EloquiiProduct


class EloquiiSpider(scrapy.Spider):
    name = 'eloquii'
    allowed_domains = ['www.eloquii.com/']
    start_urls = ['http://www.eloquii.com/']

    def parse(self, response):
        sel_all_links = response.css("ul#nav_menu li")
        sel_all_links = sel_all_links[3:-3]
        cate_links = sel_all_links.css("ul li a::attr(href)").extract()

        for category in cate_links:
            yield scrapy.Request(
                url= response.urljoin(category),
                callback=self.parse_products,
                dont_filter=True
            )

    def parse_products(self, response):
        product_links = response.css("div.product-images a::attr(href)").extract()
        for product in product_links:
            yield scrapy.Request(
                url=product,
                callback=self.parse_product_details,
                dont_filter=True
            )
        
        # pagination
        #
        next_page_sel = response.css("div.row.justify-content-center.mt-5 div:nth-child(3)")
        if next_page_sel:
            next_page = next_page_sel.css("a::attr(href)").extract_first()
            if next_page:
                yield scrapy.Request(
                    url=next_page,
                    callback=self.parse_products,
                    dont_filter=True
                )


    def parse_product_details(self, response):
        product = EloquiiProduct()

        product["product_id"] = re.search(r'(\d+)\.html', response.url).group(1)
        product["brand"] = 'Eloquii'
        name = response.css("div.d-none.d-md-block h1::text").extract_first()
        name = name.strip('\r\t\n')
        product["name"] = name
        product["category"] = response.xpath("//*[@id='bt_pdp_main']/div[1]/div/span[3]/span/text()").extract_first()
        product["description"] = response.xpath("//*[@id='bt_pdp_main']/div[2]/div/div/div[3]/div/div[3]/div/div/div/div[3]/span/text()").extract_first()
        if not product["description"]:
            product["description"] = "description isn't available"
        product["url"] = response.url
        product["image_urls"] = self.get_img_urls(response)

        merch_info = response.css("h3.text-24.font-demi.mb-3.text-center::text").extract_first()
        if not merch_info:
            merch_info = re.findall(r'\'COMINGSOON\': (true|false)',response.text)
            if merch_info:
                merch_info = merch_info[0]
                merch_info = "Coming Soon"

        product["skus"] = {}

        if not merch_info:
            product["merch_info"] = "Available"
            product["skus"] = self.get_product_skus(response)
        else:
            product["merch_info"] = merch_info


        yield product


    def get_img_urls(self,response):
        raw_img_url = response.css("div.swiper-wrapper.productthumbnails div img::attr(src)").extract()
        img_url = [i.replace("small","large",1) for i in raw_img_url]
        img_url = [response.urljoin(i) for i in img_url]

        if not img_url:
            img_url = response.css("div.productimagearea img::attr(src)").extract_first()
            img_url = response.urljoin(img_url)

        return img_url

    def get_product_skus(self,response):
        skus = {}
        colors_list = response.css("ul.swatchesdisplay.list-inline li a::attr(title)").extract()
        sizes_list = response.css("div#product_detail_size_drop_down_expanded a::attr(title)").extract()
        sizes_list = sizes_list[1:]
        price = response.css("span.subprice-retail::text").extract_first()
        if not price:
            price = response.css("div.priceGroup span.text-pink::text").extract_first()

        currency = ''
        if price:
            currency = re.search(r'([^0-9.])',price).group(1)
            price = float(re.search(r'(\d+\.\d+)',price).group(1))

        for color in colors_list:
            for size in sizes_list:
                skus[color + '_' + size] = {
                        "color": color,
                        "currency": currency,
                        "price": price,
                        "size": size,
                        }
        return skus