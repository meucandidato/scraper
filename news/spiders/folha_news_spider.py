# -*- coding: utf-8 -*-

# import re

from urllib.parse import quote
# from datetime import timedelta, datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import NewsItem


class FolhaNewsSpider(CrawlSpider):
    name = "folha_news"
    allowed_domains = ["search.folha.uol.com.br"]
    rules = [
        Rule(LinkExtractor(allow=r'search\?q=\w.*&sr=\d.'),
             callback='parse_item', follow=True)
    ]
    # TODO: Remove when the robots.txt work again
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "HTTPCACHE_ENABLED": True,
    }

    def __init__(self, keywords="", *args, **kwargs):
        super(FolhaNewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://search.folha.uol.com.br/search/?q={0}&site=todos".format(
                quote(keywords)
            ),
        ]

    def parse_start_url(self, response):
        return self._parse_news(response)

    def parse_item(self, response):
        return self._parse_news(response)

    def _parse_news(self, response):
        news_results = response.xpath(
            '//ol[@class="search-results-list"]/li | '
            '//ol[@class="search-results-list"]/b/li | '
            '//ol[@class="search-results-list"]/b/b/li | '
            '//ol[@class="search-results-list"]/b/b/b/li'
        )

        for news in news_results:
            item = NewsItem()
            header_news = news.xpath('h3/a/text()').extract()[0]
            item['title'] = header_news.split("-")[2]
            item['portal_name'] = header_news.split("-")[0]
            item['posted_at'] = header_news.split("-")[-1]
            item['summary'] = news.xpath(
                'div[@class="content"]/text()'
            ).extract()[0]
            item['image'] = None
            item['url'] = news.xpath('a/@href').extract()[0]
            item['search_origin'] = "Folha de S. Paulo"

            yield item
