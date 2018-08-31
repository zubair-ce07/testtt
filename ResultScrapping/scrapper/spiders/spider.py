from __future__ import absolute_import
import scrapy
from scrapper.items import Student


class Spider(scrapy.Spider):
    name = "ResultSpider"
    roll_no = ""
    start_urls = [
        "http://pucit.edu.pk/images/results/bsets2018/checkResult.php",
    ]

    def parse(self, response):
        for self.roll_no in range(10000, 10002):
            yield scrapy.FormRequest.from_response(
                response,
                formid="login",
                formdata={"rollno": str(self.roll_no)},
                callback=self.parse_home_page
            )

    def parse_home_page(self, response):
        link = response.css("a::attr(href)").extract_first()
        url = (response.url+link).replace("checkResult.php", "")
        return scrapy.Request(url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        def get_value(expr):
            return response.css(expr).extract_first()

        student = Student()
        student['roll_no'] = get_value("tr td+td input::attr(value)")
        student['name'] = get_value("tr td+td[colspan]::text")
        student['father_name'] = get_value("tr td+td[colspan]::text")
        student['score'] = get_value("tr td+td[colspan] b::text")
        return student
