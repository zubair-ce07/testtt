import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://news.ycombinator.com',
    ]

    def parse(self, response):
        for news_id in response.css("tr.athing::attr(id)").extract():
            news_selector='tr#{id} a.storylink::text'.format(id=news_id)
            score_selector='span#score_{id}::text'.format(id=news_id)
            news=response.css(news_selector).extract_first()
            score=response.css(score_selector).re(r'(\w+) points')
            score=score[0] if score else None

            yield {
                'news': news,
                'score': score,
            }

        next_page = response.css('a.morelink::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
