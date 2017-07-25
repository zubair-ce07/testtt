from scrapy.loader import ItemLoader
from news_scrappers.items import NewsScrappersItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class DawnNewsSpider(CrawlSpider):
    name = "dawn-news"
    date_css = '.template__header .story__time::text'
    title_css = '.template__header .story__title .story__link::text'
    img_url_css = '.template__main .media__item img::attr(src)'
    detail_css = '.story__content p ::text'
    abstract_css = '.story__content p:first-of-type ::text'

    news_paper = 'Dawn News'
    source_url = 'https://www.dawn.com/'

    link_extractor = LxmlLinkExtractor(
        restrict_css=[".story__link"],
        allow=('www.dawn.com'),
    )
    rules = (
        Rule(
            link_extractor,
            callback='parse_news_link',
            follow=True
        ),
    )

    start_urls = [
        'https://www.dawn.com',
    ]

    def parse_news_link(self, response):
        news_item = ItemLoader(item=NewsScrappersItem(), response=response)

        news_item.add_css('date', self.date_css)
        news_item.add_css('title', self.title_css)
        news_item.add_css('img_url', self.img_url_css)
        news_item.add_css('detail', self.detail_css)
        news_item.add_css('abstract', self.abstract_css)
        news_item.add_value('url', response.url)

        yield news_item.load_item()
