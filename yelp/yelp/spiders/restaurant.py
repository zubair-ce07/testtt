import scrapy



class Restaurant(scrapy.Spider):
    name = "restaurant"
    start_urls = [
                    'https://www.yelp.com/search?attrs=NewBusiness&find_loc=New+York%2C+NY'
                ]


    def parse(self, response):
        for ad in response.css('div.biz-listing-large'):
            title = ad.css('a.biz-name span::text').extract()
            speciality = ad.css('span.category-str-list a::text').extract()
            district = ad.css('span.neighborhood-str-list::text').extract()
            address = ad.css('address::text').extract()
            phone = ad.css('span.biz-phone::text').extract()
            yield {
                    'title': title,
                    'speciality': speciality,
                    'district': district,
                    'address': address,
                    'phone': phone
            }
            next_page = response.css('div.current + div a::attr(href)').extract_first()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
