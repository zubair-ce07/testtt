from scrapy import exceptions


class DateTimeFilterMiddleware(object):

    def process_spider_input(self, response, spider):
        require_years = ['2018']
        if response.meta['type'] == "post":
            date = response.css("time::attr(datetime)").extract()
            split_date = date[0].split(' ')
            year = split_date[3]

            if year not in require_years:
                raise exceptions.CloseSpider("Year Exceeded")
