# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
import json


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['www.google.com']

    search_url = "https://www.google.com/search?q=site:{} {}"
    search_keywords = ["Invisalign", "Diamond Plus", "Diamond", "Platinum Plus", "Platinum", 
                       "Gold", "Silver", "Bronze", "Top 1%", "Damon Braces ", 
                       "Damon", "Insignia", "Aligners", "Clear braces", "Clear aligners"]

    # start_urls = ["https://www.google.com/search?q=site:https://arbisoft.com Disco"]
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "DOWNLOAD_DELAY" : 1.5,
        "ROBOTSTXT_OBEY": False,
        "FEED_EXPORT_ENCODING": "utf-8"
    }

    number_of_results = 5

    def start_requests(self):
        search_requests = []
        with open('sample.jl', 'r') as f:
            for line in f.readlines():
                item = json.loads(line)
                site = item.get("website")
                if not site:
                    continue
                for keyword in self.search_keywords:
                    search_requests.append(
                            scrapy.Request(url=self.search_url.format(site, keyword),
                            meta={"keyword": keyword}))
        
        return search_requests

    def parse(self, response):
        item = {"result_stats": response.css("#resultStats::text").extract_first(),
                "keyword_found": [], "keyword": response.meta["keyword"]}
        results = response.css(".g")
        item["website_exists"] = "Y" if item["result_stats"] else "N"

        if len(results) > self.number_of_results:
            for result in results[:self.number_of_results]:
                item["keyword_found"].append({
                    "title": "".join(result.css(".r a ::text").extract()),
                    "url": "https://google.com{}".format(result.css(".r a::attr(href)").extract_first())
                })
        else:
            for result in results:
                item["keyword_found"].append({
                    "title": "".join(result.css(".r a ::text").extract()),
                    "url": "https://google.com{}".format(result.css(".r a::attr(href)").extract_first())
                })

        yield item
