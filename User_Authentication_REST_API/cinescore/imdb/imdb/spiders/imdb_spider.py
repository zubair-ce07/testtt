from urllib.parse import urljoin, urlparse

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imdb.items import ImdbItem
from scrapy.utils.response import get_base_url


class ImdbSpider(CrawlSpider):
    name = "imdb"
    start_urls = [
        'http://www.imdb.com/search/title?title_type=tv_movie',
    ]
    # extractor = LinkExtractor(allow_domains="imdb.com", restrict_css="a.lister-page-next")
    # rules = (Rule(extractor, callback="parse_movie_list", follow=False),)

    def parse(self, response):
        # extractor = LinkExtractor(allow_domains="imdb.com", restrict_css="div.lister-list a")
        # rules = (Rule(extractor, callback="parse_movie", follow=True),)
        # print ("")
        movie_links = response.css("h3.lister-item-header a::attr('href')").extract()

        for movie_link in movie_links:
            complete_link = urljoin(response.url, movie_link)

            yield scrapy.Request(url=complete_link,
                                 callback=self.parse_movie)

        next_page = urljoin(response.url, response.css("a.lister-page-next::attr('href')").extract_first())

        if next_page:
            yield scrapy.Request(url=next_page,
                                 callback=self.parse)

    def parse_movie(self, response):
        movie = ImdbItem()
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        movie['base_url'] = domain
        movie['movie_id'] = response.css('meta[property="pageId"]::attr(content)').extract_first()
        movie['title'] = response.css('meta[property="og:title"]::attr(content)').extract_first()
        if response.css('span.rating::text').extract_first() is None:
            movie['rating'] = '0'
        else:
            movie['rating'] = response.css('span.rating::text').extract_first()
        movie['release_date'] = response.css('meta[itemprop="datePublished"]::attr(content)').extract_first()
        movie['content_rating'] = response.css('meta[itemprop="contentRating"]::attr(content)').extract_first()
        if response.css('div.summary_text::text').extract_first() is None:
            movie['plot'] = "Nil"
        else:
            movie['plot'] = response.css('div.summary_text::text').extract_first().strip()
        movie['poster'] = response.css("div.poster img[itemprop='image']::attr(src)").extract_first()
        movie['url'] = response.url
        movie['categories'] = response.css("span.itemprop[itemprop='genre']::text").extract()
        yield movie

