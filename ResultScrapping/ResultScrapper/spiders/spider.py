from __future__ import absolute_import
import scrapy


class Spider(scrapy.Spider):
    name = "ResultSpider"
    roll_no = ""
    start_urls = [
        "http://pucit.edu.pk/images/results/bsets2018/checkResult.php",
    ]

    def parse(self, response):
        for self.roll_no in range(10000, 22801):
            yield scrapy.FormRequest.from_response(
                response,
                formid="login",
                formdata={"rollno": str(self.roll_no)},
                callback=self.parse_page1
            )

    def parse_page1(self, response):
        link = response.css("a::attr(href)").extract_first()
        url = (response.url+link).replace("checkResult.php", "")
        return scrapy.Request(url, callback=self.parse_page2)

    def parse_page2(self, response):
        roll_no = response.css("tr td+td input::attr(value)").extract_first()
        name = response.css("tr td+td[colspan]::text").extract_first()
        father_name = response.css("tr td+td[colspan]::text").extract()[1]
        score = response.css("tr td+td[colspan] b::text").extract_first()
        yield {
            'roll_no': roll_no,
            'name': name,
            'father_name': father_name,
            'score': score
        }
