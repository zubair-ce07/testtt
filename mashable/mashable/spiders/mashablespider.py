import json
from urllib.parse import urlencode

import scrapy

from mashable.items import Story
from mashable.Utils.PostScraper import PostScraper


class Mashablespider(scrapy.Spider):
    name = 'MashableSpider'
    basic_url = "https://mashable.com/stories.json"
    starting_params = {
        "new_per_page": 20,
        "hot_per_page": 2,
        "rising_per_page": 3
    }
    url = f"{basic_url}?{urlencode(starting_params)}"
    sort_keys = {
        "hot_after": '',
        "new_after": '',
        "rising_after": '',
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            callback=self.parse,
            meta={
                'type': 'main'
            })

    def parse(self, response):
        unwanted_categories = ["channel"]
        data = json.loads(response.text)
        for category in data:
            if category not in unwanted_categories:
                for post in data[category]:
                    key = "{}_{}".format(category, "after")
                    self.sort_keys[key] = post["sort_key"]
                    if post["link"]:
                        yield scrapy.Request(
                            url=post["link"],
                            callback=self.parse_post,
                            meta={
                                'id': post['_id'],
                                'type': 'post'
                            }
                        )

        if data:
            key_params = {
                "new_after": self.sort_keys["new_after"],
                "hot_after": self.sort_keys["hot_after"],
                "rising_after": self.sort_keys["rising_after"]
            }
            yield scrapy.Request(
                url=f"{self.url}&{urlencode(key_params)}",
                meta={
                    'type': 'main'
                },
                callback=self.parse)

    def parse_post(self, response):
        Post = PostScraper(response)
        post_detail = {
            'story_id': Post.get_story_id(),
            'title': Post.get_title(),
            'link': Post.get_link(),
            'author': Post.get_author_details(),
            'published_date': Post.get_published_date(),
            'video_link': Post.get_video_link(),
            'cover_image': Post.get_cover_image(),
        }
        post = Story(post_detail)
        yield post
