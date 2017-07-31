import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
from newsroom.settings import SPIDER_NAMES, THE_NEWS

from news.news_scrappers.news_scrappers.spiders.news_crawl_spider import NewsCrawlSpider


class TheNewsSpider(NewsCrawlSpider):
    newspaper_name = THE_NEWS
    source_url = 'https://www.thenews.com.pk/'
    name = SPIDER_NAMES[THE_NEWS]
    published_date_css = ['.category-date::text', ]
    title_css = ['[property="og:title"]::attr(content)',
                 '.top-header h1::text',
                 'title::text',
                 ]
    image_url_css = ['[property="og:image"]::attr(content)', ]
    detail_css = ['.story-detail > p::text', ]
    abstract_css = ['[property="og:title"]::attr(content)', ]
    category_css = ['.category-name ::text', ]
    news_source_css = ['.category-source ::text',
                       '.category-source::text',
                       ]

    page = 0

    link_extractor = LxmlLinkExtractor(
        restrict_css=['.writter-list-item-story'],
    )
    rules = (

        Rule(
            link_extractor,
            callback='parse_news_detail',
            follow=True
        ),
    )

    start_urls = [
        'https://www.thenews.com.pk/latest-stories/0',
    ]

    def parse_news_detail(self, response):
        yield super(TheNewsSpider, self).parse_news_link(response)

        self.page += 1
        yield scrapy.Request('https://www.thenews.com.pk/latest-stories/' + str(self.page))
