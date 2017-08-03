from backend.news.models import Newspaper
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from services.scraping.news_scrappers.news_scrappers.items import NewsScrappersItem


class NewsCrawlSpider(CrawlSpider):
    published_date_css = list()
    title_css = list()
    image_url_css = list()
    detail_css = list()
    abstract_css = list()
    category_css = list()
    news_source_css = list()

    newspaper_name = 'Dawn News'
    source_url = 'https://www.dawn.com/'
    newspaper = None

    def parse_news_link(self, response):

        news_item = ItemLoader(item=NewsScrappersItem(), response=response)

        css_dictionary = self.get_css_dictionary()
        for key, value in css_dictionary.items():
            for css in value:
                news_item.add_css(key, css)

        news_item.add_value('source_url', response.url)

        return news_item.load_item()

    def get_newspaper(self):
        if not self.newspaper:
            self.newspaper = Newspaper.objects.filter(source_url=self.source_url).first()
        return self.newspaper

    def get_css_dictionary(self):
        css_dictionary = {
            'published_date': self.published_date_css,
            'title': self.title_css,
            'image_url': self.image_url_css,
            'detail': self.detail_css,
            'abstract': self.abstract_css,
            'category': self.category_css,
            'news_source': self.news_source_css
        }
        return css_dictionary
