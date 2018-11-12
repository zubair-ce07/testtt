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
        "DOWNLOAD_DELAY" : 1.5,
        "ROBOTSTXT_OBEY": False
    }

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
                "results": [], "keyword": response.meta["keyword"]}
        results = response.css(".g")
        if len(results) > 5:
            for result in results[:5]:
                item["results"].append({
                    "title": "".join(result.css(".r a ::text").extract()),
                    "url": result.css(".r a::attr(href)").extract()
                })
        else:
            for result in results:
                item["results"].append({
                    "title": "".join(result.css(".r a ::text").extract()),
                    "url": result.css(".r a::attr(href)").extract()
                })

        yield item        
        # inspect_response(response, self)
