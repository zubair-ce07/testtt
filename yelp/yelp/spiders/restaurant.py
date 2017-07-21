import scrapy

class Restaurant(scrapy.Spider):
    name = "restaurant"
    start_urls = [
                    'https://www.yelp.com/search?attrs=NewBusiness&find_loc=New+York%2C+NY'
                ]

    def parse(self, response):
        for ad in response.css('.biz-listing-large'):
            title = ad.css('.biz-name span::text').extract()
            speciality = ad.css('.category-str-list a::text').extract()
            district = ad.css('.neighborhood-str-list::text').extract()
            address = ad.css('address::text').extract()
            phone = ad.css('.biz-phone::text').extract()
            yield {
                    'title': title,
                    'speciality': speciality,
                    'district': district,
                    'address': address,
                    'phone': phone
            }
            next_page = response.css('.current + div a::attr(href)').extract_first()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
