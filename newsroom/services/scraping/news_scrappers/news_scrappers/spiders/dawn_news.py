from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

from newsroom.settings import SPIDER_NAMES, DAWN_NEWS
from services.scraping.news_scrappers.news_scrappers.spiders.news_crawl_spider import NewsCrawlSpider


class DawnNewsSpider(NewsCrawlSpider):
    name = SPIDER_NAMES[DAWN_NEWS]
    custom_settings = {'DOWNLOAD_DELAY': 2}
    published_date_css = ['.template__header .story__time::text', ]
    title_css = ['.template__header .story__title .story__link::text', ]
    image_url_css = ['.template__main .media__item img::attr(src)', ]
    detail_css = ['.story__content p ::text', ]
    abstract_css = ['.story__content p:first-of-type ::text', ]
    category_css = ['[itemprop=articleSection]::attr(content)', ]
    news_source_css = ['[name=author]::attr(content)', ]

    newspaper_name = DAWN_NEWS
    source_url = 'https://www.dawn.com/'

    link_extractor = LxmlLinkExtractor(
        restrict_css=[".story__link"],
        allow=('www.dawn.com',),
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
