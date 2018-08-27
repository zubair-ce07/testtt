import scrapy
import re
from urllib.parse import urljoin


class GithubSpider(scrapy.Spider):
    name = "githubspider"

    selectors = {
        "organizations_selector": '.tooltipped-n::attr(aria-label)',
        "annual_contribution_selector": ".js-yearly-contributions .f4::text",
        "latest_contribution_month_selector":
            ".profile-timeline-month-heading::text",
        "latest_contribution_year_selector":
            ".profile-timeline-month-heading .text-gray::text",
        "username_selector": ".p-name::text",
        "profile_image_selector": ".u-photo .avatar::attr(src)",
        "popular_repositry_selector": ".js-repo::text",
        "title_selector": "//title/text()",
    }

    def __init__(self, username="Qubad786"):
        url = urljoin("https://github.com", username)
        self.start_urls = [
            url
        ]

    def parse(self, response):
        Data = {
            'Name': self.get_user_name(response),
            'Popular Repositries': self.get_popular_repositries(response),
            'Profile Image': self.get_profile_image_url(response),
            'Title': self.get_title(response),
            'Link to': self.get_link_of_profile(response),
            'Organizations': self.get_organizations(response),
            'Latest Contribution Date':
                self.get_latest_contribution_date(response),
            'Number of Annual Contribution':
                self.get_annual_number_of_contributions(response),
        }
        yield Data

    def get_user_name(self, response):
        name = response.css(self.selectors["username_selector"]).extract()
        return name[0] if name else None

    def get_profile_image_url(self, response):
        url = response.css(self.selectors["profile_image_selector"]).extract()
        return url[0] if url else None

    def get_popular_repositries(self, response):
        popular_repositries = response.css(
            self.selectors["popular_repositry_selector"]
        ).extract()
        return popular_repositries if popular_repositries else None

    def get_title(self, response):
        title = response.xpath(self.selectors["title_selector"]).extract()
        return title[0] if title else None

    def get_link_of_profile(self, response):
        link = response.url
        return link if link else None

    def get_latest_contribution_date(self, response):
        month = response.css(
            self.selectors["latest_contribution_month_selector"]
        ).extract()
        year = response.css(
            self.selectors["latest_contribution_year_selector"]
            ).extract()
        if month and year:
            month = re.findall("[a-zA-Z]+", month[0])
            month = month[0]
            year = re.findall("[0-9]+", year[0])
            year = year[0]
            return " ".join([month, year])
        return None

    def get_annual_number_of_contributions(self, response):
        annual_contribution = response.css(
            self.selectors["annual_contribution_selector"]
        ).extract()
        if annual_contribution:
            annual_contribution = annual_contribution[0]
            annual_contribution = re.findall("[0-9]+", annual_contribution)
            annual_contribution = annual_contribution[0]
            return annual_contribution
        return None

    def get_organizations(self, response):
        organizations = response.css(
            self.selectors["organizations_selector"]
        ).extract()
        return organizations if organizations else None
