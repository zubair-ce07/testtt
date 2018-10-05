# -*- coding: utf-8 -*-
import json
import csv

import scrapy
from scrapy.item import Item, Field
from w3lib.url import add_or_replace_parameter


class HeaderItem(Item):
    company_name = Field()
    header_name = Field()
    pie_charts = Field()
    yes_no = Field()
    user_answers = Field()


class ComparablySpiderSpider(scrapy.Spider):
    name = 'comparably_spider'
    allowed_domains = ['www.comparably.com']

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "DOWNLOAD_DELAY": 1.25
    }

    def start_requests(self):
        #company_names = self.read_company_names()
        company_names = ["Microsoft", "Netflix"]

        for company_name in company_names:
            url = "https://www.comparably.com/search"
            url = add_or_replace_parameter(url, "q", company_name)

            yield scrapy.Request(url=url, headers={"control": "mixin"}, callback=self.parse,
                                 meta={"company": company_name})

    def parse(self, response):
        data = json.loads(response.text)
        r = scrapy.Selector(text=data["body"])

        results = r.xpath("//a[@class='result primary']")

        for res in results:
            res_company_name = res.xpath("descendant-or-self::div[@class='content']/text()").extract_first()
            if res_company_name == "{} Company Page".format(response.meta["company"]):
                url = res.xpath("@href").extract_first()
                yield scrapy.Request(url=url, callback=self.parse_company_page, meta=response.meta)

    def parse_company_page(self, response):
        exception_list = ["About", "Photos", "Financials", "Internship Program",
                          "Competitors", "Jobs", "Salaries", "Trends", "• • •"]

        all_headers = response.xpath("//*[@class='cppNav-list']//a")

        links = {}

        for header in all_headers:
            if header.xpath("text()").extract_first() in exception_list:
                continue
            else:
                links[header.xpath("text()").extract_first()] = header.xpath("@href").extract_first()
        response.meta["header_name"] = "Overview"
        yield from self.parse_raw_html(response)

        for header_name, link in links.items():
            response.meta["header_name"] = header_name
            yield scrapy.Request(url=link, callback=self.parse_raw_html, meta=response.meta)

    def parse_raw_html(self, response):
        header_item = HeaderItem()
        header_item["company_name"] = response.meta["company"]
        header_item["header_name"] = response.meta["header_name"]

        question_selectors = response.xpath("//*[@data-question-id]/div[1]")

        pie_charts = []
        yes_no = []
        user_answers = []
        for question_selector in question_selectors:
            question_label = question_selector.xpath("../following::h3/text()").extract_first()
            if question_selector.xpath("@class").extract_first() == 'insightsPie':
                pie_charts.append({
                    "question": question_label,
                    "percentage": question_selector.xpath("@data-percentage").extract_first()
                })
            elif question_selector.xpath("@class").extract_first() == 'insightsYesNo':
                yes_no.append({
                    "question": question_label,
                    "yes": question_selector.xpath("@data-yes").extract_first(),
                    "no": question_selector.xpath("@data-no").extract_first()
                })
            elif question_selector.xpath("@class").extract_first() == 'result-inner user-answered answered':
                user_answers.append({
                    "question": question_label,
                    "options": self.user_options(question_selector)
                })

        header_item["pie_charts"] = pie_charts
        header_item["yes_no"] = yes_no
        header_item["user_answers"] = user_answers

        yield header_item

    def user_options(self, question_selector):
        options = []
        for ans in question_selector.css('.answer'):
            options.append({
                'title': ans.css('.answer-text::text').extract_first(),
                'percentage': ans.css('[data-percentage]::attr(data-percentage)').extract_first()
            })

        return options

    def read_company_names(self):
        names = []

        with open("Limeade TAM List 10 2018.csv") as f:
                reader = csv.DictReader(f)
                for a in reader:
                    names.append(a["Company Name"])
        return names
