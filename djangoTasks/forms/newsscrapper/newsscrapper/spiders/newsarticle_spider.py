import scrapy

from newsscrapper.items import NewsArticleItem


class NewsArticleSpider(scrapy.Spider):
    name = "newsscrapper"
    start_urls = ['https://www.thenews.com.pk/latest-stories']

    def parse(self, response):
        link_selector = '//div[@class="writter-list-item-story"]/a/@href'
        links = response.xpath(link_selector).extract()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_details
            )

    def parse_details(self, response):

        article = NewsArticleItem()

        title_selector = '//div[@class="detail-heading"]/h1/text()'
        category_name_selector = '//div[@class="category-name"]/h2/text()'
        category_source_selector = '//div[@class="category-source"]/text()'
        date_selector = '//div[@class="category-date"]/text()'
        tags_selector = '//div[@class="detail-inthisstory"]/ul//li//h5//a/text()'
        details_selector = '//div[@class="story-detail"]/p//text()'

        title = response.xpath(title_selector).extract()
        category_name = response.xpath(category_name_selector).extract()
        category_source = response.xpath(category_source_selector).extract()
        date = response.xpath(date_selector).extract()
        tags = response.xpath(tags_selector).extract()
        details = response.xpath(details_selector).extract()
        article['title'] = " ".join(title).strip()
# If detail-heading is empty string then extract top image heading as title
        if article['title'] is '':
            title = response.xpath(
                '//div[@class="top-header"]/img/@title').extract()

        article['title'] = " ".join(title).strip()
        article['category_name'] = " ".join(category_name).strip()
        article['category_source'] = " ".join(category_source).strip()
        article['publication_date'] = " ".join(date).strip()
        article['tags'] = ", ".join(tags).strip()
        article['detail'] = " ".join(details).strip()

        yield article
