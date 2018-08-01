import scrapy


class AmazonDepartmentsSpider(scrapy.Spider):
    """
    Generates a spider that crawls through https://www.amazon.com/gp/site-directory/
    and gets all the departments, their products and their links present in href
    """

    name = 'amazon_departments_spider'
    start_urls = [
        'https://www.amazon.com/gp/site-directory/'
    ]

    def parse(self, response):
        for category_sel in response.css('.fsdDeptBox'):
            department_title = category_sel.css('h2.fsdDeptTitle::text').extract_first()
            entities = []

            for raw_url in category_sel.css('a'):
                product_map = {}
                product_map['title'] = raw_url.css('::text').extract_first()
                product_map['link'] = raw_url.css('::attr("href")').extract_first()
                entities.append(product_map)

            yield {department_title: entities}
