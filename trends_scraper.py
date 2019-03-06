import scrapy

from twitter.items import TwitterTrend, Tweets


class QuotesSpider(scrapy.Spider):
    name = "trendsScraper"

    def start_requests(self):
        urls = [
           'https://www.tweet247.net/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        topics = response.css("div.card-block div.row div.post-list")
        i = 1
        for topic in topics:
            trend = TwitterTrend()
            trend['id'] = i
            trend['title'] = topic.css("div.media-body span.post-title a::text").extract_first()
            trend['link'] = topic.css("div.media-body span.post-title a::attr(href)").extract_first()
            trend['title_img'] = topic.css("div.media-left a img::attr(src)").extract_first()
            i = i + 1
            yield response.follow(trend['link'], callback=self.parse_tweets, meta={'trend': trend})

    def parse_tweets(self, response):
        trend = response.meta['trend']
        tweets = response.css("div#tweet_list div.row")
        tweet_list = list()
        for tweet in tweets:
            tweet_item = Tweets()
            profile_pic = tweet.css("img.author::attr(src)").extract_first()
            username = tweet.css("span.author-name::text").extract_first()
            username = username.split("(")[0]
            tweet_data = tweet.css("p.feed-content::text").extract_first()

            tweet_item['profile_img'] = profile_pic
            tweet_item['username'] = username
            tweet_item['tweet_data'] = tweet_data
            tweet_item['trend_id'] = trend['id']
            tweet_list.append(tweet_item)
            trend['tweets'] = tweet_list
        if len(trend['tweets']) > 0:
            yield trend

