import json
from datetime import datetime

import scrapy

from util import get_dates_between
from bs4 import BeautifulSoup
import csv


class BaseballSpider(scrapy.Spider):
    name = "baseball"
    start_urls = ["http://sports.news.naver.com/"]

    def __init__(self):
        start_datetime = datetime(2022, 1, 1)
        end_datetime = datetime(2022, 12, 31)
        self.target_dates = get_dates_between(start_datetime, end_datetime)
        self.article_list_url = "https://sports.news.naver.com/kbaseball/news/list?isphoto=N&date={date}&page={page}"
        self.article_url = "https://sports.news.naver.com/news?oid={oid}&aid={aid}"
        self.output_file = open("./baseball.csv", "w")
        self.writer = csv.writer(self.output_file)
        self.writer.writerow(["date", "title", "content"])

    def parse(self, response):
        for target_date in self.target_dates:
            target_url = self.article_list_url.format(date=target_date, page=1)
            req = scrapy.Request(
                url=target_url,
                callback=self.parse_total_pages
            )
            req.meta["date"] = target_date
            yield req

    def parse_total_pages(self, response):
        date = response.meta["date"]
        resp_json = json.loads(response.text)
        total_pages = resp_json["totalPages"]
        for i in range(total_pages):
            req = scrapy.Request(
                url=self.article_list_url.format(date=date, page=i+1),
                callback=self.parse_article_list
            )
            req.meta["date"] = date
            yield req

    def parse_article_list(self, response):
        date = response.meta["date"]
        resp_json = json.loads(response.text)
        for item in resp_json["list"]:
            oid = item["oid"]
            aid = item["aid"]
            req = scrapy.Request(
                url=self.article_url.format(oid=oid, aid=aid),
                callback=self.parse_article
            )
            req.meta["date"] = date
            yield req

    def parse_article(self, response):
        date = response.meta["date"]

        def _remove_tags(parent_soup, target_tag):
            tags = parent_soup.find_all(target_tag)
            for tag in tags:
                tag.decompose()

        soup = BeautifulSoup(response.text, "lxml")
        title = soup.find("h4", class_="title").get_text()
        content_soup = soup.find("div", id="newsEndContents")
        _remove_tags(content_soup, "p")
        _remove_tags(content_soup, "div")
        _remove_tags(content_soup, "em")
        _remove_tags(content_soup, "span")
        content = content_soup.get_text().strip()
        self.writer.writerow([date, title, content])
