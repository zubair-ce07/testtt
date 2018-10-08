class PostScraper:

    selectors = {
        "title_selector": ".title::text",
        "published_date_selector": "time::attr(datetime)",
        "video_link_selector": ".bonus-video-card a::attr(href)",
        "author_name_selector": ".author_name a::text",
        "author_image_selector": ".author_image::attr(src)",
        "cover_image_selector": ".microcontent::attr(data-image)",
    }

    def __init__(self, response):
        self.response = response

    def get_title(self):
        title = self.response.css(self.selectors["title_selector"]).extract()
        return title[0] if title else None

    def get_author_details(self):
        if self.response:
            return {
                'image': self.get_author_image(),
                'name': self.get_author_name(),
            }

    def get_link(self):
        return self.response.url if self.response.url else None

    def get_published_date(self):
        date = self.response.css(
            self.selectors["published_date_selector"]
        ).extract()
        return date[0] if date else None

    def get_video_link(self):
        video = self.response.css(
            self.selectors["video_link_selector"]
        ).extract()
        return video[0] if video else None

    def get_author_name(self):
        name = self.response.css(
            self.selectors["author_name_selector"]
        ).extract()
        return name[0] if name else None

    def get_author_image(self):
        image = self.response.css(
            self.selectors["author_image_selector"]
        ).extract()
        return image[0] if image else None

    def get_cover_image(self):
        image = self.response.css(
            self.selectors["cover_image_selector"]
        ).extract()
        return image[0] if image else None

    def get_story_id(self):
        return self.response.meta["id"]
